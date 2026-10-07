# open-badges — Makespace Madrid

Repositorio de imágenes para los Open Badges de Makespace Madrid.

Las imágenes se sirven via **jsDelivr CDN**. Para invalidar la caché tras actualizar una imagen:

```
GET https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/<filename>
```

URL base del catálogo en el portal: `https://cdn.jsdelivr.net/gh/makespacemadrid/open-badges@main/`

## Qué hay aquí

- **`badge-*.png`** — las imágenes finales: 1254×1254 px, PNG con transparencia, disco de 1180 px.
- **[`missing-images.md`](missing-images.md)** — las que faltan, con la descripción de cada badge
  y la receta completa para generarla.
- **[`badges.yaml`](badges.yaml)** — el manifiesto: estilo global, itinerarios y una entrada por
  badge con su estado.
- **[`AGENTS.md`](AGENTS.md)** — empieza por aquí si eres un agente.

El catálogo de abajo, `missing-images.md` y `badges.yaml` **los escribe el portal**. No los edites
a mano: se sobreescriben en el siguiente push.

---

<!-- badgegen:tables:start -->
## Catálogo de badges

_Generado por el portal desde su base de datos (130 badges activos: 67 con imagen en este repo, 26 con imagen sólo en el portal, 37 por generar). Los pendientes, con su descripción y la receta de generación, están en [`missing-images.md`](missing-images.md)._

_El estado "en el repo" se comprueba contra el árbol de `main`, no contra la base de datos: un badge puede tener imagen en el portal y no estar respaldado aquí._

### Onboarding

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-hello-world` | Hello world! | `badge-hello-world.png` | ✅ en el repo |
| `badge-maker-101` | Maker101 | `badge-maker-101.png` | ⬆️ sin respaldar |
| `badge-padawan` | Padawan | `badge-padawan.png` | ✅ en el repo |

### Máquinas

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-can-cnc` | I Can CNC | `badge-can-cnc.png` | ⬆️ sin respaldar |
| `badge-i-can-carve` | I Can Carve | `badge-i-can-carve.png` | ✅ en el repo |
| `badge-i-can-cast` | I Can Cast | `badge-i-can-cast.png` | ✅ en el repo |
| `badge-i-can-dtf` | I Can DTF | `badge-i-can-dtf.png` | ❌ pendiente |
| `badge-i-can-laser` | I Can Laser | `badge-i-can-laser.png` | ⬆️ sin respaldar |
| `badge-i-can-pcb` | I Can PCB | `badge-i-can-pcb.png` | ✅ en el repo |
| `badge-i-can-print` | I Can Print (3D) | `badge-i-can-print.png` | ✅ en el repo |
| `badge-i-can-print-resin` | I Can Print (Resin) | `badge-i-can-print-resin.png` | ⬆️ sin respaldar |
| `badge-i-can-sew` | I Can Sew | `badge-i-can-sew.png` | ✅ en el repo |
| `badge-i-can-solder` | I Can Solder | `badge-i-can-solder.png` | ✅ en el repo |
| `badge-i-can-sublimate` | I Can Sublimate | `badge-i-can-sublimate.png` | ✅ en el repo |
| `badge-i-can-vinyl` | I Can Vinyl | `badge-i-can-vinyl.png` | ✅ en el repo |
| `badge-jack-of-all-trades` | Jack of all trades | `badge-jack-of-all-trades.png` | ⬆️ sin respaldar |
| `badge-macgyver` | MacGyver | `badge-macgyver.png` | ✅ en el repo |
| `badge-self-replicator` | Self-Replicator | `badge-self-replicator.png` | ✅ en el repo |
| `gcode-surgeon` | Gcode Surgeon | `badge-gcode-surgeon.png` | ❌ pendiente |

