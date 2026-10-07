# AGENTS.md

Repositorio de imágenes de los Open Badges de Makespace Madrid. Si eres un agente
con este repo clonado y te han pedido generar insignias, esto es lo que necesitas
saber antes de tocar nada.

## Quién escribe qué

Tres ficheros **los genera el portal** y se sobreescriben completos en cada
sincronización. Editarlos a mano es trabajo perdido:

| Fichero | Contenido |
|---------|-----------|
| `missing-images.md` | Lista de imágenes que faltan + la receta de generación. |
| `badges.yaml` | El mismo catálogo en formato máquina (estilo, itinerarios, badges). |
| `README.md` | Sólo la tabla entre `<!-- badgegen:tables:start -->` y `:end`. |

Todo lo demás —los PNG, este fichero, la prosa del README— es de edición humana
(o tuya).

## Tu trabajo

**[`missing-images.md`](missing-images.md) es la fuente de verdad.** Trae, por cada
badge sin imagen: el nombre exacto del fichero a crear, el título que debe
aparecer en la imagen, la descripción y los criterios del badge, la pista visual
si la hay, el prompt que compone el portal (con el estilo y las reglas duras
literales) y el contrato del fichero final (tamaño, diámetro del disco,
circularidad mínima).

No describas la receta de memoria ni la copies de aquí: léela de ese fichero,
que se regenera con los valores que el portal tiene configurados **hoy**.

La versión en formato máquina está en `badges.yaml`, con un campo por badge:

- `status` — lo que opina el portal: `ok` / `missing` / `regen`.
- `repo_state` — lo que de verdad hay **en este repo**, comprobado contra el
  árbol de `main`. Es el que importa:

| `repo_state` | Significa |
|--------------|-----------|
| `backed_up` | El PNG está aquí. Nada que hacer. |
| `broken_url` | El portal sirve una URL de este repo que da **404**. Urgente. |
| `pending` | No hay imagen en ninguna parte. |
| `regen` | Hay imagen pero el control de calidad la ha marcado. |
| `portal_only` | El portal tiene la imagen y aquí no está. **No la generes**: la sube el portal en su próximo backup. |
| `external_url` | La imagen vive fuera de este repo. No es asunto nuestro. |
| `unknown` | No se pudo comprobar en esa pasada. |

Un `status: ok` **no** garantiza que el PNG esté aquí: durante meses 28 badges
figuraban como hechos sin fichero en el repo, y dos de ellos servían un 404. De
ahí `repo_state`.

## Al entregar

1. El nombre del fichero tiene que ser **exactamente** el de "Fichero a crear".
   El portal busca el badge por ese nombre; un typo deja el badge en 404.
2. Purga la caché del CDN:
   `curl https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/<fichero>`
3. Avisa a un owner del portal. Commitear aquí **no** le da la imagen al badge:
   el portal sirve su propia copia y sólo usa la URL de este repo cuando el badge
   no tiene ninguna imagen.

## Nombres heredados

Algunos ficheros no siguen la convención `badge-<slug>.png` porque vienen de una
migración anterior (`badge-i-can-cnc.png` para `badge-can-cnc`,
`badge-maker101.png` para `badge-maker-101`…). El nombre bueno es siempre el que
diga `missing-images.md` o el campo `file` de `badges.yaml`. No renombres nada:
romperías las URL que el portal ya está sirviendo.

`deprecated/` son imágenes retiradas. No las uses como referencia.
