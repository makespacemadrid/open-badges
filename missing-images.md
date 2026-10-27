# Imágenes de badges pendientes

_Generado por el portal el 2026-10-27. **No editar a mano**: se reescribe completo en cada sincronización. Los datos de cada badge vienen de la base de datos del portal y están también, en formato máquina, en [`badges.yaml`](badges.yaml)._

Faltan **13** imágenes de **167** badges activos (13 marcadas para regenerar).

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
| [`badge-community-pillar`](#badge-community-pillar--community-pillar) | `badge-community-pillar.png` | 🔄 regenerar |
| [`badge-community-veteran`](#badge-community-veteran--community-veteran) | `badge-community-veteran.png` | 🔄 regenerar |
| [`badge-first-assembly`](#badge-first-assembly--first-assembly) | `badge-first-assembly.png` | 🔄 regenerar |
| [`badge-hackspace-hero`](#badge-hackspace-hero--hackspace-hero) | `badge-hackspace-hero.png` | 🔄 regenerar |
| [`badge-hackspace-legend`](#badge-hackspace-legend--hackspace-legend) | `badge-hackspace-legend.png` | 🔄 regenerar |
| [`badge-keymaster`](#badge-keymaster--keymaster) | `badge-keymaster.png` | 🔄 regenerar |
| [`badge-make-noise`](#badge-make-noise--make-noise) | `badge-make-noise.png` | 🔄 regenerar |
| [`badge-palego`](#badge-palego--palego) | `badge-palego.png` | 🔄 regenerar |
| [`badge-relic-printer`](#badge-relic-printer--relic-printer) | `badge-relic-printer.png` | 🔄 regenerar |
| [`badge-textile-maker`](#badge-textile-maker--no-es-una-bufanda-es-un-prototipo) | `badge-textile-maker.png` | 🔄 regenerar |
| [`badge-token-donor`](#badge-token-donor--token-donor) | `badge-token-donor.png` | 🔄 regenerar |
| [`badge-vehicle-builder`](#badge-vehicle-builder--muévelo) | `badge-vehicle-builder.png` | 🔄 regenerar |
| [`badge-viajero-del-tiempo`](#badge-viajero-del-tiempo--viajero-del-tiempo) | `badge-viajero-del-tiempo.png` | 🔄 regenerar |

## Eventos

### `badge-community-pillar` — Community Pillar

- **Fichero a crear**: `badge-community-pillar.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Community Pillar`
- **Categoría**: eventos
- **Itinerario**: `reunion-mensual` (nivel 15) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 15 reuniones. La comunidad lo nota cuando no estás.

**Criterios para conseguirlo**:

> Asistir a 15 reuniones mensuales.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-community-veteran` — Community Veteran

- **Fichero a crear**: `badge-community-veteran.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Community Veteran`
- **Categoría**: eventos
- **Itinerario**: `reunion-mensual` (nivel 10) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 10 reuniones. Un pilar de la asamblea mensual.

**Criterios para conseguirlo**:

> Asistir a 10 reuniones mensuales.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-first-assembly` — First Assembly

- **Fichero a crear**: `badge-first-assembly.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `First Assembly`
- **Categoría**: eventos
- **Itinerario**: `reunion-mensual` (nivel 1) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> Asististe a la reunión mensual de la comunidad por primera vez.

**Criterios para conseguirlo**:

> Asistir a 1 reunión mensual.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-hackspace-hero` — Hackspace Hero

- **Fichero a crear**: `badge-hackspace-hero.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Hackspace Hero`
- **Categoría**: eventos
- **Itinerario**: `hack-the-space` (nivel 30) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 30 sesiones de contribución dedicada al espacio.

**Criterios para conseguirlo**:

> Asistir a 30 sesiones de Hack the Space.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-hackspace-legend` — Hackspace Legend

- **Fichero a crear**: `badge-hackspace-legend.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Hackspace Legend`
- **Categoría**: eventos
- **Itinerario**: `hack-the-space` (nivel 25) — ver `tracks` en `badges.yaml`

**Motivo del badge** (lo que se le cuenta al socio):

> 25 sesiones. Se cuentan historias de makers como tú.

**Criterios para conseguirlo**:

> Asistir a 25 sesiones de Hack the Space.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

## Otros

### `badge-keymaster` — Keymaster

- **Fichero a crear**: `badge-keymaster.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Keymaster`

**Motivo del badge** (lo que se le cuenta al socio):

> Con un gran acceso viene una gran responsabilidad. Esta insignia reconoce a quien usa su llave para facilitar la vida a los demás makers.

**Criterios para conseguirlo**:

> Quedarse o volver al espacio para que otro maker pueda terminar su sesión sin prisas, o contestar en el chat cuando alguien pregunte si el espacio estará abierto.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-make-noise` — Make Noise!

- **Fichero a crear**: `badge-make-noise.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Make Noise!`

**Motivo del badge** (lo que se le cuenta al socio):

> Haz un instrumento o un engendro musical. Desde simple caña con agujeros a un engendro electromecánico que toque la pandereta, todo vale.

**Criterios para conseguirlo**:

> Fabricar su propio instrumento musical.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-palego` — PaLego

- **Fichero a crear**: `badge-palego.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `PaLego`

**Motivo del badge** (lo que se le cuenta al socio):

> Habilidad de reconvertir pallets en muebles u otras cosas útiles para el espacio.

**Criterios para conseguirlo**:

> Construir algo interesante a base de pallets y tornillos o clavos.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-relic-printer` — Relic Printer

- **Fichero a crear**: `badge-relic-printer.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Relic Printer`

**Motivo del badge** (lo que se le cuenta al socio):

> Has conseguido imprimir algo con hardware legacy del Makespace (Taz, Monster o Madre).

**Criterios para conseguirlo**:

> Completar una impresión 3D usando una de las máquinas históricas del espacio (anteriores a 2020).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-textile-maker` — No es una bufanda, es un prototipo

- **Fichero a crear**: `badge-textile-maker.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `No es una bufanda, es un prototipo`

**Motivo del badge** (lo que se le cuenta al socio):

> Demuestra tu destreza con el ganchillo, las dos agujas o cualquier técnica de tejido.

**Criterios para conseguirlo**:

> Realizar un objeto con alguna técnica de tejido (ganchillo, dos agujas, telar, etc.).

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-token-donor` — Token Donor

- **Fichero a crear**: `badge-token-donor.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Token Donor`

**Motivo del badge** (lo que se le cuenta al socio):

> Has puesto a tus cuentas de OpenAI, Claude u Ollama a trabajar en tareas pendientes de los repos de Makespace.

**Criterios para conseguirlo**:

> Contribuir código al proyecto del portal del Makespace: al menos 1 pull request aceptado.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-vehicle-builder` — Muévelo

- **Fichero a crear**: `badge-vehicle-builder.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Muévelo`

**Motivo del badge** (lo que se le cuenta al socio):

> Construye tu propio vehículo, desde una bicicleta a un longboard del Decathlon tuneado.

**Criterios para conseguirlo**:

> Construir, o ayudar a construir, un vehículo funcional.

**Sin pista visual**: no hay `visual` definido para este badge. Deriva el motivo principal de la descripción y los criterios de arriba — un objeto o acción reconocible, no una escena.

### `badge-viajero-del-tiempo` — Viajero del tiempo

- **Fichero a crear**: `badge-viajero-del-tiempo.png`
- **Estado**: 🔄 regenerar
- **Título que debe aparecer en la imagen**: `Viajero del tiempo`

**Motivo del badge** (lo que se le cuenta al socio):

> Todos viajamos al futuro, un segundo cada segundo, pero algunos hemos fabricado relojes o herramientas para mostrar o medir el paso del tiempo.

**Criterios para conseguirlo**:

> Fabricar o reparar un reloj, o explicar en un evento cómo funciona un reloj.

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