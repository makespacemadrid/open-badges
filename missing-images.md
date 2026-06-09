# Badges sin imagen — pendientes de generar

Lista de badges del catálogo del portal que todavía no tienen imagen en este repositorio.
El nombre de archivo sugerido sigue la convención `badge-<slug>.png`.

Para actualizar la imagen en el portal una vez subida al repo, ejecutar desde el servidor:
```
npx prisma db seed
```
(El seed usa `applyBadgeCatalog` que asigna `imageUrl` automáticamente si la badge no tiene imagen.)

---

## Eventos — Hack the Space (`track: hack-the-space`, 9 niveles)

Sugerencia: iconografía de herramientas / taller con niveles de desgaste creciente.
Se pueden usar variantes del mismo diseño (bronce → plata → oro → …).

| Slug | Nombre | Sesiones (trackCountThreshold) | Archivo sugerido |
|------|--------|--------------------------------|-----------------|
| `badge-hackspace-immortal` | Hackspace Immortal | 35 | `badge-hackspace-immortal.png` |

## Eventos — Reunión mensual (`track: reunion-mensual`, 9 niveles)

Sugerencia: iconografía de asamblea / democracia participativa con niveles de antigüedad.

| Slug | Nombre | Reuniones (trackCountThreshold) | Archivo sugerido |
|------|--------|--------------------------------|-----------------|
| `badge-assembly-elder` | Assembly Elder | 20 | `badge-assembly-elder.png` |
| `badge-assembly-legend` | Assembly Legend | 25 | `badge-assembly-legend.png` |
| `badge-marathon-member` | Marathon Member | 30 | `badge-marathon-member.png` |
| `badge-eternal-council` | Eternal Council | 35 | `badge-eternal-council.png` |

## Eventos — Track de eventos externos (4 niveles)

Badges de participación en eventos externos de la comunidad tech. Slug base sin prefijo `badge-`.
Sugerencia: iconografía de networking / ponente con progresión de nivel.

| Slug | Nombre | Descripción | Quests del track | Archivo sugerido |
|------|--------|-------------|-----------------|-----------------|
| `eventos-primer-paso` | Primer Paso | Primer evento de la comunidad | 1 | `eventos-primer-paso.png` |
| `eventos-embajador` | Embajador | Representa a Makespace en eventos tech | 3 | `eventos-embajador.png` |
| `eventos-evangelista` | Evangelista | Referente en la difusión del Makespace | 5 | `eventos-evangelista.png` |
| `eventos-networker` | Networker Pro | Red de contactos sin límites | 10 | `eventos-networker.png` |

## Comunidad — Show & Tell

Sugerencia: iconografía de presentación / demostración (micrófono, pizarra, proyector).

| Slug | Nombre | Descripción | Archivo sugerido |
|------|--------|-------------|-----------------|
| `badge-show-and-tell` | Show & Tell | Impartir un taller o demostración en el Makespace | `badge-show-and-tell.png` |

## Membresía — Aniversarios (`track: membresia-anios`, 13 niveles)

Makespace Madrid abrió en abril de 2013. El máximo actual de antigüedad es 13 años.

Sugerencia: escudo/anillo con el número de años. Paleta progresiva bronce→plata→oro→platino→diamante.

| Slug | Nombre | Años (metricThreshold) | Archivo sugerido |
|------|--------|------------------------|-----------------|
| `badge-first-year` | First Year | 1 | `badge-first-year.png` |
| `badge-second-year` | Second Year | 2 | `badge-second-year.png` |
| `badge-third-year` | Third Year | 3 | `badge-third-year.png` |
| `badge-fourth-year` | Fourth Year | 4 | `badge-fourth-year.png` |
| `badge-fifth-year` | Fifth Year | 5 | `badge-fifth-year.png` |
| `badge-sixth-year` | Sixth Year | 6 | `badge-sixth-year.png` |
| `badge-seventh-year` | Seventh Year | 7 | `badge-seventh-year.png` |
| `badge-eighth-year` | Eighth Year | 8 | `badge-eighth-year.png` |
| `badge-ninth-year` | Ninth Year | 9 | `badge-ninth-year.png` |
| `badge-10-years` | A Decade at Makespace | 10 | `badge-10-years.png` |
| `badge-11-years` | Eleven Years | 11 | `badge-11-years.png` |
| `badge-12-years` | Twelve Years | 12 | `badge-12-years.png` |
| `badge-13-years` | Thirteen Years | 13 | `badge-13-years.png` |

## Membresía — Founding Member ⭐ (máximo nivel)

Badge especial para los mecenas del crowdfunding fundacional de Makespace Madrid (2012-2013).
**Concesión manual por admin** — no se desbloquea automáticamente.

Sugerencia de estética: diseño único y distinguible del resto, que evoque los orígenes del espacio.
Podría incluir el año "2013" o la fecha de apertura. Paleta dorada/especial diferente a los aniversarios.

| Slug | Nombre | Archivo sugerido |
|------|--------|-----------------|
| `badge-founding-member` | **Founding Member** | `badge-founding-member.png` |

---

**Total pendientes:** 25 imágenes
