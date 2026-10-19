# Cambios pendientes de aplicar

El cliente los va pasando de a uno; se aplican todos juntos cuando avise **LISTO**.

| # | qué | estado |
|---|---|---|
| 1 | Reemplazar la foto del **LED STICK T45** (`TZ-STICKE27-12W-6K`, pág. 7, slot inferior) por `fotos/stick-t45.webp` | foto guardada |
| 2 | Fotos nuevas para los tres bloques de la **DICROICA LED GU10 7W** (pág. 4): `TZ-GU10-7W-3K/4K/6K.webp` | las 3 guardadas · **van más grandes** |

## Corregido en el camino

Yo había marcado `TZ-MR11-3W-3K DIM` y `TZ-AR111-15W-4K DIM` como códigos que estaban en
la lista de precios y no en el catálogo. **Era falso**: los dos están. El error era de mi
chequeo, que cortaba los códigos en el espacio y los confundía con las versiones no
dimerizables.

Eso además tapaba un error real: **el contador de la portadilla de LÁMPARAS estaba mal**.
Decía 33 y son **35**. Viene de antes —el original decía 29 cuando eran 31— y yo lo
arrastré al sumarle mis cuatro códigos nuevos. Corregido, y anotado en la skill para que no
se repita. Contados bien, catálogo y planilla dan **82 códigos cada uno, sin diferencias**.

## Notas

- **1.** La ficha está en LÁMPARAS, así que su panel es oscuro `#1e1e1e`: la foto hay que
  recortarla de su fondo blanco y recomponerla sobre ese color. La foto es la del producto
  con la marca TENARUZ impresa en el cuerpo, 1024x1536.
- **2.** Esa ficha no tiene una foto sola: tiene **tres bloques de variante** —3000K, 4000K
  y 6000K—, cada uno con su lámpara de perfil y un halo del color de su temperatura. La
  foto nueva es **de frente y con el haz de luz dibujado hacia arriba**, otra composición.
  Si se reemplaza sólo el 3000K, el bloque queda distinto de los otros dos. Además la
  lámpara ocupa apenas la mitad de abajo del cuadro, así que al entrar en el hueco del
  bloque (unos 45 x 46 pt) quedaría mucho más chica que las otras dos.
  Llegaron las tres en la misma toma, así que se reemplaza el bloque de variantes entero.
  **Confirmado que van más grandes**, que es lo que resuelve el haz sin achicar la lámpara.
  Medido sobre la página: cada foto ocupa hoy **54 x 46,3 pt** y entre una y la siguiente
  quedan **51,1 pt de aire** (paso de 97,4 pt), así que entran a unos **85 pt de alto** y
  quedan 12 pt de aire. A lo ancho sobra: el bloque de texto arranca a 128,6 pt y la foto va
  centrada en 72,5 pt, así que admite hasta unos 95 pt y estas piden 79. El bloque de texto
  de cada variante no se mueve.

  **Regla para todas las fotos nuevas de lámpara, no sólo estas.** Las tomas nuevas son de
  frente con el haz dibujado hacia arriba, así que buena parte del alto es resplandor y no
  lámpara. Si se encajan en el hueco de hoy, la lámpara queda más chica que la que
  reemplazan. Al aplicar se escala cada foto por el **cuerpo de la lámpara**, no por el
  recuadro entero: que el cuerpo quede igual o mayor que el actual, creciendo hacia el aire
  disponible, y se verifica bloque por bloque que no se toquen. Afecta a los pedidos 2, 5,
  6, 7 y 8, y a los del MR11 cuando se confirmen. El 9 (G4) y el 1 (stick) no, porque son
  lámparas rectas sin haz dibujado: ahí la foto entra en el hueco tal cual.

