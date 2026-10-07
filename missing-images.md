# Imágenes de badges pendientes

_Generado por el portal el 2026-10-07. **No editar a mano**: se reescribe completo en cada sincronización. Los datos de cada badge vienen de la base de datos del portal y están también, en formato máquina, en [`badges.yaml`](badges.yaml)._

No falta ninguna imagen: los **130** badges activos tienen la suya.

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

Ninguno. Todos los badges activos tienen su imagen.

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