# Catálogo de diseño

Segunda versión del catálogo TENARUZ: los mismos productos que
`catalogo/TZ-Importado_Catalogo.pdf`, pero con un diseño más de arquitectura —fotos de
producto en uso, mucho blanco, menos tabla— en vez del formato técnico.

    python3 -I catalogo-diseno/armar.py

Sale `CATALOGO_TENARUZ_DISENO.pdf`.

## De dónde sale cada cosa

Las páginas de producto **vienen diseñadas de afuera**, una imagen por ficha, en
`paginas/`. Cada archivo es un **pliego de dos páginas A4 verticales pegadas lado a lado**,
así que el armador lo parte al medio y cada mitad va a una página del PDF.

Tapa, índice y portadillas se componen acá con **texto real**, no como imagen: son las
únicas páginas que no vinieron diseñadas. La tipografía es Outfit, que es la que usan los
títulos de las páginas generadas, incrustada entera con codificación WinAnsi —alcanza para
el español, incluidos Ø y ·—.

El orden de los productos y el índice salen del catálogo técnico, no se inventan: la tabla
`FICHAS` de `armar.py` tiene las 31 fichas en el orden del original, con sus tres secciones.
Las que todavía no tienen diseño van con `None` y el armador las saltea, las deja fuera del
índice y las lista al final de la corrida. Cuando lleguen, se agrega el archivo a `paginas/`
con su número y se vuelve a correr: la paginación y el índice se recalculan solos.

## Decisiones que conviene no deshacer

**Las imágenes van en JPEG, al revés que en el catálogo técnico.** Allá las fotos eran
recortes pegados sobre un panel liso y el ruido de la compresión se veía como un recuadro
fantasma contra ese fondo plano, así que iban con Flate. Acá la página **entera** es la
imagen y no hay fondo debajo con el que pueda no coincidir. Sin comprimir, el archivo da
**30 MB** y no entra en un mail; en JPEG 92 sin submuestreo de croma da **5,6 MB**, con una
diferencia media de 1,5 sobre 255 contra el original y sólo 0,25 % de píxeles con desvío
apreciable. El logo sí va sin pérdida: es dibujo de línea y el JPEG le haría ruido alrededor.

**Lo que no es A4 no se estira.** Dos archivos vinieron en otro lienzo —el LED STICK en 4:3
y el SPOT MÓVIL en 5:3—. Se encajan enteros respetando su proporción y el sobrante se
rellena con el color del borde de la propia imagen, que en estas páginas es blanco, así que
la junta no se ve. Deformarlos para que entren sería lo único que se notaría de verdad.

**El `Tc` se emite siempre.** El espaciado entre letras es estado del texto y persiste entre
bloques: omitirlo deja el espaciado del renglón anterior y ensancha lo que viene después.
En el índice eso hacía que el detalle se montara sobre el título.

## Resolución: para pantalla, no para imprenta

Cada página queda en **745 × 1055 px**, que a tamaño A4 son **90 dpi**. Para mandar por
WhatsApp o mirar en el celular va bien. **Para imprimir no sirve**: una imprenta pide 300
dpi, o sea 2480 × 3508 px por página. El generador que se está usando topea mucho antes y
no hay prompt que lo arregle; si hace falta versión imprenta, hay que construir las páginas
en vez de generarlas como imagen.
