"""CLI de badgegen: sync | scan | generate | review | promote | fix | docs."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from PIL import Image

from badgegen import catalog, docs_gen, gallery, generate as generate_mod, manifest as manifest_mod, promote as promote_mod, qc
from badgegen.config import Settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="badgegen",
                                     description="Generación y QC de imágenes de Open Badges")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sync = sub.add_parser("sync", help="catálogo del portal → badges.yaml")
    p_sync.add_argument("--catalog", type=Path, default=None)

    p_scan = sub.add_parser("scan", help="QC de las imágenes existentes")
    p_scan.add_argument("slugs", nargs="*")
    p_scan.add_argument("--judge", action="store_true")
    p_scan.add_argument("--write", action="store_true")

    p_gen = sub.add_parser("generate", help="genera candidatos")
    p_gen.add_argument("slugs", nargs="*")
    p_gen.add_argument("--status", default="missing,regen")
    p_gen.add_argument("-n", type=int, default=4)
    p_gen.add_argument("--provider", choices=["gemini", "custom"], default=None)
    p_gen.add_argument("--model", default=None)

    p_rev = sub.add_parser("review", help="regenera la galería de candidatos")
    p_rev.add_argument("slugs", nargs="*")

    p_pro = sub.add_parser("promote", help="candidato → imagen final")
    p_pro.add_argument("slug")
    p_pro.add_argument("candidate", type=Path)
    p_pro.add_argument("--keep-candidates", action="store_true")

    p_fix = sub.add_parser("fix", help="post-proceso in-place del PNG final")
    p_fix.add_argument("slug")

    sub.add_parser("docs", help="regenera README.md y missing-images.md")
    return parser


def _load(settings: Settings) -> manifest_mod.Manifest:
    if settings.manifest_path.is_file():
        return manifest_mod.load(settings.manifest_path)
    return manifest_mod.Manifest()


def cmd_sync(settings: Settings, args) -> int:
    m = _load(settings)
    entries = catalog.parse_catalog(args.catalog or settings.catalog_path)
    warnings = catalog.merge_catalog(m, entries, settings.repo_root)
    manifest_mod.save(m, settings.manifest_path)
    counts = {s: sum(1 for b in m.badges if b.status == s) for s in ("ok", "missing", "regen")}
    print(f"{len(m.badges)} badges en manifiesto: {counts}")
    for warning in warnings:
        print(f"AVISO: {warning}")
    return 0


def cmd_scan(settings: Settings, args) -> int:
    m = _load(settings)
    badges = generate_mod.select_badges(m, args.slugs or None, None) if args.slugs \
        else [b for b in m.badges if b.status != "missing"]
    rows = []
    for badge in badges:
        path = settings.repo_root / badge.file
        if not path.is_file():
            continue
        result = qc.check_image(Image.open(path), threshold=m.roundness_threshold)
        judge_score, judge_issues = None, []
        if args.judge:
            verdict = qc.judge_legibility(path.read_bytes(), os.environ["GEMINI_API_KEY"])
            judge_score, judge_issues = verdict.score, verdict.issues
            if verdict.score <= 3:
                result.issues.append("low-legibility")
        rows.append({"slug": badge.slug, "file": badge.file,
                     "roundness": result.roundness, "issues": result.issues,
                     "judge_score": judge_score, "judge_issues": judge_issues})
        if args.write:
            badge.issues = list(result.issues)
        flag = "OK " if not result.issues else "!! "
        print(f"{flag}{badge.slug} redondez={result.roundness:.4f} {result.issues}")
    if args.write:
        manifest_mod.save(m, settings.manifest_path)
    out = gallery.write_scan_report(settings, rows)
    print(f"informe: {out}")
    return 0


def cmd_generate(settings: Settings, args) -> int:
    from badgegen.providers import get_provider

    m = _load(settings)
    provider = get_provider(args.provider, model=args.model)
    statuses = None if args.slugs else [s.strip() for s in args.status.split(",") if s.strip()]
    report = generate_mod.run_generate(settings, m, provider,
                                       slugs=args.slugs or None, statuses=statuses, n=args.n)
    errors = 0
    for slug, outcome in report.items():
        if isinstance(outcome, str):
            errors += 1
            print(f"!! {slug}: {outcome}")
        else:
            print(f"OK {slug}: {len(outcome)} candidatos")
    _write_review(settings, m, None)
    return 1 if errors else 0


def cmd_review(settings: Settings, args) -> int:
    m = _load(settings)
    _write_review(settings, m, args.slugs or None)
    return 0


def _write_review(settings: Settings, m, slugs) -> None:
    items = []
    if not settings.candidates_dir.is_dir():
        print("no hay candidatos")
        return
    for directory in sorted(settings.candidates_dir.iterdir()):
        if not directory.is_dir() or (slugs and directory.name not in slugs):
            continue
        badge = m.get(directory.name)
        candidates = []
        for png in sorted(directory.glob("*.png")):
            sidecar_path = png.with_suffix(".json")
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8")) if sidecar_path.is_file() else {}
            qc_data = sidecar.get("qc", {})
            candidates.append({
                "file": str(png.relative_to(settings.repo_root)),
                "qc_ok": not qc_data.get("issues"),
                "roundness": qc_data.get("roundness", 0.0),
                "provider": sidecar.get("provider", "?"),
                "model": sidecar.get("model", "?"),
            })
        if candidates:
            current = badge.file if badge and (settings.repo_root / badge.file).is_file() else None
            items.append({"slug": directory.name, "current": current, "candidates": candidates})
    out = gallery.write_review(settings, items)
    print(f"galería: {out}")


def cmd_promote(settings: Settings, args) -> int:
    m = _load(settings)
    candidate = args.candidate if args.candidate.is_absolute() \
        else settings.repo_root / args.candidate
    final = promote_mod.promote(settings, m, args.slug, candidate,
                                keep=args.keep_candidates)
    print(f"promocionado: {final}")
    return 0


def cmd_fix(settings: Settings, args) -> int:
    m = _load(settings)
    final = promote_mod.fix(settings, m, args.slug)
    print(f"corregido in-place: {final}")
    return 0


def cmd_docs(settings: Settings, args) -> int:
    m = _load(settings)
    docs_gen.write_docs(settings, m)
    print("README.md y missing-images.md regenerados")
    return 0


COMMANDS = {
    "sync": cmd_sync,
    "scan": cmd_scan,
    "generate": cmd_generate,
    "review": cmd_review,
    "promote": cmd_promote,
    "fix": cmd_fix,
    "docs": cmd_docs,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings.locate()
    return COMMANDS[args.command](settings, args)
