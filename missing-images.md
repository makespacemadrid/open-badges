# Badges sin imagen — pendientes de generar

Lista de badges del catálogo del portal que todavía no tienen imagen en este repositorio.
El nombre de archivo sugerido sigue la convención `badge-<slug>.png`.

Para actualizar la imagen en el portal una vez subida al repo, ejecutar desde el servidor:
```
npx prisma db seed
```
(El seed usa `applyBadgeCatalog` que asigna `imageUrl` automáticamente si la badge no tiene imagen.)

---

## Plataformas — GLaDOS (`track: glados-messages`)

Sugerencia de estética: iconografía Portal 2 (cubo compañero, pasteles, cámaras de pruebas).

| Slug | Nombre | Track | Nivel | Umbral | Archivo sugerido |
|------|--------|-------|-------|--------|-----------------|
| `badge-hello-glados` | Hello, GLaDOS! | `glados-messages` | 1 | 1 msg | `badge-hello-glados.png` |
| `badge-still-alive` | Still Alive | `glados-messages` | 2 | 10 msg | `badge-still-alive.png` |
| `badge-test-subject` | Test Subject | `glados-messages` | 3 | 50 msg | `badge-test-subject.png` |
| `badge-property-of-aperture` | Property of Aperture | — | — | 100 msg ⚠️ | `badge-property-of-aperture.png` |
| `badge-cake-is-a-lie` | The Cake Is a Lie | `glados-messages` | 5 | 500 msg | `badge-cake-is-a-lie.png` |

> ⚠️ `badge-property-of-aperture` no tiene quest asociado en el catálogo (falta nivel 4 / 100 msg en el track `glados-messages`). Es badge de otorgamiento manual hasta que se añada el quest.

## Plataformas — Docmost / wiki (`track: docmost-pages`)

Sugerencia de estética: libros, plumas, pergaminos, rollos de conocimiento.

| Slug | Nombre | Track | Nivel | Umbral | Archivo sugerido |
|------|--------|-------|-------|--------|-----------------|
| `badge-first-draft` | First Draft | `docmost-pages` | 1 | 1 página | `badge-first-draft.png` |
| `badge-wiki-contributor` | Wiki Contributor | `docmost-pages` | 2 | 10 páginas | `badge-wiki-contributor.png` |
| `badge-archivist` | Archivist | `docmost-pages` | 3 | 25 páginas | `badge-archivist.png` |
| `badge-space-chronicler` | Space Chronicler | `docmost-pages` | 4 | 50 páginas | `badge-space-chronicler.png` |

> `badge-guardian-of-knowledge` (nivel 5, 100 páginas) ya tiene imagen: `badge-knowledge-keeper.png`.

## Plataformas — Ocabra / tokens IA (`track: ocabra-tokens`)

Sugerencia de estética: chips, GPUs, fuego/calor, tokens crypto-like.

| Slug | Nombre | Track | Nivel | Umbral | Archivo sugerido |
|------|--------|-------|-------|--------|-----------------|
| `badge-first-queries` | First Queries | `ocabra-tokens` | 1 | 10 K tokens | `badge-first-queries.png` |
| `badge-token-collector` | Token Collector | `ocabra-tokens` | 2 | 100 K tokens | `badge-token-collector.png` |
| `badge-burning-tokens` | Burning Tokens | `ocabra-tokens` | 3 | 1 M tokens | `badge-burning-tokens.png` |
| `badge-gpu-melter` | GPU Melter | `ocabra-tokens` | 4 | 5 M tokens | `badge-gpu-melter.png` |
| `badge-infinite-loop` | Infinite Loop | `ocabra-tokens` | 5 | 10 M tokens | `badge-infinite-loop.png` |

## Eventos — Hack the Space (`track: hack-the-space`, 9 niveles)

Sugerencia: iconografía de herramientas / taller con niveles de desgaste creciente.
Se pueden usar variantes del mismo diseño (bronce → plata → oro → …).

| Slug | Nombre | Track | Nivel (trackCountThreshold) | Archivo sugerido |
|------|--------|-------|-----------------------------|-----------------|
| `badge-first-hack` | First Hack | `hack-the-space` | 1 sesión | `badge-first-hack.png` |
| `badge-hammer-time` | Hammer Time | `hack-the-space` | 3 sesiones | `badge-hammer-time.png` |
| `badge-space-regular` | Space Regular | `hack-the-space` | 5 sesiones | `badge-space-regular.png` |
| `badge-hackspace-veteran` | Hackspace Veteran | `hack-the-space` | 10 sesiones | `badge-hackspace-veteran.png` |
| `badge-master-hacker` | Master Hacker | `hack-the-space` | 15 sesiones | `badge-master-hacker.png` |
| `badge-hackspace-elder` | Hackspace Elder | `hack-the-space` | 20 sesiones | `badge-hackspace-elder.png` |
| `badge-hackspace-legend` | Hackspace Legend | `hack-the-space` | 25 sesiones | `badge-hackspace-legend.png` |
| `badge-hackspace-hero` | Hackspace Hero | `hack-the-space` | 30 sesiones | `badge-hackspace-hero.png` |
| `badge-hackspace-immortal` | Hackspace Immortal | `hack-the-space` | 35 sesiones | `badge-hackspace-immortal.png` |

