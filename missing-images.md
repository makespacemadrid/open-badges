# Imágenes de badges pendientes

_Generado por el portal el 2026-10-22. **No editar a mano**: se reescribe completo en cada sincronización. Los datos de cada badge vienen de la base de datos del portal y están también, en formato máquina, en [`badges.yaml`](badges.yaml)._

Faltan **28** imágenes de **159** badges activos.

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
3. Nada más. El portal sincroniza este repo cada hora: en la siguiente pasada descarga el PNG, lo adopta como imagen del badge y actualiza esta lista. Si el badge está marcado **⚠️ Urgente** (sirve un 404 ahora mismo), el purgado del paso 2 lo arregla en el momento sin esperar a la sincronización.

## Pendientes

| Slug | Fichero | Estado |
|------|---------|--------|
| [`badge-beam-buddy`](#badge-beam-buddy--beam-buddy) | `badge-beam-buddy.png` | ❌ pendiente |
| [`badge-beam-operator`](#badge-beam-operator--beam-operator) | `badge-beam-operator.png` | ❌ pendiente |
| [`badge-bed-leveler`](#badge-bed-leveler--the-bed-leveler) | `badge-bed-leveler.png` | ❌ pendiente |
| [`badge-color-duo`](#badge-color-duo--color-duo) | `badge-color-duo.png` | ❌ pendiente |
| [`badge-cut-specialist`](#badge-cut-specialist--cut-specialist) | `badge-cut-specialist.png` | ❌ pendiente |
| [`badge-day-job`](#badge-day-job--day-job) | `badge-day-job.png` | ❌ pendiente |
| [`badge-epic-print`](#badge-epic-print--epic-print) | `badge-epic-print.png` | ❌ pendiente |
| [`badge-extrusion-legend`](#badge-extrusion-legend--extrusion-legend) | `badge-extrusion-legend.png` | ❌ pendiente |
| [`badge-filament-whisperer`](#badge-filament-whisperer--filament-whisperer) | `badge-filament-whisperer.png` | ❌ pendiente |
| [`badge-first-burn`](#badge-first-burn--first-burn) | `badge-first-burn.png` | ❌ pendiente |
| [`badge-first-extrusion`](#badge-first-extrusion--first-extrusion) | `badge-first-extrusion.png` | ❌ pendiente |
| [`badge-full-spool`](#badge-full-spool--full-spool) | `badge-full-spool.png` | ❌ pendiente |
| [`badge-hello-prusa`](#badge-hello-prusa--hello-prusa) | `badge-hello-prusa.png` | ❌ pendiente |
| [`badge-laser-ace`](#badge-laser-ace--laser-ace) | `badge-laser-ace.png` | ❌ pendiente |
| [`badge-laser-pilot`](#badge-laser-pilot--laser-pilot) | `badge-laser-pilot.png` | ❌ pendiente |
| [`badge-laser-shaman`](#badge-laser-shaman--laser-shaman) | `badge-laser-shaman.png` | ❌ pendiente |
| [`badge-laser-wingman`](#badge-laser-wingman--laser-wingman) | `badge-laser-wingman.png` | ❌ pendiente |
| [`badge-layer-by-layer`](#badge-layer-by-layer--layer-by-layer) | `badge-layer-by-layer.png` | ❌ pendiente |
| [`badge-marathon-printer`](#badge-marathon-printer--marathon-printer) | `badge-marathon-printer.png` | ❌ pendiente |
| [`badge-master-operator`](#badge-master-operator--master-operator) | `badge-master-operator.png` | ❌ pendiente |
| [`badge-overnight-maker`](#badge-overnight-maker--overnight-maker) | `badge-overnight-maker.png` | ❌ pendiente |
| [`badge-patience-101`](#badge-patience-101--patience-101) | `badge-patience-101.png` | ❌ pendiente |
| [`badge-photon-sensei`](#badge-photon-sensei--photon-sensei) | `badge-photon-sensei.png` | ❌ pendiente |
| [`badge-plastic-hoarder`](#badge-plastic-hoarder--plastic-hoarder) | `badge-plastic-hoarder.png` | ❌ pendiente |
| [`badge-print-addict`](#badge-print-addict--print-addict) | `badge-print-addict.png` | ❌ pendiente |
| [`badge-rainbow-master`](#badge-rainbow-master--rainbow-master) | `badge-rainbow-master.png` | ❌ pendiente |
| [`badge-spool-halfway`](#badge-spool-halfway--spool-halfway) | `badge-spool-halfway.png` | ❌ pendiente |
| [`badge-triple-threat`](#badge-triple-threat--triple-threat) | `badge-triple-threat.png` | ❌ pendiente |

## Máquinas

### `badge-beam-buddy` — Beam Buddy

- **Fichero a crear**: `badge-beam-buddy.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Beam Buddy`
- **Categoría**: maquinas
- **Itinerario**: `laser-assistance-time` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 1 hora compartiendo el poder del rayo.

**Criterios para conseguirlo**:

> Acumular 1 hora ayudando a otros con el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-beam-operator` — Beam Operator

- **Fichero a crear**: `badge-beam-operator.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Beam Operator`
- **Categoría**: maquinas
- **Itinerario**: `laser-flight-hours` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 5 horas de dominio del rayo.

**Criterios para conseguirlo**:

> Acumular 5 horas operando el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-bed-leveler` — The Bed Leveler

- **Fichero a crear**: `badge-bed-leveler.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `The Bed Leveler`
- **Categoría**: maquinas
- **Itinerario**: `printing-hours` (nivel 4) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 100 horas dominando la impresión.

**Criterios para conseguirlo**:

> Acumular 100 horas de impresión 3D.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-color-duo` — Color Duo

- **Fichero a crear**: `badge-color-duo.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Color Duo`
- **Categoría**: maquinas
- **Itinerario**: `multimat-printing` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tu primera impresión con 2 materiales/colores.

**Criterios para conseguirlo**:

> Completar una impresión usando 2 materiales o colores diferentes.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-cut-specialist` — Cut Specialist

- **Fichero a crear**: `badge-cut-specialist.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Cut Specialist`
- **Categoría**: maquinas
- **Itinerario**: `laser-assistance-time` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 3 horas de especialista en corte comunitario.

**Criterios para conseguirlo**:

> Acumular 3 horas ayudando a otros con el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-day-job` — Day Job

- **Fichero a crear**: `badge-day-job.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Day Job`
- **Categoría**: maquinas
- **Itinerario**: `longest-print` (nivel 4) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Una pieza de 24 horas completas.

**Criterios para conseguirlo**:

> Completar una impresión de 24 horas o más.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-epic-print` — Epic Print

- **Fichero a crear**: `badge-epic-print.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Epic Print`
- **Categoría**: maquinas
- **Itinerario**: `longest-print` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> El santo grial: 48h de impresión continua.

**Criterios para conseguirlo**:

> Completar una impresión de 48 horas o más.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-extrusion-legend` — Extrusion Legend

- **Fichero a crear**: `badge-extrusion-legend.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Extrusion Legend`
- **Categoría**: maquinas
- **Itinerario**: `filament-weight` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 10 kilos de maestría en manufactura aditiva.

**Criterios para conseguirlo**:

> Fundir 10 kilos de filamento.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-filament-whisperer` — Filament Whisperer

- **Fichero a crear**: `badge-filament-whisperer.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Filament Whisperer`
- **Categoría**: maquinas
- **Itinerario**: `printing-hours` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 500 horas de maestría absoluta.

**Criterios para conseguirlo**:

> Acumular 500 horas de impresión 3D.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-first-burn` — First Burn

- **Fichero a crear**: `badge-first-burn.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `First Burn`
- **Categoría**: maquinas
- **Itinerario**: `laser-flight-hours` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tus primeros 15 minutos pilotando el láser.

**Criterios para conseguirlo**:

> Operar el láser durante 15 minutos.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-first-extrusion` — First Extrusion

- **Fichero a crear**: `badge-first-extrusion.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `First Extrusion`
- **Categoría**: maquinas
- **Itinerario**: `filament-weight` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tus primeros 100g de plástico fundido.

**Criterios para conseguirlo**:

> Fundir 100g de filamento.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-full-spool` — Full Spool

- **Fichero a crear**: `badge-full-spool.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Full Spool`
- **Categoría**: maquinas
- **Itinerario**: `filament-weight` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Un kilo completo de filamento consumido.

**Criterios para conseguirlo**:

> Fundir 1 kilo de filamento.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-hello-prusa` — Hello, Prusa!

- **Fichero a crear**: `badge-hello-prusa.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Hello, Prusa!`
- **Categoría**: maquinas
- **Itinerario**: `printing-hours` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tu primera hora de impresión 3D.

**Criterios para conseguirlo**:

> Acumular 1 hora de impresión 3D.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-laser-ace` — Laser Ace

- **Fichero a crear**: `badge-laser-ace.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Laser Ace`
- **Categoría**: maquinas
- **Itinerario**: `laser-flight-hours` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 50 horas de as del láser.

**Criterios para conseguirlo**:

> Acumular 50 horas operando el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-laser-pilot` — Laser Pilot

- **Fichero a crear**: `badge-laser-pilot.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Laser Pilot`
- **Categoría**: maquinas
- **Itinerario**: `laser-flight-hours` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 1 hora de experiencia en los controles.

**Criterios para conseguirlo**:

> Acumular 1 hora operando el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-laser-shaman` — Laser Shaman

- **Fichero a crear**: `badge-laser-shaman.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Laser Shaman`
- **Categoría**: maquinas
- **Itinerario**: `laser-assistance-time` (nivel 5) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 30 horas de chamán del láser al servicio del espacio.

**Criterios para conseguirlo**:

> Acumular 30 horas ayudando a otros con el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-laser-wingman` — Laser Wingman

- **Fichero a crear**: `badge-laser-wingman.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Laser Wingman`
- **Categoría**: maquinas
- **Itinerario**: `laser-assistance-time` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tus primeros 15 minutos como copiloto del láser.

**Criterios para conseguirlo**:

> Ayudar a otro maker con el láser durante 15 minutos.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-layer-by-layer` — Layer by Layer

- **Fichero a crear**: `badge-layer-by-layer.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Layer by Layer`
- **Categoría**: maquinas
- **Itinerario**: `printing-hours` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 50 horas de paciencia y capas.

**Criterios para conseguirlo**:

> Acumular 50 horas de impresión 3D.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-marathon-printer` — Marathon Printer

- **Fichero a crear**: `badge-marathon-printer.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Marathon Printer`
- **Categoría**: maquinas
- **Itinerario**: `longest-print` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 12 horas de una sola pieza.

**Criterios para conseguirlo**:

> Completar una impresión de 12 horas o más.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-master-operator` — Master Operator

- **Fichero a crear**: `badge-master-operator.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Master Operator`
- **Categoría**: maquinas
- **Itinerario**: `laser-flight-hours` (nivel 4) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 15 horas de maestría operacional.

**Criterios para conseguirlo**:

> Acumular 15 horas operando el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-overnight-maker` — Overnight Maker

- **Fichero a crear**: `badge-overnight-maker.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Overnight Maker`
- **Categoría**: maquinas
- **Itinerario**: `longest-print` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Dejaste una impresión corriendo toda la noche.

**Criterios para conseguirlo**:

> Completar una impresión de 6 horas o más.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-patience-101` — Patience 101

- **Fichero a crear**: `badge-patience-101.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Patience 101`
- **Categoría**: maquinas
- **Itinerario**: `longest-print` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Tu primera impresión larga (1h+).

**Criterios para conseguirlo**:

> Completar una impresión de 1 hora o más.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-photon-sensei` — Photon Sensei

- **Fichero a crear**: `badge-photon-sensei.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Photon Sensei`
- **Categoría**: maquinas
- **Itinerario**: `laser-assistance-time` (nivel 4) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 10 horas enseñando el camino del fotón.

**Criterios para conseguirlo**:

> Acumular 10 horas ayudando a otros con el láser.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-plastic-hoarder` — Plastic Hoarder

- **Fichero a crear**: `badge-plastic-hoarder.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Plastic Hoarder`
- **Categoría**: maquinas
- **Itinerario**: `filament-weight` (nivel 4) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 5 kilos de proyectos impresos.

**Criterios para conseguirlo**:

> Fundir 5 kilos de filamento.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-print-addict` — Print Addict

- **Fichero a crear**: `badge-print-addict.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Print Addict`
- **Categoría**: maquinas
- **Itinerario**: `printing-hours` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 10 horas acumuladas imprimiendo.

**Criterios para conseguirlo**:

> Acumular 10 horas de impresión 3D.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-rainbow-master` — Rainbow Master

- **Fichero a crear**: `badge-rainbow-master.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Rainbow Master`
- **Categoría**: maquinas
- **Itinerario**: `multimat-printing` (nivel 3) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Impresión con 4+ materiales/colores simultáneos.

**Criterios para conseguirlo**:

> Completar una impresión usando 4 o más materiales o colores diferentes.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-spool-halfway` — Spool Halfway

- **Fichero a crear**: `badge-spool-halfway.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Spool Halfway`
- **Categoría**: maquinas
- **Itinerario**: `filament-weight` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Medio kilo de creatividad materializada.

**Criterios para conseguirlo**:

> Fundir 500g de filamento.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-triple-threat` — Triple Threat

- **Fichero a crear**: `badge-triple-threat.png`
- **Estado**: ❌ pendiente
- **Título que debe aparecer en la imagen**: `Triple Threat`
- **Categoría**: maquinas
- **Itinerario**: `multimat-printing` (nivel 2) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Impresión con 3 materiales/colores.

**Criterios para conseguirlo**:

> Completar una impresión usando 3 materiales o colores diferentes.

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