import pytest

from badgegen import docs_gen, manifest
from badgegen.config import Settings


def _manifest():
    return manifest.Manifest(badges=[
        manifest.Badge(slug="badge-a", name="A", file="badge-a.png",
                       track="maquinas", status="ok"),
        manifest.Badge(slug="badge-b", name="B", file="badge-b.png",
                       track="maquinas", status="missing"),
        manifest.Badge(slug="badge-c", name="C", file="badge-c.png",
                       track="eventos", status="regen"),
        manifest.Badge(slug="badge-x", name="X", file="badge-x.png",
                       track="", status="missing"),
    ])


def test_readme_tables():
    text = docs_gen.render_readme_tables(_manifest())
    assert "### Máquinas" in text and "### Eventos" in text and "### Otros" in text
    assert "| `badge-a` | A | `badge-a.png` | ✅ |" in text
    assert "| `badge-b` | B | `badge-b.png` | ❌ pendiente |" in text
    assert "🔄 regenerar" in text  # status regen visible
    assert "4 badges activos" in text and "2 sin imagen" in text


def test_missing_only_lists_missing_and_regen():
    text = docs_gen.render_missing(_manifest())
    assert "badge-b" in text and "badge-c" in text and "badge-x" in text
    assert "badge-a" not in text


def test_replace_between_and_missing_markers():
    doc = f"intro\n\n{docs_gen.START}\nviejo\n{docs_gen.END}\ncola\n"
    out = docs_gen.replace_between(doc, "NUEVO")
    assert "NUEVO" in out and "viejo" not in out
    assert out.startswith("intro") and out.rstrip().endswith("cola")
    with pytest.raises(docs_gen.MarkersMissing):
        docs_gen.replace_between("sin marcadores", "x")


def test_write_docs(tmp_path):
    settings = Settings(repo_root=tmp_path)
    (tmp_path / "README.md").write_text(
        f"# título\n\n{docs_gen.START}\n{docs_gen.END}\n", encoding="utf-8")
    (tmp_path / "missing-images.md").write_text(
        f"# faltan\n\n{docs_gen.START}\n{docs_gen.END}\n", encoding="utf-8")
    docs_gen.write_docs(settings, _manifest())
    assert "badge-a" in (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "badge-b" in (tmp_path / "missing-images.md").read_text(encoding="utf-8")
