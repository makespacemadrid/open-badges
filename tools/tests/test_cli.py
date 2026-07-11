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