### Plataformas

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-archivist` | Archivist | `badge-archivist.png` | ✅ en el repo |
| `badge-burning-tokens` | Burning Tokens | `badge-burning-tokens.png` | ✅ en el repo |
| `badge-cake-is-a-lie` | The Cake Is a Lie | `badge-cake-is-a-lie.png` | ✅ en el repo |
| `badge-elevated-privileges` | Elevated Privileges | `badge-elevated-privileges.png` | 🚫 sirve 404 |
| `badge-first-draft` | First Draft | `badge-first-draft.png` | ✅ en el repo |
| `badge-first-queries` | First Queries | `badge-first-queries.png` | ✅ en el repo |
| `badge-gpu-melter` | GPU Melter | `badge-gpu-melter.png` | ✅ en el repo |
| `badge-guardian-of-knowledge` | Guardian of Knowledge | `badge-guardian-of-knowledge.png` | ⬆️ sin respaldar |
| `badge-hello-glados` | Hello GLaDOS | `badge-hello-glados.png` | ✅ en el repo |
| `badge-infinite-loop` | Infinite Loop | `badge-infinite-loop.png` | ✅ en el repo |
| `badge-property-of-aperture` | Property of Aperture | `badge-property-of-aperture.png` | ✅ en el repo |
| `badge-space-chronicler` | Space Chronicler | `badge-space-chronicler.png` | ✅ en el repo |
| `badge-still-alive` | Still Alive | `badge-still-alive.png` | ✅ en el repo |
| `badge-test-subject` | Test Subject | `badge-test-subject.png` | ✅ en el repo |
| `badge-token-collector` | Token Collector | `badge-token-collector.png` | ✅ en el repo |
| `badge-wiki-contributor` | Wiki Contributor | `badge-wiki-contributor.png` | ✅ en el repo |

### Comunidad

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-absolute-zero` | Absolute Zero | `badge-absolute-zero.png` | ❌ pendiente |
| `badge-all-nighter` | All-Nighter | `badge-all-nighter.png` | ❌ pendiente |
| `badge-chief-scout` | Chief Scout | `badge-chief-scout.png` | ❌ pendiente |
| `badge-cold-storage` | Cold Storage | `badge-cold-storage.png` | ❌ pendiente |
| `badge-compulsive-shopper` | Compulsive Shopper | `badge-compulsive-shopper.png` | ⬆️ sin respaldar |
| `badge-counselor` | Badge Counselor | `badge-counselor.png` | ❌ pendiente |
| `badge-cron-job` | Cron Job | `badge-cron-job.png` | ❌ pendiente |
| `badge-daemon-process` | Daemon Process | `badge-daemon-process.png` | ❌ pendiente |
| `badge-data-scrubber` | Data Scrubber | `badge-data-scrubber.png` | ✅ en el repo |
| `badge-demolition-man` | Demolition Man | `badge-demolition-man.png` | ✅ en el repo |
| `badge-dependency-injection` | Dependency Injection | `badge-dependency-injection.png` | ❌ pendiente |
| `badge-dont-feed-gremlins` | Don't Feed Them After Midnight | `badge-dont-feed-gremlins.png` | ✅ en el repo |
| `badge-early-bird` | Early Bird | `badge-early-bird.png` | ✅ en el repo |
| `badge-embajador-maker` | Space Ambassador | `badge-embajador-maker.png` | ⬆️ sin respaldar |
| `badge-garbage-collector` | Garbage Collector | `badge-garbage-collector.png` | ✅ en el repo |
| `badge-gotta-catch-em-all` | Gotta Catch 'Em All | `badge-gotta-catch-em-all.png` | ✅ en el repo |
| `badge-human-readme` | Human README | `badge-human-readme.png` | ❌ pendiente |
| `badge-hyperfocus` | Hyperfocus | `badge-hyperfocus.png` | ❌ pendiente |
| `badge-let-that-sink-in` | Let That Sink In | `badge-let-that-sink-in.png` | 🚫 sirve 404 |
| `badge-liquid-cooling` | Liquid Cooling Specialist | `badge-liquid-cooling.png` | ✅ en el repo |
| `badge-load-bearing-member` | Load-Bearing Member | `badge-load-bearing-member.png` | ❌ pendiente |
| `badge-man-makespace` | man makespace | `badge-man-makespace.png` | ❌ pendiente |
| `badge-mark-and-sweep` | Mark and Sweep | `badge-mark-and-sweep.png` | ❌ pendiente |
| `badge-master-minter` | Master Minter | `badge-master-minter.png` | ❌ pendiente |
| `badge-minter` | Minter | `badge-minter.png` | ❌ pendiente |
| `badge-onboarding-daemon` | Onboarding Daemon | `badge-onboarding-daemon.png` | ❌ pendiente |
| `badge-package-manager` | Package Manager | `badge-package-manager.png` | ❌ pendiente |
| `badge-petty-cash-rookie` | Petty Cash Rookie | `badge-petty-cash-rookie.png` | ⬆️ sin respaldar |
| `badge-platform-maker` | Platform Maker | `badge-platform-maker.png` | ✅ en el repo |
| `badge-procurer` | Procurer | `badge-procurer.png` | ⬆️ sin respaldar |
| `badge-sanitize-input` | Sanitize Input | `badge-sanitize-input.png` | ❌ pendiente |
| `badge-scoutmaster` | Scoutmaster | `badge-scoutmaster.png` | ❌ pendiente |
| `badge-secure-erase` | Secure Erase | `badge-secure-erase.png` | ❌ pendiente |
| `badge-serial-spender` | Serial Spender | `badge-serial-spender.png` | ⬆️ sin respaldar |
| `badge-show-and-tell` | Show & Tell | `badge-show-and-tell.png` | ⬆️ sin respaldar |
| `badge-spendzilla` | Spendzilla | `badge-spendzilla.png` | ⬆️ sin respaldar |
| `badge-sre` | Site Reliability Engineer | `badge-sre.png` | ❌ pendiente |
| `badge-stack-overflow` | Stack Overflow | `badge-stack-overflow.png` | ✅ en el repo |
| `badge-stop-the-world` | Stop the World | `badge-stop-the-world.png` | ❌ pendiente |
| `badge-supply-chain-exploit` | Supply Chain Exploit | `badge-supply-chain-exploit.png` | ⬆️ sin respaldar |
| `badge-tetris-master` | Tetris Master | `badge-tetris-master.png` | ✅ en el repo |
| `badge-the-great-flood` | The Great Flood | `badge-the-great-flood.png` | ⬆️ sin respaldar |
| `badge-uptime-99` | Uptime 99.9% | `badge-uptime-99.png` | ❌ pendiente |

