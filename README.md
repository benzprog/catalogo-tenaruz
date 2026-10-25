# Catálogo TENARUZ

Materiales comerciales de **TENARUZ / PANA ILUMINACIÓN**: el catálogo PDF, las listas de
precios, los flyers y los avisos. No es una aplicación web: es contenido, más los scripts
de Python que lo generan y lo editan.

| | |
| --- | --- |
| Carpeta en esta PC | `Z:\Proyectos\catalogo-tenaruz` |
| Repositorio | https://github.com/benzprog/catalogo-tenaruz (privado) |
| Rama principal | `main` |
| Publicado en | no se publica: los PDF se entregan a mano o por WhatsApp |

## Qué hay en cada carpeta

| Carpeta | Qué contiene |
| --- | --- |
| `catalogo/` | El catálogo PDF de productos y los scripts que lo editan |
| `catalogo-diseno/` | La versión de diseño del catálogo |
| `listas-precios/` | Listas de precios al público, por mes |
| `listas-mayorista/` | Listas mayoristas |
| `flyers/` | Flyers mensuales de PANA, generados con Python + Pillow |
| `avisos/` | Avisos y ofertas puntuales |
| `logos/` | Logos de TENARUZ en distintos formatos |

Varias de esas carpetas tienen su propio `README.md` con el detalle.

## Editar el catálogo

Hay una skill de Claude Code en `.claude/skills/catalogo-tenaruz/` que explica cómo
inyectar contenido en el PDF sin romper la tipografía. **Leerla antes de tocar el
catálogo**: el PDF se generó con `wkhtmltopdf`, el archivo fuente no existe, y tiene una
transformación de escala que hace que los tamaños de fuente del content stream no sean los
que se ven al renderizar.

Los scripts de `.claude/skills/catalogo-tenaruz/scripts/` se importan entre sí y resuelven
su propia ruta, así que corren desde cualquier carpeta. La variable `W` de cada uno apunta
a la carpeta de trabajo y por defecto es `.`.

## De dónde vienen los nombres

Hasta el 24 de octubre de 2026 este repositorio se llamaba
`benzprog/nicolas-logistics-portfolio`, un nombre heredado que no describía nada de lo que
hay acá. GitHub redirige el nombre viejo, pero el actual es `catalogo-tenaruz`.

PANA Gestión también se construyó dentro de este repositorio antes de mudarse a
`benzprog/pana-gestion`. Por eso en el historial hay commits de PANA Gestión y quedó la
rama `claude/pana-gestion-architecture-umxpmo`, que ya no se usa.
