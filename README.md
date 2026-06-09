# open-badges — Makespace Madrid

Repositorio de imágenes para los Open Badges de Makespace Madrid.

Las imágenes se sirven via **jsDelivr CDN**. Para invalidar la caché tras actualizar una imagen:

```
GET https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/<filename>
```

URL base del catálogo en el portal: `https://cdn.jsdelivr.net/gh/makespacemadrid/open-badges@main/`

---

## Catálogo de badges

### Onboarding

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-hola-mundo` | Hello, World! | `badge-hello-world.png` | ✅ |
| `badge-maker` | Maker Padawan | `badge-maker101.png` | ✅ |

### Máquinas

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-i-can-print` | I Can Print (3D) | `badge-i-can-print.png` | ✅ |
| `badge-i-can-vinyl` | I Can Vinyl | `badge-i-can-vinyl.png` | ✅ |
| `badge-can-cnc` | I Can CNC | `badge-i-can-cnc.png` | ✅ |
| `badge-i-can-solder` | I Can Solder | `badge-i-can-solder.png` | ✅ |
| `badge-i-can-pcb` | I Can PCB | `badge-i-can-pcb.png` | ✅ |
| `badge-i-can-sew` | I Can Sew | `badge-i-can-sew.png` | ✅ |
| `badge-i-can-sublimate` | I Can Sublimate | `badge-i-can-sublimate.png` | ✅ |
| `badge-jack-of-all-trades` | Jack of all trades | `badge-jack-all-trades.png` | ✅ |

### Comunidad

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-embajador-maker` | Space Ambassador | `badge-maker-ambassador.png` | ✅ |
| `badge-garbage-collector` | Garbage Collector | `badge-garbage-collector.png` | ✅ |
| `badge-por-el-bien-comun` | For the Greater Good | `badge-common-good.png` | ✅ |
| `badge-creador-plataformas` | Platform Builder | `badge-platform-maker.png` | ✅ |
| `badge-hacked-the-space` | Hacked the Space | `badge-hack-the-space.png` | ✅ |

> `badge-hackthespace.png` es un duplicado alternativo de `badge-hack-the-space.png` — sin uso activo en el catálogo.

### Plataformas — GLaDOS (`track: glados-messages`)

| Slug | Nombre | Track nivel | Umbral | Imagen | Estado |
|------|--------|-------------|--------|--------|--------|
| `badge-hello-glados` | Hello, GLaDOS! | 1 | 1 msg | — | ❌ pendiente |
| `badge-still-alive` | Still Alive | 2 | 10 msg | — | ❌ pendiente |
| `badge-test-subject` | Test Subject | 3 | 50 msg | — | ❌ pendiente |
| `badge-property-of-aperture` | Property of Aperture | 4 | 100 msg | — | ❌ pendiente |
| `badge-cake-is-a-lie` | The Cake Is a Lie | 5 | 500 msg | — | ❌ pendiente |

### Plataformas — Docmost / wiki (`track: docmost-pages`)

| Slug | Nombre | Track nivel | Umbral | Imagen | Estado |
|------|--------|-------------|--------|--------|--------|
| `badge-first-draft` | First Draft | 1 | 1 página | — | ❌ pendiente |
| `badge-wiki-contributor` | Wiki Contributor | 2 | 10 páginas | — | ❌ pendiente |
| `badge-archivist` | Archivist | 3 | 25 páginas | — | ❌ pendiente |
| `badge-space-chronicler` | Space Chronicler | 4 | 50 páginas | — | ❌ pendiente |
| `badge-guardian-of-knowledge` | Guardian of Knowledge | 5 | 100 páginas | `badge-knowledge-keeper.png` | ✅ |

### Plataformas — Ocabra / tokens IA (`track: ocabra-tokens`)

| Slug | Nombre | Track nivel | Umbral | Imagen | Estado |
|------|--------|-------------|--------|--------|--------|
| `badge-first-queries` | First Queries | 1 | 10 K tokens | — | ❌ pendiente |
| `badge-token-collector` | Token Collector | 2 | 100 K tokens | — | ❌ pendiente |
| `badge-burning-tokens` | Burning Tokens | 3 | 1 M tokens | — | ❌ pendiente |
| `badge-gpu-melter` | GPU Melter | 4 | 5 M tokens | — | ❌ pendiente |
| `badge-infinite-loop` | Infinite Loop | 5 | 10 M tokens | — | ❌ pendiente |

### Eventos

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-ctf-v1` | Capture the Flag v1 | `badge-ctf-v1.png` | ✅ |
| `badge-been-there` | Been there, done that | `badge-been-there.png` | ✅ |
| `badge-evento-nerdearla2025` | Nerdearla 2025 | `badge-nerdearla-2025.png` | ✅ |
| `badge-evento-codemotion2026` | Codemotion 2026 | `badge-codemotion-2026.png` | ✅ |

