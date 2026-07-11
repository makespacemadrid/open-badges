from badgegen import catalog, manifest


def _entry(**kw):
    base = dict(slug="badge-a", name="A", description="d", criteria="c",
                category="maquinas", image_file=None, retired=False)
    base.update(kw)
    return catalog.CatalogEntry(**base)


def test_new_badge_added_with_status_by_file(tmp_path):
    (tmp_path / "badge-a.png").write_bytes(b"png")
    m = manifest.Manifest(badges=[])
    warnings = catalog.merge_catalog(m, [_entry(), _entry(slug="badge-b", name="B")], tmp_path)
    assert warnings == []
    a, b = m.get("badge-a"), m.get("badge-b")
    assert a.status == "ok" and a.file == "badge-a.png" and a.category == "maquinas"
    assert b.status == "missing" and b.file == "badge-b.png"


def test_image_file_wins_over_convention(tmp_path):
    m = manifest.Manifest(badges=[])
    catalog.merge_catalog(m, [_entry(slug="badge-embajador", image_file="badge-maker-ambassador.png")], tmp_path)
    assert m.get("badge-embajador").file == "badge-maker-ambassador.png"


def test_manual_fields_survive_sync(tmp_path):
    b = manifest.Badge(slug="badge-a", name="viejo", file="badge-a.png",
                       visual="mi visual", status="regen", issues=["flattened-circle"],
                       provider="custom", prompt_extra="extra")
    (tmp_path / "badge-a.png").write_bytes(b"png")
    m = manifest.Manifest(badges=[b])
    catalog.merge_catalog(m, [_entry(name="Nuevo Nombre")], tmp_path)
    assert b.name == "Nuevo Nombre"          # sincronizado
    assert b.visual == "mi visual"           # intacto
    assert b.status == "regen"               # regen nunca se recalcula
    assert b.issues == ["flattened-circle"]
    assert b.provider == "custom" and b.prompt_extra == "extra"


def test_status_recomputed_ok_missing(tmp_path):
    b = manifest.Badge(slug="badge-a", name="A", file="badge-a.png", status="missing")
    m = manifest.Manifest(badges=[b])
    (tmp_path / "badge-a.png").write_bytes(b"png")
    catalog.merge_catalog(m, [_entry()], tmp_path)
    assert b.status == "ok"


def test_retired_skipped_and_orphan_warned(tmp_path):
    m = manifest.Manifest(badges=[manifest.Badge(slug="badge-huerfano", name="H", file="h.png")])
    warnings = catalog.merge_catalog(m, [_entry(slug="badge-r", retired=True)], tmp_path)
    assert m.get("badge-r") is None
    assert any("badge-huerfano" in w for w in warnings)
