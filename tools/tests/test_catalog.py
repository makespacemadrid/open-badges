import pytest

from badgegen import catalog

FIXTURE_TS = """
const CATEGORIES: CategorySpec[] = [
  { slug: 'maquinas', name: 'Máquinas', description: 'x', icon: 'i', color: '#fff', order: 1 },
];

const QUESTS: QuestSpec[] = [
  {
    slug: 'first-3d-print',
    title: 'Primera impresión',
    description: 'x',
    icon: 'i',
    order: 1,
    trackSlug: 'printing-ladder',
    trackLevel: 2,
  },
  { slug: 'q-1', title: 'A', description: 'x', icon: 'i', order: 2 },
  { slug: 'q-2', title: 'B', description: 'x', icon: 'i', order: 3 },
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
    assert e.category == "maquinas"
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
    assert by_slug["badge-retirado"].category == ""


def test_default_file():
    assert catalog.default_file("eventos-primer-paso") == "badge-eventos-primer-paso.png"
    assert catalog.default_file("badge-i-can-laser") == "badge-i-can-laser.png"


def test_parse_errors(tmp_path):
    with pytest.raises(catalog.CatalogParseError):
        catalog.parse_catalog(_write(tmp_path, "const OTRA = 1;"))
    with pytest.raises(catalog.CatalogParseError):
        catalog.parse_catalog(_write(tmp_path, "const BADGES: BadgeSpec[] = [];"))


FIXTURE_TS_COMMENTS = """
const BADGES: BadgeSpec[] = [
  {
    slug: 'badge-uno',
    name: 'Uno',
    description: 'Primera entrada.',
    criteria: 'Criterio uno.',
    categorySlug: 'maquinas',
    achievementType: 'Achievement',
  },
  // Sofía's badge — don't count
  {
    slug: 'badge-dos',
    /* isn't this fun */
    name: 'Dos',
    description: 'Segunda entrada.',
    criteria: 'Criterio dos.',
    categorySlug: 'maquinas',
    achievementType: 'Achievement',
  },
];
"""


def test_comments_with_apostrophes_do_not_break_scanner(tmp_path):
    entries = catalog.parse_catalog(_write(tmp_path, FIXTURE_TS_COMMENTS))
    slugs = {e.slug for e in entries}
    assert slugs == {"badge-uno", "badge-dos"}


FIXTURE_TS_DOUBLE_QUOTED = """
const BADGES: BadgeSpec[] = [
  {
    slug: 'badge-apostrofe',
    name: "Apóstrofe",
    description: "isn't this fun",
    criteria: 'Criterio.',
    categorySlug: 'maquinas',
    achievementType: 'Achievement',
  },
];
"""


def test_double_quoted_string_with_apostrophe(tmp_path):
    by_slug = {e.slug: e for e in catalog.parse_catalog(_write(tmp_path, FIXTURE_TS_DOUBLE_QUOTED))}
    e = by_slug["badge-apostrofe"]
    assert e.name == "Apóstrofe"
    assert e.description == "isn't this fun"


def test_track_extraction(tmp_path):
    by_slug = {e.slug: e for e in catalog.parse_catalog(_write(tmp_path))}
    # hereda el track de su quest (trackLevel máximo)
    printed = by_slug["badge-i-can-print"]
    assert printed.track == "printing-ladder" and printed.track_level == 2
    # badge de colección: su propio trackSlug + threshold como nivel
    groupie = by_slug["eventos-primer-paso"]
    assert groupie.track == "eventos" and groupie.track_level == 1
    # quests sin track -> badge sin track
    multi = by_slug["badge-multilinea"]
    assert multi.track is None and multi.track_level is None
