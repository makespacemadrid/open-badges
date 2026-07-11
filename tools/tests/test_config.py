import os
from pathlib import Path

from badgegen import config


def test_settings_paths(tmp_path):
    s = config.Settings(repo_root=tmp_path)
    assert s.manifest_path == tmp_path / "badges.yaml"
    assert s.candidates_dir == tmp_path / "candidates"
    assert s.review_dir == tmp_path / "review"
    assert s.readme_path == tmp_path / "README.md"
    assert s.missing_path == tmp_path / "missing-images.md"
    assert s.env_path == tmp_path / "tools" / ".env"


def test_catalog_path_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv("BADGEGEN_CATALOG", "/outro/catalog.ts")
    s = config.Settings(repo_root=tmp_path)
    assert s.catalog_path == Path("/outro/catalog.ts")
    monkeypatch.delenv("BADGEGEN_CATALOG")
    assert "InfraSelfService" in str(s.catalog_path)


def test_load_env_file(tmp_path, monkeypatch):
    monkeypatch.delenv("FOO_KEY", raising=False)
    monkeypatch.setenv("YA_EXISTE", "original")
    env = tmp_path / ".env"
    env.write_text("# comentario\nFOO_KEY=abc123\nYA_EXISTE=nuevo\n\nMALFORMADO\n")
    config.load_env_file(env)
    assert os.environ["FOO_KEY"] == "abc123"
    assert os.environ["YA_EXISTE"] == "original"  # no pisa
    config.load_env_file(tmp_path / "no-existe.env")  # no revienta


def test_constants():
    assert config.CANVAS_SIZE == 1254
    assert config.TARGET_DIAMETER == 1180
    assert config.ROUNDNESS_THRESHOLD == 0.985
    assert config.MIN_FIXABLE_RATIO == 0.95
    assert "{file}" in config.JSDELIVR_PURGE
