# badgegen — generación y gestión de imágenes de Open Badges

**Fecha:** 2026-07-11
**Estado:** aprobado (diseño)

## Problema

El repo tiene 86 badges en catálogo: 50 con imagen y 36 pendientes de generar
(`missing-images.md`). Varios de los existentes tienen defectos: el círculo
exterior salió achatado (elíptico) o la imagen tiene mala legibilidad. Hoy no
hay tooling: las imágenes se generan a mano y README/missing-images.md se
mantienen manualmente.

## Objetivo

CLI en Python (`tools/badgegen/`) dentro de este repo para:

1. Generar los badges que faltan y regenerar los defectuosos, usando
   **nano banana (Gemini, `gemini-2.5-flash-image`) como proveedor primario**
   y un **endpoint custom OpenAI-compatible** (flux-klein y otros modelos)
   como alternativa, detrás de una abstracción común.
2. Detectar defectos automáticamente (scan geométrico + juez de visión) con
   veto humano.
3. Flujo de candidatos + revisión visual en galería HTML; promoción manual
   del candidato elegido.
4. Post-proceso determinista que garantiza círculo perfecto, transparencia
   y tamaño estándar — corrige círculos ligeramente achatados en vez de
   rechazarlos.
5. Regenerar `README.md` y `missing-images.md` desde un manifiesto, en vez
   de mantenerlos a mano.

## Decisiones tomadas

| Decisión | Elección |
|---|---|
| Proveedor primario | nano banana (Gemini) con imágenes de referencia; endpoint custom por flag |
| Flujo | candidatos por badge + galería HTML de revisión + promote manual |
| Detección de defectos | scan automático (geometría + visión) con veto del usuario |
| Arquitectura | CLI Python en `tools/` de este repo, manifiesto `badges.yaml` |

## Estructura del repo (nueva)

```
open-badges/
├─ badge-*.png             # imágenes finales (sin cambio)
├─ badges.yaml             # manifiesto: fuente de verdad local
├─ candidates/<slug>/      # variantes generadas (gitignored)
├─ review/                 # galerías HTML generadas (gitignored)
├─ docs/superpowers/specs/ # este documento
└─ tools/
   ├─ badgegen/
   │  ├─ cli.py            # subcomandos: sync|scan|generate|review|promote|docs
   │  ├─ manifest.py       # carga/merge/escritura de badges.yaml
   │  ├─ providers/
   │  │  ├─ base.py        # generate(prompt, reference_images, n) -> [bytes]
   │  │  ├─ gemini.py      # nano banana, multimodal con referencias
   │  │  └─ openai_compat.py # POST /v1/images/generations (b64_json)
   │  ├─ qc.py             # redondez, alpha, tamaño; juez de visión opcional
   │  ├─ postprocess.py    # circularización, centrado, máscara, 1254px
   │  ├─ gallery.py        # scan-report.html y review.html estáticos
   │  └─ docs_gen.py       # README.md + missing-images.md desde manifiesto
   ├─ requirements.txt     # pillow, numpy, httpx, pyyaml (sin OpenCV, sin SDKs)
   └─ .env                 # credenciales (gitignored)
```

## Manifiesto `badges.yaml`

```yaml
style: >
  Circular maker badge, flat vector style, golden yellow (#F5C400) on black,
  outer ring with screw heads, bold sans-serif text, high contrast, centered
  composition, transparent background outside the ring
badges:
  - slug: badge-i-can-laser
    name: I Can Laser
    file: badge-i-can-laser.png
    track: maquinas
    description: "..."      # sincronizado desde el portal
    criteria: "..."         # sincronizado desde el portal
    visual: "a laser cutter head with beam cutting plywood"  # manual
    status: missing          # ok | missing | regen
    issues: []               # p.ej. [flattened-circle, low-legibility]
    provider: null           # override opcional por badge
    prompt_extra: null       # texto adicional opcional
```

- `sync` parsea `../InfraSelfService/src/lib/badges/catalog.ts` (ruta
  configurable) con un extractor tolerante de literales de objeto y actualiza
  `name`, `description`, `criteria`, `track`; añade badges nuevos con
  `status: missing` si no existe su PNG. **Nunca pisa** campos manuales:
  `visual`, `status: regen`, `issues` confirmados, `provider`, `prompt_extra`.
- El prompt final de un badge = `style` global + nombre + `visual` (o
  descripción si no hay `visual`) + `prompt_extra`.

## Proveedores

Interfaz común (`providers/base.py`):

```python
def generate(prompt: str, reference_images: list[bytes], n: int) -> list[bytes]
```

- **gemini** (default): REST directo a la API de Gemini
  (`gemini-2.5-flash-image`), petición multimodal que incluye las imágenes de
  referencia listadas en `badges.yaml` (clave global `reference_images`,
  default: `badge-template.png`, `badge-member.png`, `badge-hello-glados.png`)
  y pide mantener estilo, proporciones y anillo circular.
- **custom**: endpoint OpenAI-compatible, `POST {CUSTOM_BASE_URL}/v1/images/generations`
  con `response_format: b64_json`; modelo via `--model` o `CUSTOM_IMAGE_MODEL`
  (flux-klein u otros).

Ambos vía `httpx`, sin SDKs. Credenciales en `tools/.env`:
`GEMINI_API_KEY`, `CUSTOM_BASE_URL`, `CUSTOM_API_KEY`, `CUSTOM_IMAGE_MODEL`.

## Comandos

