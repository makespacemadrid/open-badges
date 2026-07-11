from badgegen import cli


def test_parser_has_all_subcommands():
    parser = cli.build_parser()
    sub = {a.dest: a for a in parser._subparsers._group_actions}["command"]
    assert set(sub.choices) == {"sync", "scan", "generate", "review", "promote", "fix", "docs"}


def test_generate_defaults():
    args = cli.build_parser().parse_args(["generate"])
    assert args.status == "missing,regen" and args.n == 4 and args.provider is None


def test_promote_args():
    args = cli.build_parser().parse_args(
        ["promote", "badge-a", "candidates/badge-a/01-gemini.png", "--keep-candidates"])
    assert args.slug == "badge-a" and args.keep_candidates is True


def test_main_docs_roundtrip(tmp_path, monkeypatch, make_badge):
    # main() con settings inyectados vía monkeypatch de Settings.locate
    from badgegen import docs_gen, manifest
    from badgegen.config import Settings

    settings = Settings(repo_root=tmp_path)
    monkeypatch.setattr(Settings, "locate", classmethod(lambda cls: settings))
    manifest.save(manifest.Manifest(badges=[
        manifest.Badge(slug="badge-a", name="A", file="badge-a.png", status="missing"),
    ]), settings.manifest_path)
    for name in ("README.md", "missing-images.md"):
        (tmp_path / name).write_text(f"x\n\n{docs_gen.START}\n{docs_gen.END}\n", encoding="utf-8")
    assert cli.main(["docs"]) == 0
    assert "badge-a" in (tmp_path / "README.md").read_text(encoding="utf-8")


def _repo_with_badge(tmp_path, monkeypatch, make_badge):
    from badgegen import manifest
    from badgegen.config import Settings
    from tests.conftest import png_bytes

    settings = Settings(repo_root=tmp_path)
    monkeypatch.setattr(Settings, "locate", classmethod(lambda cls: settings))
    manifest.save(manifest.Manifest(badges=[
        manifest.Badge(slug="badge-a", name="A", file="badge-a.png", status="ok"),
        manifest.Badge(slug="badge-b", name="B", file="badge-b.png", status="ok"),
    ]), settings.manifest_path)
    (tmp_path / "badge-a.png").write_bytes(png_bytes(make_badge()))
    (tmp_path / "badge-b.png").write_bytes(png_bytes(make_badge()))
    return settings


def test_scan_judge_without_key_clear_error(tmp_path, monkeypatch, make_badge, capsys):
    _repo_with_badge(tmp_path, monkeypatch, make_badge)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert cli.main(["scan", "--judge"]) == 1
    assert "GEMINI_API_KEY" in capsys.readouterr().out


def test_scan_judge_failure_does_not_abort(tmp_path, monkeypatch, make_badge):
    from badgegen import qc

    settings = _repo_with_badge(tmp_path, monkeypatch, make_badge)
    monkeypatch.setenv("GEMINI_API_KEY", "K")

    def boom(png, key, **kw):
        raise RuntimeError("api caída")

    monkeypatch.setattr(qc, "judge_legibility", boom)
    assert cli.main(["scan", "--judge"]) == 0
    report = (settings.review_dir / "scan-report.html").read_text(encoding="utf-8")
    assert "badge-a" in report and "badge-b" in report