#### Hack the Space (`track: hack-the-space`, 9 niveles)

| Slug | Nombre | Sesiones | Imagen | Estado |
|------|--------|----------|--------|--------|
| `badge-first-hack` | First Hack | 1 | — | ❌ pendiente |
| `badge-hammer-time` | Hammer Time | 3 | — | ❌ pendiente |
| `badge-space-regular` | Space Regular | 5 | — | ❌ pendiente |
| `badge-hackspace-veteran` | Hackspace Veteran | 10 | — | ❌ pendiente |
| `badge-master-hacker` | Master Hacker | 15 | — | ❌ pendiente |
| `badge-hackspace-elder` | Hackspace Elder | 20 | — | ❌ pendiente |
| `badge-hackspace-legend` | Hackspace Legend | 25 | — | ❌ pendiente |
| `badge-hackspace-hero` | Hackspace Hero | 30 | — | ❌ pendiente |
| `badge-hackspace-immortal` | Hackspace Immortal | 35 | — | ❌ pendiente |

#### Reunión mensual (`track: reunion-mensual`, 9 niveles)

| Slug | Nombre | Reuniones | Imagen | Estado |
|------|--------|-----------|--------|--------|
| `badge-first-assembly` | First Assembly | 1 | — | ❌ pendiente |
| `badge-assembly-regular` | Assembly Regular | 3 | — | ❌ pendiente |
| `badge-council-member` | Council Member | 5 | — | ❌ pendiente |
| `badge-community-veteran` | Community Veteran | 10 | — | ❌ pendiente |
| `badge-community-pillar` | Community Pillar | 15 | — | ❌ pendiente |
| `badge-assembly-elder` | Assembly Elder | 20 | — | ❌ pendiente |
| `badge-assembly-legend` | Assembly Legend | 25 | — | ❌ pendiente |
| `badge-marathon-member` | Marathon Member | 30 | — | ❌ pendiente |
| `badge-eternal-council` | Eternal Council | 35 | — | ❌ pendiente |

### Membresía

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-miembro-makespace` | Makespace Member | `badge-member.png` | ✅ |
| `makespace-key` | Keys of Kingdom | `badge-keys-of-kingdom.png` | ✅ |
| `badge-first-year` | First Year (1 año) | — | ❌ pendiente |
| `badge-second-year` | Second Year (2 años) | — | ❌ pendiente |
| `badge-third-year` | Third Year (3 años) | — | ❌ pendiente |
| `badge-fourth-year` | Fourth Year (4 años) | — | ❌ pendiente |
| `badge-fifth-year` | Fifth Year (5 años) | — | ❌ pendiente |
| `badge-sixth-year` | Sixth Year (6 años) | — | ❌ pendiente |
| `badge-seventh-year` | Seventh Year (7 años) | — | ❌ pendiente |
| `badge-eighth-year` | Eighth Year (8 años) | — | ❌ pendiente |
| `badge-ninth-year` | Ninth Year (9 años) | — | ❌ pendiente |
| `badge-10-years` | A Decade at Makespace (10 años) | — | ❌ pendiente |
| `badge-11-years` | Eleven Years (11 años) | — | ❌ pendiente |
| `badge-12-years` | Twelve Years (12 años) | — | ❌ pendiente |
| `badge-13-years` | Thirteen Years (13 años) | — | ❌ pendiente |
| `badge-founding-member` | **Founding Member** | — | ❌ pendiente |

> `badge-founding-member` es el badge de mayor rango: para mecenas del crowdfunding fundacional de Makespace Madrid (2012-2013). Concesión manual por admin.

---

## Imágenes disponibles sin badge asignado

| Archivo | Posible uso |
|---------|-------------|
| `badge-data-scrubber.png` | Badge futuro (limpieza de datos / GDPR) |
| `badge-hackthespace.png` | Duplicado alternativo de `badge-hack-the-space.png` |
| `badge-liquid-cooling.png` | Sin badge asignado — uso indeterminado |
| `badge-template.png` | Plantilla base para crear nuevos badges |

---

## Convención de nombres

`badge-<slug>.png` — mismo slug que el badge en el portal, con guiones en lugar de underscore.

Resolución recomendada: **512×512 px**, fondo transparente o con círculo de color de categoría.
