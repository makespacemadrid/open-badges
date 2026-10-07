# Imágenes de badges pendientes

_Generado por el portal el 2026-10-07. **No editar a mano**: se reescribe completo en cada sincronización. Los datos de cada badge vienen de la base de datos del portal y están también, en formato máquina, en [`badges.yaml`](badges.yaml)._

Faltan **37** imágenes de **130** badges activos (2 sirven un 404 ahora mismo, 35 sin imagen).

## Cómo generar una imagen

### 1. Prompt

El portal compone el prompt juntando estas líneas con saltos de línea, en este orden:

```
<estilo>
Badge title text (must appear exactly): "<nombre del badge>"
Main motif: <pista visual, o la descripción si no hay pista>
<instrucción extra del itinerario, si la hay>
<instrucción extra del badge, si la hay>
<reglas duras>
```

El **estilo** en vigor (`style` en `badges.yaml`):

> Circular maker badge emblem, flat vector style, golden yellow (#F5C400) artwork on a black disc, outer yellow ring with small screw heads, bold sans-serif lettering, high contrast, clean centered composition, no gradients, no photo textures

Las **reglas duras**, literales y no negociables:

> Hard requirements: the badge is a PERFECT CIRCLE (never an ellipse or squashed disc), fully visible and centered with margin around it, on a plain solid black background with nothing else in the frame. Any text must be spelled EXACTLY as given, fully legible, with clean unbroken letterforms. The title appears exactly ONCE, at the top of the badge.

Imágenes de referencia globales (ficheros de este repo, pásalas al modelo si puede: `badge:badge-space-regular`, `badge:badge-miembro-makespace`, `badge:badge-hello-glados`).

### 2. El fichero final

- PNG de **1254×1254** px con **canal alfa**.
- El disco del badge, centrado, de **1180** px de diámetro; todo lo de fuera del círculo, transparente.
- Circularidad mínima **0.985** (área del disco sobre el área del círculo que lo circunscribe). El portal rechaza por debajo de **0.93** incluso tras reencuadrar.
- El título debe aparecer **una sola vez**, arriba, escrito exactamente igual que en "Título que debe aparecer en la imagen".

Si generas sobre fondo negro (lo que piden las reglas duras), recorta el disco y pégalo centrado en un lienzo transparente antes de guardar — es lo que hace el portal. Los defectos que detecta su control de calidad son: `wrong-size` (no es 1254×1254), `no-transparency` (sin alfa), `empty-image` (lienzo vacío) y `flattened-circle` (elipse).

### 3. Entrega

1. Commitea el PNG en la raíz de este repo con **exactamente** el nombre de "Fichero a crear". El nombre no es decorativo: el portal busca el badge por ese nombre y un typo deja el badge sirviendo un 404.
2. Purga la caché de jsDelivr: `curl https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/<fichero>`.
3. Avisa a un owner del portal para que suba la imagen al badge. Commitear aquí **no** le da la imagen al badge por sí solo: el portal sirve su propia copia y sólo usa la URL de este repo cuando el badge no tiene ninguna imagen.

## Pendientes

| Slug | Fichero | Estado |
|------|---------|--------|
| [`badge-absolute-zero`](#badge-absolute-zero--absolute-zero) | `badge-absolute-zero.png` | ❌ pendiente |
| [`badge-all-nighter`](#badge-all-nighter--all-nighter) | `badge-all-nighter.png` | ❌ pendiente |
| [`badge-chief-scout`](#badge-chief-scout--chief-scout) | `badge-chief-scout.png` | ❌ pendiente |
| [`badge-cold-storage`](#badge-cold-storage--cold-storage) | `badge-cold-storage.png` | ❌ pendiente |
| [`badge-counselor`](#badge-counselor--badge-counselor) | `badge-counselor.png` | ❌ pendiente |
| [`badge-cron-job`](#badge-cron-job--cron-job) | `badge-cron-job.png` | ❌ pendiente |
| [`badge-daemon-process`](#badge-daemon-process--daemon-process) | `badge-daemon-process.png` | ❌ pendiente |
| [`badge-dependency-injection`](#badge-dependency-injection--dependency-injection) | `badge-dependency-injection.png` | ❌ pendiente |
| [`badge-elevated-privileges`](#badge-elevated-privileges--elevated-privileges) | `badge-elevated-privileges.png` | 🚫 sirve 404 |
| [`badge-eternal-council`](#badge-eternal-council--eternal-council) | `badge-eternal-council.png` | ❌ pendiente |
| [`badge-human-readme`](#badge-human-readme--human-readme) | `badge-human-readme.png` | ❌ pendiente |
| [`badge-hyperfocus`](#badge-hyperfocus--hyperfocus) | `badge-hyperfocus.png` | ❌ pendiente |
| [`badge-i-can-dtf`](#badge-i-can-dtf--i-can-dtf) | `badge-i-can-dtf.png` | ❌ pendiente |
| [`badge-let-that-sink-in`](#badge-let-that-sink-in--let-that-sink-in) | `badge-let-that-sink-in.png` | 🚫 sirve 404 |
| [`badge-load-bearing-member`](#badge-load-bearing-member--load-bearing-member) | `badge-load-bearing-member.png` | ❌ pendiente |
| [`badge-man-makespace`](#badge-man-makespace--man-makespace) | `badge-man-makespace.png` | ❌ pendiente |
| [`badge-marathon-member`](#badge-marathon-member--marathon-member) | `badge-marathon-member.png` | ❌ pendiente |
| [`badge-mark-and-sweep`](#badge-mark-and-sweep--mark-and-sweep) | `badge-mark-and-sweep.png` | ❌ pendiente |
| [`badge-master-minter`](#badge-master-minter--master-minter) | `badge-master-minter.png` | ❌ pendiente |
| [`badge-minter`](#badge-minter--minter) | `badge-minter.png` | ❌ pendiente |
| [`badge-onboarding-daemon`](#badge-onboarding-daemon--onboarding-daemon) | `badge-onboarding-daemon.png` | ❌ pendiente |
| [`badge-package-manager`](#badge-package-manager--package-manager) | `badge-package-manager.png` | ❌ pendiente |
| [`badge-sanitize-input`](#badge-sanitize-input--sanitize-input) | `badge-sanitize-input.png` | ❌ pendiente |
| [`badge-scoutmaster`](#badge-scoutmaster--scoutmaster) | `badge-scoutmaster.png` | ❌ pendiente |
| [`badge-secure-erase`](#badge-secure-erase--secure-erase) | `badge-secure-erase.png` | ❌ pendiente |
| [`badge-sre`](#badge-sre--site-reliability-engineer) | `badge-sre.png` | ❌ pendiente |
| [`badge-stop-the-world`](#badge-stop-the-world--stop-the-world) | `badge-stop-the-world.png` | ❌ pendiente |
| [`badge-uptime-99`](#badge-uptime-99--uptime-999) | `badge-uptime-99.png` | ❌ pendiente |
| [`eventos-networker`](#eventos-networker--tour-manager) | `badge-eventos-networker.png` | ❌ pendiente |
| [`for-i-am-here`](#for-i-am-here--for-i-am-here) | `badge-for-i-am-here.png` | ❌ pendiente |
| [`gcode-surgeon`](#gcode-surgeon--gcode-surgeon) | `badge-gcode-surgeon.png` | ❌ pendiente |
| [`maker-level-2-oficial`](#maker-level-2-oficial--oficial) | `badge-maker-level-2-oficial.png` | ❌ pendiente |
| [`maker-level-3-artesano`](#maker-level-3-artesano--artesano) | `badge-maker-level-3-artesano.png` | ❌ pendiente |
| [`maker-level-4-maestro`](#maker-level-4-maestro--maestro) | `badge-maker-level-4-maestro.png` | ❌ pendiente |
| [`maker-level-5-virtuoso`](#maker-level-5-virtuoso--virtuoso) | `badge-maker-level-5-virtuoso.png` | ❌ pendiente |
| [`maker-level-6-gran-maestro`](#maker-level-6-gran-maestro--gran-maestro) | `badge-maker-level-6-gran-maestro.png` | ❌ pendiente |
| [`maker-level-7-leyenda`](#maker-level-7-leyenda--leyenda) | `badge-maker-level-7-leyenda.png` | ❌ pendiente |

## Máquinas

### `badge-i-can-dtf` — I Can DTF

- **Fichero a crear**: `badge-i-can-dtf.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `I Can DTF`
- **Categoría**: maquinas

**Motivo del badge** (lo que se le cuenta al socio):

> Ha hecho su primera transferencia DTF en el Makespace: film, polvo de poliamida, curado y prensa. Ahora puede estampar también sobre algodón y sobre prendas oscuras.

**Criterios para conseguirlo**:

> Completar la primera transferencia DTF con el equipo del Makespace.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `gcode-surgeon` — Gcode Surgeon

- **Fichero a crear**: `badge-gcode-surgeon.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Gcode Surgeon`
- **Categoría**: maquinas

**Motivo del badge** (lo que se le cuenta al socio):

> Habilidad para salvar impresiones 3D mediante la edición manual del archivo G-Code cuando una maquina se queda atascada en una impresión de muchas horas

**Criterios para conseguirlo**:

> Demostrar conocimiento profundo sobre las impresoras y el funcionamiento del código G-Code mediante la corrección manual del  archivo de impresión.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

## Plataformas

### `badge-elevated-privileges` — Elevated Privileges

- **Fichero a crear**: `badge-elevated-privileges.png`
- **Estado**: 🚫 sirve 404
- **Título que debe aparecer en la imagen**: `Elevated Privileges`
- **Categoría**: plataformas
- **⚠️ Urgente**: el portal sirve `https://cdn.jsdelivr.net/gh/makespacemadrid/open-badges@main/badge-elevated-privileges.png`, que es un 404. Este badge se ve roto para los socios ahora mismo.

**Motivo del badge** (lo que se le cuenta al socio):

> Autoaloja su propio equipo en el datacenter escalable del Makespace.

**Criterios para conseguirlo**:

> Instalar y mantener un equipo propio en el datacenter del altillo.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

## Comunidad

### `badge-absolute-zero` — Absolute Zero

- **Fichero a crear**: `badge-absolute-zero.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Absolute Zero`
- **Categoría**: comunidad
- **Itinerario**: `chore-nevera` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Quince recargas. La nevera nunca ha estado vacía por su culpa.

**Criterios para conseguirlo**:

> Completar el reto «Recarga la nevera comunitaria» 15 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-all-nighter` — All-Nighter

- **Fichero a crear**: `badge-all-nighter.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `All-Nighter`
- **Categoría**: comunidad
- **Itinerario**: `nocturnidad` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha pasado la noche entera en el espacio y ha visto amanecer desde dentro. No durmió: iteró.

**Criterios para conseguirlo**:

> Permanecer en el Makespace de forma continuada desde antes de la medianoche hasta después del amanecer.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-chief-scout` — Chief Scout

- **Fichero a crear**: `badge-chief-scout.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Chief Scout`
- **Categoría**: comunidad
- **Itinerario**: `minter` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Jefe Scout supremo — 50 insignias acuñadas. La fábrica eres tú.

**Criterios para conseguirlo**:

> Propón 50 insignias para la comunidad. Cuentan tanto las propuestas de socio (desde «Tu progreso» o el asistente de chat) como las insignias creadas desde el panel de administración.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-cold-storage` — Cold Storage

- **Fichero a crear**: `badge-cold-storage.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Cold Storage`
- **Categoría**: comunidad
- **Itinerario**: `chore-nevera` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha recargado la nevera cinco veces. La bebida fría no aparece sola.

**Criterios para conseguirlo**:

> Completar el reto «Recarga la nevera comunitaria» 5 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-counselor` — Badge Counselor

- **Fichero a crear**: `badge-counselor.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Badge Counselor`
- **Categoría**: comunidad
- **Itinerario**: `minter` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Un consejero experimentado en la creación de insignias.

**Criterios para conseguirlo**:

> Propón 5 insignias para la comunidad. Cuentan tanto las propuestas de socio (desde «Tu progreso» o el asistente de chat) como las insignias creadas desde el panel de administración.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-cron-job` — Cron Job

- **Fichero a crear**: `badge-cron-job.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Cron Job`
- **Categoría**: comunidad
- **Itinerario**: `cuidado-espacio` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tres tareas de mantenimiento. Ya no es casualidad: es una rutina.

**Criterios para conseguirlo**:

> Completar 3 tareas de mantenimiento del espacio (basura, baños, nevera, materiales o tours).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-daemon-process` — Daemon Process

- **Fichero a crear**: `badge-daemon-process.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Daemon Process`
- **Categoría**: comunidad
- **Itinerario**: `cuidado-espacio` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Cinco tareas de mantenimiento, de las que se hacen sin que nadie las pida.

**Criterios para conseguirlo**:

> Completar 5 tareas de mantenimiento del espacio (basura, baños, nevera, materiales o tours).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-dependency-injection` — Dependency Injection

- **Fichero a crear**: `badge-dependency-injection.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Dependency Injection`
- **Categoría**: comunidad
- **Itinerario**: `chore-materiales` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha traído material cinco veces. Resuelve las dependencias del espacio.

**Criterios para conseguirlo**:

> Completar el reto «Trae material para el espacio» 5 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-human-readme` — Human README

- **Fichero a crear**: `badge-human-readme.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Human README`
- **Categoría**: comunidad
- **Itinerario**: `chore-tour` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Quince tours. Si no sabes cómo funciona algo del espacio, pregúntale.

**Criterios para conseguirlo**:

> Completar el reto «Da un tour del espacio a visitantes» 15 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-hyperfocus` — Hyperfocus

- **Fichero a crear**: `badge-hyperfocus.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Hyperfocus`
- **Categoría**: comunidad
- **Itinerario**: `nocturnidad` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> En un arrebato de creatividad (o de pura cabezonería) se quedó tan absorto en el problema que se le olvidó qué hora era… y cenar.

**Criterios para conseguirlo**:

> Cerrar el Makespace pasadas las 3 de la madrugada.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-let-that-sink-in` — Let That Sink In

- **Fichero a crear**: `badge-let-that-sink-in.png`
- **Estado**: 🚫 sirve 404
- **Título que debe aparecer en la imagen**: `Let That Sink In`
- **Categoría**: comunidad
- **⚠️ Urgente**: el portal sirve `https://cdn.jsdelivr.net/gh/makespacemadrid/open-badges@main/badge-let-that-sink-in.png`, que es un 404. Este badge se ve roto para los socios ahora mismo.

**Motivo del badge** (lo que se le cuenta al socio):

> Ha instalado, desinstalado o arreglado un fregadero del Makespace.

**Criterios para conseguirlo**:

> Instalar, desinstalar o reparar un fregadero del espacio.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-load-bearing-member` — Load-Bearing Member

- **Fichero a crear**: `badge-load-bearing-member.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Load-Bearing Member`
- **Categoría**: comunidad
- **Itinerario**: `cuidado-espacio` (nivel 25) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Veinticinco tareas de mantenimiento. Como esa dependencia del xkcd 2347 que sostiene medio internet.

**Criterios para conseguirlo**:

> Completar 25 tareas de mantenimiento del espacio (basura, baños, nevera, materiales o tours).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-man-makespace` — man makespace

- **Fichero a crear**: `badge-man-makespace.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `man makespace`
- **Categoría**: comunidad
- **Itinerario**: `chore-tour` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha enseñado el espacio a alguien que venía por primera vez.

**Criterios para conseguirlo**:

> Completar el reto «Da un tour del espacio a visitantes» 1 vez.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-mark-and-sweep` — Mark and Sweep

- **Fichero a crear**: `badge-mark-and-sweep.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Mark and Sweep`
- **Categoría**: comunidad
- **Itinerario**: `chore-basura` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha sacado la basura cinco veces. Recolección periódica y fiable.

**Criterios para conseguirlo**:

> Completar el reto «Saca la basura del espacio» 5 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-master-minter` — Master Minter

- **Fichero a crear**: `badge-master-minter.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Master Minter`
- **Categoría**: comunidad
- **Itinerario**: `minter` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Maestro acuñador — 15 insignias y subiendo.

**Criterios para conseguirlo**:

> Propón 15 insignias para la comunidad. Cuentan tanto las propuestas de socio (desde «Tu progreso» o el asistente de chat) como las insignias creadas desde el panel de administración.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-minter` — Minter

- **Fichero a crear**: `badge-minter.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Minter`
- **Categoría**: comunidad
- **Itinerario**: `minter` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha acuñado su primera insignia en la plataforma.

**Criterios para conseguirlo**:

> Propón 1 insignia para la comunidad. Cuentan tanto las propuestas de socio (desde «Tu progreso» o el asistente de chat) como las insignias creadas desde el panel de administración.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-onboarding-daemon` — Onboarding Daemon

- **Fichero a crear**: `badge-onboarding-daemon.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Onboarding Daemon`
- **Categoría**: comunidad
- **Itinerario**: `chore-tour` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Cinco tours. Siempre en segundo plano, siempre atendiendo a quien llega.

**Criterios para conseguirlo**:

> Completar el reto «Da un tour del espacio a visitantes» 5 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-package-manager` — Package Manager

- **Fichero a crear**: `badge-package-manager.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Package Manager`
- **Categoría**: comunidad
- **Itinerario**: `chore-materiales` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Quince viajes de material. Mantiene el inventario del espacio al día.

**Criterios para conseguirlo**:

> Completar el reto «Trae material para el espacio» 15 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-sanitize-input` — Sanitize Input

- **Fichero a crear**: `badge-sanitize-input.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Sanitize Input`
- **Categoría**: comunidad
- **Itinerario**: `chore-banos` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Ha limpiado los baños cinco veces. Un trabajo que nadie ve y todos agradecen.

**Criterios para conseguirlo**:

> Completar el reto «Limpia los baños del Makespace» 5 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-scoutmaster` — Scoutmaster

- **Fichero a crear**: `badge-scoutmaster.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Scoutmaster`
- **Categoría**: comunidad
- **Itinerario**: `minter` (nivel 4) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Líder de tropa: ha creado 30 insignias para la comunidad.

**Criterios para conseguirlo**:

> Propón 30 insignias para la comunidad. Cuentan tanto las propuestas de socio (desde «Tu progreso» o el asistente de chat) como las insignias creadas desde el panel de administración.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-secure-erase` — Secure Erase

- **Fichero a crear**: `badge-secure-erase.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Secure Erase`
- **Categoría**: comunidad
- **Itinerario**: `chore-banos` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Quince limpiezas. No queda rastro de lo que había.

**Criterios para conseguirlo**:

> Completar el reto «Limpia los baños del Makespace» 15 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-sre` — Site Reliability Engineer

- **Fichero a crear**: `badge-sre.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Site Reliability Engineer`
- **Categoría**: comunidad
- **Itinerario**: `cuidado-espacio` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Quince tareas. Mantener esto en marcha es, oficialmente, lo suyo.

**Criterios para conseguirlo**:

> Completar 15 tareas de mantenimiento del espacio (basura, baños, nevera, materiales o tours).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-stop-the-world` — Stop the World

- **Fichero a crear**: `badge-stop-the-world.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Stop the World`
- **Categoría**: comunidad
- **Itinerario**: `chore-basura` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Quince veces. Cuando esta persona recoge, no queda una bolsa en pie.

**Criterios para conseguirlo**:

> Completar el reto «Saca la basura del espacio» 15 veces.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-uptime-99` — Uptime 99.9%

- **Fichero a crear**: `badge-uptime-99.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Uptime 99.9%`
- **Categoría**: comunidad
- **Itinerario**: `cuidado-espacio` (nivel 10) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Diez tareas de mantenimiento. El espacio funciona porque hay gente así.

**Criterios para conseguirlo**:

> Completar 10 tareas de mantenimiento del espacio (basura, baños, nevera, materiales o tours).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

## Eventos

### `badge-eternal-council` — Eternal Council

- **Fichero a crear**: `badge-eternal-council.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Eternal Council`
- **Categoría**: eventos
- **Itinerario**: `reunion-mensual` (nivel 35) — ver `tracks` en `badges.yaml`
- **Instrucción extra para el prompt**: Top level (35) of the monthly-assembly attendance ladder. The most solemn and ornate of the family shown in the reference badges.
- **Imágenes de referencia**: `badge:badge-marathon-member`, `badge:badge-assembly-legend`

**Motivo del badge** (lo que se le cuenta al socio):

> 35 reuniones. Has sobrevivido a tres presidentes y dos proyectores.

**Criterios para conseguirlo**:

> Asistir a 35 reuniones mensuales.

**Pista visual** (úsala como motivo principal): a round council table seen from above with an ouroboros ring engraved around it

### `badge-marathon-member` — Marathon Member

- **Fichero a crear**: `badge-marathon-member.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Marathon Member`
- **Categoría**: eventos
- **Itinerario**: `reunion-mensual` (nivel 30) — ver `tracks` en `badges.yaml`
- **Instrucción extra para el prompt**: Level 30 of the monthly-assembly attendance ladder (above Assembly Legend). Same family as the reference badges, even more ornate.
- **Imágenes de referencia**: `badge:badge-assembly-legend`, `badge:badge-assembly-elder`

**Motivo del badge** (lo que se le cuenta al socio):

> 30 reuniones mensuales. Paciencia, dedicación y un historial de asistencia impecable.

**Criterios para conseguirlo**:

> Asistir a 30 reuniones mensuales.

**Pista visual** (úsala como motivo principal): a runner crossing a finish line tape strung between two meeting chairs

### `eventos-networker` — Tour Manager

- **Fichero a crear**: `badge-eventos-networker.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Tour Manager`
- **Categoría**: eventos
- **Itinerario**: `track-eventos` (nivel 10) — ver `tracks` en `badges.yaml`
- **Instrucción extra para el prompt**: Level 4 of 4 in the events badge series (concert tour theme: Groupie, Roadie, Headliner, Tour Manager). Same style family as the reference badge; ornamentation grows with the level.
- **Imágenes de referencia**: `badge:eventos-evangelista`, `badge:eventos-primer-paso`

**Motivo del badge** (lo que se le cuenta al socio):

> Te pateas la gira entera de eventos — no hay stand sin ti.

**Criterios para conseguirlo**:

> Completa 10 quests del track de eventos.

**Pista visual** (úsala como motivo principal): a clipboard with a tour route map and a laminated all-access pass

## Membresía

### `maker-level-2-oficial` — Oficial

- **Fichero a crear**: `badge-maker-level-2-oficial.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Oficial`
- **Categoría**: membresia

**Motivo del badge** (lo que se le cuenta al socio):

> Nivel 2 del camino del Maker. Tus primeras insignias en el zurrón.

**Criterios para conseguirlo**:

> Reunir 2 insignias activas en el Makespace Madrid.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `maker-level-3-artesano` — Artesano

- **Fichero a crear**: `badge-maker-level-3-artesano.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Artesano`
- **Categoría**: membresia

**Motivo del badge** (lo que se le cuenta al socio):

> Nivel 3 del camino del Maker. Ya tienes oficio propio.

**Criterios para conseguirlo**:

> Reunir 6 insignias activas en el Makespace Madrid.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `maker-level-4-maestro` — Maestro

- **Fichero a crear**: `badge-maker-level-4-maestro.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Maestro`
- **Categoría**: membresia

**Motivo del badge** (lo que se le cuenta al socio):

> Nivel 4 del camino del Maker. Dominas varias artes del taller.

**Criterios para conseguirlo**:

> Reunir 14 insignias activas en el Makespace Madrid.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `maker-level-5-virtuoso` — Virtuoso

- **Fichero a crear**: `badge-maker-level-5-virtuoso.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Virtuoso`
- **Categoría**: membresia

**Motivo del badge** (lo que se le cuenta al socio):

> Nivel 5 del camino del Maker. Tu obra habla por ti.

**Criterios para conseguirlo**:

> Reunir 27 insignias activas en el Makespace Madrid.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `maker-level-6-gran-maestro` — Gran Maestro

- **Fichero a crear**: `badge-maker-level-6-gran-maestro.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Gran Maestro`
- **Categoría**: membresia

**Motivo del badge** (lo que se le cuenta al socio):

> Nivel 6 del camino del Maker. Referente del taller.

**Criterios para conseguirlo**:

> Reunir 44 insignias activas en el Makespace Madrid.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `maker-level-7-leyenda` — Leyenda

- **Fichero a crear**: `badge-maker-level-7-leyenda.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Leyenda`
- **Categoría**: membresia

**Motivo del badge** (lo que se le cuenta al socio):

> Nivel 7 del camino del Maker. Tu nombre es historia del espacio.

**Criterios para conseguirlo**:

> Reunir 65 insignias activas en el Makespace Madrid.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

## Otros

### `for-i-am-here` — For I am here

- **Fichero a crear**: `badge-for-i-am-here.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `For I am here`

**Motivo del badge** (lo que se le cuenta al socio):

> En un mundo repleto de máquinas complejas, programas obtusos y herramientas extrañas, sé el símbolo de la esperanza de alguien y pasa la llama.

**Criterios para conseguirlo**:

> Ayuda a alguien a usar una herramienta, programa o máquina del espacio.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

## Con imagen en el portal pero sin respaldar aquí

26 badges tienen su imagen en el portal y no en este repo (se subieron a mano o se importaron sin pasar por la sincronización). No hay nada que generar: los recupera el portal en su próxima pasada de backup.

| Slug | Fichero esperado |
|------|------------------|
| `badge-assembly-elder` | `badge-assembly-elder.png` |
| `badge-assembly-legend` | `badge-assembly-legend.png` |
| `badge-can-cnc` | `badge-can-cnc.png` |
| `badge-compulsive-shopper` | `badge-compulsive-shopper.png` |
| `badge-embajador-maker` | `badge-embajador-maker.png` |
| `badge-evento-aniversario2026` | `badge-evento-aniversario2026.png` |
| `badge-evento-codemotion2026` | `badge-evento-codemotion2026.png` |
| `badge-evento-nerdearla2025` | `badge-evento-nerdearla2025.png` |
| `badge-founding-member` | `badge-founding-member.png` |
| `badge-guardian-of-knowledge` | `badge-guardian-of-knowledge.png` |
| `badge-hackspace-immortal` | `badge-hackspace-immortal.png` |
| `badge-hot-pot` | `badge-hot-pot.png` |
| `badge-i-can-laser` | `badge-i-can-laser.png` |
| `badge-i-can-print-resin` | `badge-i-can-print-resin.png` |
| `badge-jack-of-all-trades` | `badge-jack-of-all-trades.png` |
| `badge-maker-101` | `badge-maker-101.png` |
| `badge-petty-cash-rookie` | `badge-petty-cash-rookie.png` |
| `badge-procurer` | `badge-procurer.png` |
| `badge-serial-spender` | `badge-serial-spender.png` |
| `badge-show-and-tell` | `badge-show-and-tell.png` |
| `badge-spendzilla` | `badge-spendzilla.png` |
| `badge-supply-chain-exploit` | `badge-supply-chain-exploit.png` |
| `badge-the-great-flood` | `badge-the-great-flood.png` |
| `eventos-embajador` | `badge-eventos-embajador.png` |
| `eventos-evangelista` | `badge-eventos-evangelista.png` |
| `eventos-primer-paso` | `badge-eventos-primer-paso.png` |