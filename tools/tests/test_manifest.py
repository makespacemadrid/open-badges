from pathlib import Path

from badgegen import manifest


def _badge(**kw):
    base = dict(slug="badge-x", name="X", file="badge-x.png")
    base.update(kw)
    return manifest.Badge(**base)


def test_roundtrip(tmp_path):
    m = manifest.Manifest(
        style="estilo global",
        reference_images=["badge-template.png"],
        badges=[
            _badge(visual="un láser", status="regen", issues=["flattened-circle"], prompt_extra="extra"),
            _badge(slug="badge-y", name="Y", file="badge-y.png"),
        ],
    )
    p = tmp_path / "badges.yaml"
    manifest.save(m, p)
    m2 = manifest.load(p)
    assert m2.style == "estilo global"
    assert m2.target_diameter == 1180
    assert m2.roundness_threshold == 0.985
    assert len(m2.badges) == 2
    b = m2.get("badge-x")
    assert b.visual == "un láser"
    assert b.status == "regen"
    assert b.issues == ["flattened-circle"]
    assert b.prompt_extra == "extra"
    assert m2.get("badge-y").status == "missing"
    assert m2.get("no-existe") is None


def test_load_defaults_missing_keys(tmp_path):
    p = tmp_path / "badges.yaml"
    p.write_text("badges:\n  - slug: badge-z\n    name: Z\n    file: badge-z.png\n", encoding="utf-8")
    m = manifest.load(p)
    assert m.style == manifest.DEFAULT_STYLE
    assert m.reference_images == manifest.DEFAULT_REFERENCES
    b = m.get("badge-z")
    assert b.status == "missing" and b.issues == [] and b.visual is None


def test_save_omits_null_optionals(tmp_path):
    p = tmp_path / "badges.yaml"
    manifest.save(manifest.Manifest(badges=[_badge()]), p)
    text = p.read_text(encoding="utf-8")
    assert "provider" not in text  # opcionales None no ensucian el YAML
    assert "prompt_extra" not in text
    assert "slug: badge-x" in text