### Eventos

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-assembly-elder` | Assembly Elder | `badge-assembly-elder.png` | ⬆️ sin respaldar |
| `badge-assembly-legend` | Assembly Legend | `badge-assembly-legend.png` | ⬆️ sin respaldar |
| `badge-assembly-regular` | Assembly Regular | `badge-assembly-regular.png` | ✅ en el repo |
| `badge-been-there` | Been there, done that | `badge-been-there.png` | ✅ en el repo |
| `badge-community-pillar` | Community Pillar | `badge-community-pillar.png` | ✅ en el repo |
| `badge-community-veteran` | Community Veteran | `badge-community-veteran.png` | ✅ en el repo |
| `badge-council-member` | Council Member | `badge-council-member.png` | ✅ en el repo |
| `badge-ctf-v1` | Capture the Flag v1 | `badge-ctf-v1.png` | ✅ en el repo |
| `badge-eternal-council` | Eternal Council | `badge-eternal-council.png` | ❌ pendiente |
| `badge-evento-aniversario2026` | Aniversario 2026 (6+7 años) | `badge-evento-aniversario2026.png` | ⬆️ sin respaldar |
| `badge-evento-codemotion2026` | Codemotion 2026 | `badge-evento-codemotion2026.png` | ⬆️ sin respaldar |
| `badge-evento-nerdearla2025` | Nerdearla 2025 | `badge-evento-nerdearla2025.png` | ⬆️ sin respaldar |
| `badge-first-assembly` | First Assembly | `badge-first-assembly.png` | ✅ en el repo |
| `badge-first-hack` | First Hack | `badge-first-hack.png` | ✅ en el repo |
| `badge-hackspace-elder` | Hackspace Elder | `badge-hackspace-elder.png` | ✅ en el repo |
| `badge-hackspace-hero` | Hackspace Hero | `badge-hackspace-hero.png` | ✅ en el repo |
| `badge-hackspace-immortal` | Hackspace Immortal | `badge-hackspace-immortal.png` | ⬆️ sin respaldar |
| `badge-hackspace-legend` | Hackspace Legend | `badge-hackspace-legend.png` | ✅ en el repo |
| `badge-hackspace-veteran` | Hackspace Veteran | `badge-hackspace-veteran.png` | ✅ en el repo |
| `badge-hammer-time` | Hammer Time | `badge-hammer-time.png` | ✅ en el repo |
| `badge-hot-pot` | Too hot to handle | `badge-hot-pot.png` | ⬆️ sin respaldar |
| `badge-marathon-member` | Marathon Member | `badge-marathon-member.png` | ❌ pendiente |
| `badge-master-hacker` | Master Hacker | `badge-master-hacker.png` | ✅ en el repo |
| `badge-space-regular` | Space Regular | `badge-space-regular.png` | ✅ en el repo |
| `eventos-embajador` | Roadie | `badge-eventos-embajador.png` | ⬆️ sin respaldar |
| `eventos-evangelista` | Headliner | `badge-eventos-evangelista.png` | ⬆️ sin respaldar |
| `eventos-networker` | Tour Manager | `badge-eventos-networker.png` | ❌ pendiente |
| `eventos-primer-paso` | Groupie | `badge-eventos-primer-paso.png` | ⬆️ sin respaldar |

### Membresía

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `badge-10-years` | A Decade at Makespace | `badge-10-years.png` | ✅ en el repo |
| `badge-11-years` | Eleven Years | `badge-11-years.png` | ✅ en el repo |
| `badge-12-years` | Twelve Years | `badge-12-years.png` | ✅ en el repo |
| `badge-13-years` | Thirteen Years | `badge-13-years.png` | ✅ en el repo |
| `badge-eighth-year` | Eighth Year | `badge-eighth-year.png` | ✅ en el repo |
| `badge-fifth-year` | Fifth Year | `badge-fifth-year.png` | ✅ en el repo |
| `badge-first-year` | First Year | `badge-first-year.png` | ✅ en el repo |
| `badge-founding-member` | Founding Member | `badge-founding-member.png` | ⬆️ sin respaldar |
| `badge-fourth-year` | Fourth Year | `badge-fourth-year.png` | ✅ en el repo |
| `badge-level-18` | Level 18 Unlocked | `badge-level-18.png` | ✅ en el repo |
| `badge-miembro-makespace` | Makespace Member | `badge-miembro-makespace.png` | ✅ en el repo |
| `badge-ninth-year` | Ninth Year | `badge-ninth-year.png` | ✅ en el repo |
| `badge-second-year` | Second Year | `badge-second-year.png` | ✅ en el repo |
| `badge-seventh-year` | Seventh Year | `badge-seventh-year.png` | ✅ en el repo |
| `badge-sixth-year` | Sixth Year | `badge-sixth-year.png` | ✅ en el repo |
| `badge-third-year` | Third Year | `badge-third-year.png` | ✅ en el repo |
| `keys-of-kingdom` | Keys of Kingdom | `badge-keys-of-kingdom.png` | ✅ en el repo |
| `maker-level-2-oficial` | Oficial | `badge-maker-level-2-oficial.png` | ❌ pendiente |
| `maker-level-3-artesano` | Artesano | `badge-maker-level-3-artesano.png` | ❌ pendiente |
| `maker-level-4-maestro` | Maestro | `badge-maker-level-4-maestro.png` | ❌ pendiente |
| `maker-level-5-virtuoso` | Virtuoso | `badge-maker-level-5-virtuoso.png` | ❌ pendiente |
| `maker-level-6-gran-maestro` | Gran Maestro | `badge-maker-level-6-gran-maestro.png` | ❌ pendiente |
| `maker-level-7-leyenda` | Leyenda | `badge-maker-level-7-leyenda.png` | ❌ pendiente |

### Otros

| Slug | Nombre | Imagen | Estado |
|------|--------|--------|--------|
| `for-i-am-here` | For I am here | `badge-for-i-am-here.png` | ❌ pendiente |
<!-- badgegen:tables:end -->