```
badgegen sync                      # catálogo del portal → badges.yaml
badgegen scan [slugs...] [--judge] [--write]
badgegen generate [slugs... | --status missing,regen] [-n 4]
                  [--provider gemini|custom] [--model X]
badgegen review [slugs...]
badgegen promote <slug> <candidato.png> [--keep-candidates]
badgegen fix <slug>                # post-proceso in-place del PNG final existente
badgegen docs                      # regenera README.md y missing-images.md
```

> **Addendum (medición real):** el propio `badge-template.png` está achatado
> (ratio ejes 0.9566, bbox 1166×1219), igual que varios badges existentes.
> Por ello: (1) el diámetro objetivo del post-proceso es una constante
> configurable (`target_diameter: 1180` en `badges.yaml`), no se mide del
> template; (2) existe `badgegen fix <slug>`, que aplica el post-proceso
> directamente al PNG final existente — arregla badges achatados sin
> regenerarlos con IA, preservando el arte aprobado.

### scan

- Checks deterministas (Pillow + numpy): tamaño 1254×1254, modo RGBA,
  esquinas transparentes, **redondez**: elipse ajustada por momentos de
  segundo orden de la máscara alpha del disco exterior; flag
  `flattened-circle` si eje_menor/eje_mayor < **0.985** (configurable).
- `--judge`: manda cada imagen a Gemini con una rúbrica de legibilidad
  (texto legible, tipografía rota, ruido, contraste) → score 1–5 + issues.
  Opt-in para no gastar API en cada pasada.
- Salida: `review/scan-report.html` (miniaturas + tabla de issues). Con
  `--write`, vuelca los issues al manifiesto; el paso a `status: regen` lo
  decide siempre el usuario editando el YAML (el scan nunca cambia `status`).

### generate

- Selección por slugs explícitos o `--status missing,regen`.
- Deja `candidates/<slug>/NN-<provider>.png` + sidecar
  `NN-<provider>.json` (prompt completo, provider, modelo, fecha).
- Cada candidato pasa el QC geométrico al generarse; el resultado se guarda
  en el sidecar (la galería marca en rojo los que fallan).
- Batch: fallo en un badge no corta el resto; resumen de errores al final.
  Reintentos con backoff exponencial en 429/5xx (3 intentos).

### review

- HTML estático (funciona con `file://`): por badge, candidatos en fila +
  imagen actual si existe, con badge de QC (verde/rojo) y metadata.
- Cada candidato muestra su comando `badgegen promote <slug> <file>` con
  click-para-copiar. Sin servidor, sin estado en el HTML.

### promote (post-proceso determinista, siempre se aplica)

1. Detecta el disco exterior sobre la máscara alpha (o sobre color si el
   fondo vino opaco) y ajusta elipse.
2. Ratio ejes ∈ [0.93, 1.0) → **corrección anisotrópica de escala** para
   circularizar. Ratio < 0.93 → error con mensaje "regenerar" y aborta.
   (Originalmente 0.95; se bajó a 0.93 tras medir el corpus real: el
   achatamiento sistémico llega a 0.943 y el estirado ≤7% restaura las
   proporciones originales sin artefactos visibles.)
3. Centra el disco, escala al diámetro del template, lienzo 1254×1254 RGBA,
   máscara circular alpha (fuera del anillo → transparente).
4. Guarda `badge-<slug>.png`, marca `status: ok` y limpia `issues` en el
   manifiesto, borra `candidates/<slug>/` (salvo `--keep-candidates`),
   purga jsDelivr (`GET https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/<file>`)
   y ejecuta `docs` para refrescar README/missing-images.
5. Si el purge falla: warning con la URL para lanzarlo a mano; no aborta.

### docs

- Regenera las tablas de `README.md` (por track, con ✅/❌) y
  `missing-images.md` desde el manifiesto, preservando el texto introductorio
  fuera de las tablas mediante marcadores de comentario HTML
  (`<!-- badgegen:tables -->`), que la primera ejecución inserta en ambos
  archivos.

## Manejo de errores

- API: backoff exponencial en 429/5xx, 3 reintentos; errores 4xx no
  recuperables se reportan con cuerpo de respuesta.
- Batch resiliente: se acumulan errores por badge y se listan al final con
  exit code ≠ 0 si hubo alguno.
- `sync`: si el parser del catálogo no encuentra el archivo o el formato
  cambió (0 entradas), aborta sin tocar el manifiesto.
- `promote`: nunca sobreescribe el PNG final si el post-proceso falla.

## Testing

- Unit tests (pytest) sin llamadas de red:
  - `qc`: fixtures sintéticas — círculo perfecto (pasa), elipse 0.97
    (flag), elipse 0.90 (irrecuperable), imagen sin alpha, tamaño incorrecto.
  - `postprocess`: una elipse 0.97 tras circularizar queda ≥ 0.995;
    centrado y máscara correctos; idempotencia (procesar dos veces no cambia).
  - `manifest`: merge de `sync` no pisa campos manuales; badges nuevos
    entran como `missing`.
  - `docs_gen`: golden files de README/missing-images.
  - providers con fakes (respuestas b64 precocinadas).
- Prueba manual de humo: `generate` de 1 badge real con cada proveedor.

## Fuera de alcance

- UI en el portal InfraSelfService (descartado en diseño).
- Commit/push automático (el usuario revisa y commitea como hasta ahora).
- Optimización de peso de PNGs (posible mejora futura).
- Edición/inpainting de badges existentes (solo regeneración completa).