## Eventos — Reunión mensual (`track: reunion-mensual`, 9 niveles)

Sugerencia: iconografía de asamblea / democracia participativa con niveles de antigüedad.

| Slug | Nombre | Track | Nivel (trackCountThreshold) | Archivo sugerido |
|------|--------|-------|-----------------------------|-----------------|
| `badge-first-assembly` | First Assembly | `reunion-mensual` | 1 reunión | `badge-first-assembly.png` |
| `badge-assembly-regular` | Assembly Regular | `reunion-mensual` | 3 reuniones | `badge-assembly-regular.png` |
| `badge-council-member` | Council Member | `reunion-mensual` | 5 reuniones | `badge-council-member.png` |
| `badge-community-veteran` | Community Veteran | `reunion-mensual` | 10 reuniones | `badge-community-veteran.png` |
| `badge-community-pillar` | Community Pillar | `reunion-mensual` | 15 reuniones | `badge-community-pillar.png` |
| `badge-assembly-elder` | Assembly Elder | `reunion-mensual` | 20 reuniones | `badge-assembly-elder.png` |
| `badge-assembly-legend` | Assembly Legend | `reunion-mensual` | 25 reuniones | `badge-assembly-legend.png` |
| `badge-marathon-member` | Marathon Member | `reunion-mensual` | 30 reuniones | `badge-marathon-member.png` |
| `badge-eternal-council` | Eternal Council | `reunion-mensual` | 35 reuniones | `badge-eternal-council.png` |

## Membresía — Aniversarios (`track: membresia-anios`, 10 niveles)

Sugerencia: escudo/anillo con el número de años. Paleta progresiva bronce→plata→oro→platino.

| Slug | Nombre | Track | Nivel (metricThreshold) | Archivo sugerido |
|------|--------|-------|-------------------------|-----------------|
| `badge-first-year` | First Year | `membresia-anios` | 1 año | `badge-first-year.png` |
| `badge-second-year` | Second Year | `membresia-anios` | 2 años | `badge-second-year.png` |
| `badge-third-year` | Third Year | `membresia-anios` | 3 años | `badge-third-year.png` |
| `badge-fourth-year` | Fourth Year | `membresia-anios` | 4 años | `badge-fourth-year.png` |
| `badge-fifth-year` | Fifth Year | `membresia-anios` | 5 años | `badge-fifth-year.png` |
| `badge-sixth-year` | Sixth Year | `membresia-anios` | 6 años | `badge-sixth-year.png` |
| `badge-seventh-year` | Seventh Year | `membresia-anios` | 7 años | `badge-seventh-year.png` |
| `badge-eighth-year` | Eighth Year | `membresia-anios` | 8 años | `badge-eighth-year.png` |
| `badge-ninth-year` | Ninth Year | `membresia-anios` | 9 años | `badge-ninth-year.png` |
| `badge-10-years` | A Decade at Makespace | `membresia-anios` | 10 años | `badge-10-years.png` |

## Eventos especiales pendientes

| Slug | Nombre | Nota | Archivo sugerido |
|------|--------|------|-----------------|
| `badge-evento-codemotion2025` | Codemotion 2025 | Ya existe `badge-codemotion-2026.png` para 2026; para 2025 falta imagen propia o reusar la de 2026 manualmente | `badge-codemotion-2025.png` |

## Máquinas sin badge en catálogo (imágenes ya disponibles)

Estas imágenes ya están en el repo pero no tienen badge en el catálogo del portal todavía.
Hay que crear el badge primero en el admin, luego referenciar la imagen.

| Imagen disponible | Badge sugerido |
|------------------|----------------|
| `badge-i-can-pcb.png` | `badge-i-can-pcb` — I Can PCB (fresadora de circuitos) |
| `badge-i-can-sew.png` | `badge-i-can-sew` — I Can Sew (máquina de coser) |
| `badge-i-can-sublimate.png` | `badge-i-can-sublimate` — I Can Sublimate (sublimación) |

---

**Total pendientes:** 42 imágenes (sin contar las máquinas sin badge en catálogo)
