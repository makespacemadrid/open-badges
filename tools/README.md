# badgegen

CLI para generar y gestionar las imágenes de los Open Badges.

## Setup

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    cp .env.example .env   # y rellena las claves

## Uso (desde tools/)

    .venv/bin/python -m badgegen sync           # catálogo del portal → badges.yaml
    .venv/bin/python -m badgegen scan           # QC de las imágenes existentes (+ --judge, --write)
    .venv/bin/python -m badgegen generate       # candidatos para missing/regen (-n 4, --provider custom)
    .venv/bin/python -m badgegen review --serve # revisión en el navegador con botón Promocionar
    .venv/bin/python -m badgegen review         # (alternativa: galería estática review/review.html)
    .venv/bin/python -m badgegen promote badge-x candidates/badge-x/01-gemini.png
    .venv/bin/python -m badgegen fix badge-x    # circulariza el PNG final sin regenerar
    .venv/bin/python -m badgegen docs           # regenera README.md y missing-images.md

Flujo típico: `sync` → `generate` → `review --serve` (elegir con un clic) → push + purge.

## Series y tracks

Un badge puede llevar `references:` en badges.yaml (PNGs del repo) que
sustituyen a las `reference_images` globales — así los niveles de una serie
heredan el estilo del nivel anterior. Además, `tracks:` define config por
track: `references` (artworks que se SUMAN a las del badge, p.ej.
`assets/makespace-icon.png`) y `prompt_extra` (texto común a toda la serie).
Si ninguna referencia existe aún en disco, se cae a las globales. Generar las
series en orden de nivel y promocionar antes de pasar al siguiente da la
máxima coherencia. Los artworks sueltos viven en `assets/`.

## Gestor web (`review --serve`) — contrato de endpoints

Pensado para migrarse al portal de miembros; el portal puede consumir esto o
reimplementarlo. Todos los POST son `application/x-www-form-urlencoded`:

    GET  /                 página del gestor
    GET  /api/state        estado completo en JSON (badges, candidatos, jobs, config)
    GET  /img?p=<rel.png>  sirve un PNG del repo (candidatos, finales, assets)
    POST /promote          slug, candidate         → post-proceso + final + purge + docs
    POST /generate         slug, provider?         → 3 candidatos en background
    POST /fix              slug                    → circulariza el PNG final in-place
    POST /scan             —                       → QC de todos los finales (background)
    POST /sync             —                       → catálogo del portal → badges.yaml
    POST /docs             —                       → regenera README/missing-images
    POST /edit             slug, visual, prompt_extra, references
    POST /track            track, references, prompt_extra
    POST /globals          style, references

Sin autenticación: pensado para LAN o detrás del auth del portal.

## Tests

    .venv/bin/pytest -v
