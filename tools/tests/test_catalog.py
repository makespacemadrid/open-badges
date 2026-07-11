import pytest

from badgegen import catalog

FIXTURE_TS = """
const CATEGORIES: CategorySpec[] = [
  { slug: 'maquinas', name: 'Máquinas', description: 'x', icon: 'i', color: '#fff', order: 1 },
];

const B = (f: string) => `https://cdn.jsdelivr.net/gh/makespacemadrid/open-badges@main/${f}`;

const BADGES: BadgeSpec[] = [
  {
    oldSlug: 'i-can-print',
    slug: 'badge-i-can-print',
    name: 'I Can Print (3D)',
    description: 'Ha completado su primera impresión 3D.',
    criteria: 'Completar la primera impresión 3D.',
    categorySlug: 'maquinas',
    achievementType: 'Certification',
    imageUrl: B('badge-i-can-print.png'),
    questSlugs: ['first-3d-print'],
  },
  {
    slug: 'badge-multilinea',
    name: 'Multi Línea',
    description:
      'Descripción en la línea siguiente con \\'comilla\\' escapada.',
    criteria: 'Criterio.',
    categorySlug: 'eventos',
    achievementType: 'Award',
    questGroups: [
      { label: 'vía A', questSlugs: ['q-1'] },
      { label: 'vía B', questSlugs: ['q-2'] },
    ],
  },
  {
    slug: 'badge-retirado',
    name: 'Retirado',
    description: 'Ya no existe.',
    criteria: 'N/A.',
    categorySlug: null,
    achievementType: 'Achievement',
    retire: true,
  },
  {
    slug: 'eventos-primer-paso',
    name: 'Groupie',
    description: 'Primer evento.',
    criteria: 'Asistir a un evento.',
    categorySlug: 'eventos',
    achievementType: 'Achievement',
    trackSlug: 'eventos',
    trackCountThreshold: 1,
  },
];

export async function applyBadgeCatalog() {}
"""


def _write(tmp_path, text=FIXTURE_TS):
    p = tmp_path / "catalog.ts"
    p.write_text(text, encoding="utf-8")
    return p


def test_parse_entries(tmp_path):
    entries = catalog.parse_catalog(_write(tmp_path))
    assert len(entries) == 4  # las CATEGORIES no cuentan
    by_slug = {e.slug: e for e in entries}
    e = by_slug["badge-i-can-print"]
    assert e.name == "I Can Print (3D)"
    assert e.track == "maquinas"
    assert e.image_file == "badge-i-can-print.png"
    assert e.retired is False


def test_multiline_and_nested_groups(tmp_path):
    by_slug = {e.slug: e for e in catalog.parse_catalog(_write(tmp_path))}
    e = by_slug["badge-multilinea"]
    assert e.description == "Descripción en la línea siguiente con 'comilla' escapada."
    assert e.image_file is None  # sin imageUrl


def test_retired_and_null_category(tmp_path):
    by_slug = {e.slug: e for e in catalog.parse_catalog(_write(tmp_path))}
    assert by_slug["badge-retirado"].retired is True
    assert by_slug["badge-retirado"].track == ""


def test_default_file():
    assert catalog.default_file("eventos-primer-paso") == "badge-eventos-primer-paso.png"
    assert catalog.default_file("badge-i-can-laser") == "badge-i-can-laser.png"


def test_parse_errors(tmp_path):
    with pytest.raises(catalog.CatalogParseError):
        catalog.parse_catalog(_write(tmp_path, "const OTRA = 1;"))
    with pytest.raises(catalog.CatalogParseError):
        catalog.parse_catalog(_write(tmp_path, "const BADGES: BadgeSpec[] = [];"))
