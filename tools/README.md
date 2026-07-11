# badgegen

CLI para generar y gestionar las imágenes de los Open Badges.

## Setup

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    cp .env.example .env   # y rellena las claves

## Uso (desde tools/)

    .venv/bin/python -m badgegen sync        # catálogo del portal → badges.yaml
    .venv/bin/python -m badgegen scan        # QC de las imágenes existentes (+ --judge, --write)
    .venv/bin/python -m badgegen generate    # candidatos para missing/regen (-n 4, --provider custom)
    .venv/bin/python -m badgegen review      # galería review/review.html
    .venv/bin/python -m badgegen promote badge-x candidates/badge-x/01-gemini.png
    .venv/bin/python -m badgegen fix badge-x # circulariza el PNG final sin regenerar
    .venv/bin/python -m badgegen docs        # regenera README.md y missing-images.md

Flujo típico: `sync` → `scan --write` → marcar `status: regen` en badges.yaml →
`generate` → abrir `review/review.html` → `promote` de los elegidos.

## Tests

    .venv/bin/pytest -v
