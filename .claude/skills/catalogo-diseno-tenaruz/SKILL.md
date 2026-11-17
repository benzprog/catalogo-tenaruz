---
name: catalogo-diseno-tenaruz
description: Armar o modificar el catálogo DE DISEÑO de TENARUZ / Pana Iluminación (CATALOGO_TENARUZ_DISENO.pdf), el de estilo arquitectura con fotos de ambiente, que se arma pegando páginas ya diseñadas afuera. Usar cuando llegue una página nueva o corregida para ese catálogo, cuando haya que rehacer el índice interactivo, la tapa o las portadillas, cuando se pida comparar ese catálogo contra el técnico, o cuando se pida convertir páginas sueltas (imágenes de pliegos A4) en un PDF con índice clickeable. NO es para el catálogo técnico de fichas: ese tiene su propia skill, `catalogo-tenaruz`.
---

# Catálogo de diseño TENARUZ

Segunda versión del catálogo: **los mismos productos que el técnico**, con un diseño de
arquitectura —fotos de producto en uso, mucho blanco, menos tabla—.

Las reglas de trabajo del cliente y los chequeos de foto están en la skill
**`catalogo-tenaruz`**, en «Cómo trabaja el cliente» y «Antes de aplicar una foto que te
mandan». Valen igual acá. Lo de abajo es lo propio de este catálogo.

    python3 -I catalogo-diseno/armar.py

Sale `catalogo-diseno/CATALOGO_TENARUZ_DISENO.pdf`.

## Lo que hay que entender primero

**Las páginas de producto vienen diseñadas de afuera**, una imagen por ficha, en
`catalogo-diseno/paginas/`. Cada archivo es un **pliego de dos páginas A4 verticales pegadas
lado a lado** (proporción 1,414), así que el armador lo parte al medio y cada mitad va a una
página del PDF. El número del archivo es el orden de la ficha.

**Tapa, índice y portadillas se componen acá con texto real**, no como imagen: son las únicas
páginas que no vinieron diseñadas. La tipografía es **Outfit**, la misma de los títulos
generados, incrustada entera con codificación WinAnsi —alcanza para el español, Ø y · incluidos—.

**El orden y el índice salen del catálogo técnico**, no se inventan. La tabla `FICHAS` de
`armar.py` tiene las 30 fichas en el orden del original con sus tres secciones. Una ficha sin
diseño va con `None`: el armador la saltea, la deja fuera del índice y la lista al final de la
corrida. Cuando llega, se agrega el archivo a `paginas/` con su número y se vuelve a correr:
**la paginación y el índice se recalculan solos**.

## Trampas que costaron

**El `Tc` se emite siempre.** El espaciado entre letras es estado del texto y **persiste entre
bloques**: omitirlo deja el espaciado del renglón anterior y ensancha lo que viene después. En
el índice eso hacía que la aclaración se montara sobre el título.

**`OutlineItem` espera el número de página contando desde cero**, no el objeto de página.
Pasarle el objeto deja un `/Dest` que el lector no entiende y el PDF abre sin marcadores.

**Lo que no es A4 no se estira.** Algunos archivos vienen en otro lienzo (4:3, 5:3, 1,595).
Se encajan enteros respetando su proporción y el sobrante se rellena con **el color del borde
de la propia imagen** —en estas páginas, blanco—, así la junta no se ve. Deformarlos para que
entren sería lo único que se notaría de verdad.

**Las imágenes van en JPEG, al revés que en el catálogo técnico.** Allá las fotos eran recortes
pegados sobre un panel liso y el ruido del JPEG se veía como un recuadro fantasma contra ese
fondo plano. Acá la página **entera** es la imagen y no hay fondo debajo con el que pueda no
coincidir. Sin comprimir el archivo da 30 MB y no entra en un mail; en **JPEG 92 sin
submuestreo de croma** da 8,5 MB. Comparadas al 300 % contra el PNG original, las calidades 88,
92 y 96 son indistinguibles: subirla sólo pesa (96 llevaba el archivo a 14 MB).

**No bajes la resolución de nada.** El tope del incrustador está en 4000 px a propósito. Con
tope 1600 las dos páginas del reflector, que vienen a 1800, caían de 218 a 194 dpi: justo las
únicas nítidas del catálogo.

## El índice interactivo

Cada renglón lleva un enlace que salta a la página de esa ficha, **sobre todo el ancho del
renglón** y no sólo sobre el texto: en un celular hay que poder tocarlo sin apuntar fino. El
PDF lleva además marcadores por sección.

El orden importa: **los enlaces se arman después de crear las páginas** y el índice se inserta
en el lugar 2, porque antes los objetos de página a los que apuntan no existen.

Cada renglón lleva también una **aclaración** —cuántas temperaturas tiene, si hay versión
dimerizable, si no incluye lámpara o zócalo—. **No se deducen: se leen de la lista de modelos
de cada página.** Van alineadas a la derecha para que el renglón largo se acomode solo, y el
armador avisa por consola si alguna no entra.

Los 30 renglones más las tres cabeceras entran justo en una página: los pasos están medidos
para eso, así que tocar los cuerpos obliga a recalcularlos.

## Auditar contra el catálogo técnico

Es el control que más valor dio. Se compara **ficha por ficha**: título y subtítulo,
descripción, **cada fila** de la tabla técnica, la lista de códigos, el bulto cerrado y la foto.

La forma práctica: armar una imagen por ficha con el **slot del técnico arriba y el pliego de
diseño abajo**, a 1500 px de ancho, y mirarlas de a una. No hay OCR disponible, así que el
cotejo de las tablas es a ojo; lo que sí se automatiza es el recuento de códigos y el diff
contra la versión anterior.

Métricas de la última auditoría, como referencia de qué se mide: **30/30 productos, 82/82
códigos presentes, 254/255 filas técnicas, 30/30 fotos correctas**.

Dos cosas que encontró y que no se ven de otra manera:

- una ficha con **4 filas de especificaciones donde el técnico tiene 10** (el BIPIN COB G9);
- un título pegado —«LED STICKT45»— y un «Cantidad por bulto: 1.100» que se contradecía con el
  «x 100» de su propia tabla.

Y una que **no se pudo confirmar y por eso no se reportó como error**: en el MINISPOT, blanco y
plateado dan 167 y 175 de luminancia, demasiado cerca para afirmar que la foto grande está mal
rotulada. Cuando el método no alcanza, se dice.

## Si llega una versión «corregida» desde afuera

Pasó: volvió un PDF de 66 páginas con las correcciones **pegadas encima como parches de texto**
—un recuadro blanco con el texto nuevo arriba de la imagen—. Para revisarla:

1. **Diff página por página contra la versión propia**, teniendo en cuenta las páginas
   insertadas. Encontró 7 páginas tocadas más una en blanco; el resto, idéntico píxel a píxel.
2. **`pdftotext` por página** para ver dónde hay parches: el texto nuevo aparece ahí.

Lo que los parches dejan mal, y hay que buscar siempre: **páginas en blanco** insertadas para
renumerar, **parches corridos de fila** que tapan un dato real (uno borró el `Ø111 x 66 mm` de
la AR111), **tipografía distinta** de la del documento, **el texto viejo asomando** debajo del
recuadro blanco cuando quedó corto, y la **capa de texto duplicada** —tapar no borra: el índice
quedó con el 37 y el 38 a la vez—.

**Conviene rehacerlo desde el fuente** en vez de parchear: `armar.py` reconstruye el PDF de
cero y las correcciones salen como texto propio del documento, sin recuadros, sin restos y sin
capa enterrada.