| 3 | Foto nueva para **`TZ-MR11-3W-3K`** (MINIDICRO LED, pág. 4, slot inferior) → `fotos/TZ-MR11-3W-3K.webp` | guardada · **la medida no cierra** |
| 4 | Foto nueva para **`TZ-MR11-3W-3K DIM`** (mismo slot, bloque 2700K) → `fotos/TZ-MR11-3W-3K-DIM.webp` | guardada · **la medida no cierra** |
| 5 | Fotos nuevas para los dos bloques del **MR16 LED** (pág. 5): `TZ-MR16-5W-3K.webp`, `TZ-MR16-5W-6K.webp` | las 2 guardadas |
| 6 | Foto nueva para **`TZ-AR70-7W-DIM-3K`** (AR70 LED, pág. 5, slot inferior) → `fotos/TZ-AR70-7W-DIM-3K.webp` | foto guardada |
| 7 | Fotos nuevas para los dos bloques de la **AR111 LED** (pág. 6): `TZ-AR111-15W-3K.webp`, `TZ-AR111-15W-4K.webp` | las 2 guardadas |
| 8 | Fotos nuevas para los tres bloques del **PLL LED** (pág. 6, slot inferior): `TZ-PLL-18W-3K/4K/6K.webp` | **las 3 guardadas** |
| 9 | Fotos nuevas para los tres bloques del **BIPIN COB G4 12V 2W** (pág. 8): `TZ-G412V-2W-3K/4K/6K.webp` | **las 3 guardadas** · medidas verificadas |
- **3 y 4. La medida no cierra, pendiente de confirmar.** Llegó una toma nueva del 3000K,
  en tres cuartos y con lente transparente, distinta de las descartadas. La del 2700K se vio
  en el chat pero el archivo no bajó.

  **El problema es el tamaño de la lámpara.** La ficha declara **zócalo GU10 y Ø35 x 47 mm**.
  El casquillo GU10 de la foto está bien, pero el cuerpo no. La medida que lo delata es la
  relación entre el diámetro de la cabeza y el del cilindro del zócalo, que no depende de la
  escala ni del encuadre:

  | foto | cabeza / cilindro |
  |---|---|
  | la que hoy está en la ficha MINIDICRO (Ø35) | **1,62** |
  | la que hoy está en la ficha DICROICA (Ø50) | **2,32** |
  | GU10 7W del cliente (Ø50) | 2,27 / 2,48 / 2,57 |
  | MR11 descartadas por el cliente | 1,93 / 1,85 |
  | **MR11 3000K nueva** | **2,05** |
  | **MR11 2700K nueva** | **2,16** |

  O sea que las nuevas miden **igual o más que las que el cliente descartó** y lejos de la
  minidicroica que hoy está en el catálogo; quedan pegadas a la dicroica de Ø50. Medidas
  contra el paso de los pines GU10, que son 10 mm fijos, dan unos **44 mm de cabeza** cuando
  la ficha declara 35.

  Lo que sí está bien en las dos: son una pareja de tomas distintas y el tono va en el
  sentido correcto, el 2700K más cálido que el 3000K (R−B +97 contra +73), así que los dos
  bloques se van a distinguir.

  Dos salvedades honestas: el tres cuartos agranda algo la cabeza porque queda más cerca de
  la cámara, así que el número real es algo menor que 1,96 —pero no baja a 1,62—; y el
  render no parece dimensionalmente fiel, porque con la misma regla la lámpara da unos 70 mm
  de largo contra los 47 declarados. Por eso vale la relación y no el milímetro.

  **No se aplica nada en esta ficha hasta que el cliente confirme.** Si el producto es el que
  está declarado, falta la foto; si cambió el producto, hay que corregir también las medidas
  de la ficha.

  Aviso sobre mi chequeo anterior: comparar la foto contra la que **ya estaba** en la ficha
  sólo probaba parecido, no que fuera el producto correcto. La referencia buena es la medida
  declarada.

- **5.** La ficha quedó con cuatro códigos (5W en 3000K, 4000K y 6000K, más el de 7W) y
  **dos bloques de variante**, 3000K y 6000K. Son los dos que llegaron, así que se
  reemplazan los dos y la ficha queda completa: es el mismo criterio del REFLECTOR, que
  tiene cuatro códigos y dos fotos.
- **6.** De paso se verificó lo que avisa la skill, que en el 2026 las fotos de la AR70 y
  la AR111 habían quedado cruzadas de ficha. **En este archivo están bien**: medida contra
  el casquillo GU10, la lámpara de la ficha AR70 da Ø75 mm —coincide con el Ø70 que declara—
  y la de la AR111 es el reflector ancho y chato que corresponde. No hay nada que corregir.
- **7.** La ficha de la AR111 tiene **dos bloques**, 3000K y 4000K, y llegaron los dos, así
  que se reemplaza completa. El tercer código, `TZ-AR111-15W-4K DIM`, va listado en el panel
  blanco sin foto propia, como ya estaba.
- **8.** La ficha del PLL tiene **tres bloques** apilados —3000K, 4000K y 6000K—, cada uno
  con el tubo **horizontal** y su resplandor del color de la temperatura. Las dos fotos que
  llegaron son horizontales y entran en ese mismo molde sin cambiar nada. **Están las tres**
  y son tomas distintas, con el tono en el orden correcto: medido sobre el tubo encendido,
  R−B da **+32** en el 3000K, **+7** en el 4000K y **−16** en el 6000K. La ficha se reemplaza
  completa.
- **9.** El código **ya existe en el catálogo**: es la ficha BIPIN COB G4 12V 2W de la
  página 8, con `TZ-G412V-2W-3K`, `-4K` y `-6K`. Así que es un reemplazo de foto, no un
  producto nuevo, y no toca ni el índice ni los contadores de las portadillas.

  **Medida verificada.** Contra el paso de los pines G4, que son 4 mm fijos, el cuerpo da
  **9,4 mm** y la ficha declara 10. El largo total con pines da 36 mm contra los 41
  declarados, diferencia que se explica por el largo de los pines en el render. Esta foto sí
  corresponde al producto.

  **Llegaron las tres** y la ficha se reemplaza completa. Las tres miden igual —cuerpo de
  9,4 a 9,5 mm contra los 10 declarados— y el tono va en el orden correcto: R−B **+71** en el
  3000K, **+20** en el 4000K y **−11** en el 6000K.

  Aparte, al leer esta ficha apareció que **su descripción está duplicada y encimada en la
  capa de texto** del PDF ("Reemplaza Ideal una halógena para reemplazar con tamaño los
  bipines reducido…"). Es una corrección vieja que se tapó sin borrar. No se ve impreso pero
  sale al copiar o buscar texto. Entra en la limpieza de capa enterrada que está pendiente de
  decisión.
