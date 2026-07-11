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

## Series

Un badge puede llevar `references:` en badges.yaml (lista de PNGs del repo) que
sustituyen a las `reference_images` globales al generar — se usa para que los
badges de una serie (antigüedad, eventos, assembly…) hereden el estilo del
nivel anterior. Si ninguna referencia de la lista existe todavía (nivel previo
sin promocionar), se cae a las globales. Generar las series en orden de nivel
y promocionar cada nivel antes de generar el siguiente da la máxima coherencia.

## Tests

    .venv/bin/pytest -v
