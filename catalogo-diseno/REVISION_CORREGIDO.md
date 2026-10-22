# Revisión del «CATALOGO_TENARUZ_CORREGIDO_HEYZINE_66P.pdf»

Es el catálogo de diseño que armé, con **correcciones pegadas encima como texto**: cada
parche es un recuadro blanco con el texto nuevo arriba, sobre la imagen original. Comparado
página por página contra mi versión de 65 páginas y contra el catálogo técnico.

El diff encontró **7 páginas tocadas** más **una página nueva**; el resto es idéntico píxel
a píxel, así que todo lo demás de la auditoría anterior sigue valiendo igual.

## Corregido bien — 4

| pág | qué | estado |
|---|---|---|
| 18 | título **«LED STICK T45»**, con el espacio | ✔ |
| 19 | **«Cantidad por bulto: 100»**; desapareció el 1.100 que se contradecía | ✔ |
| 25 | **tabla completa del BIPIN COB G9**: las 10 filas, con los valores exactos del técnico (250 lm, 83 lm/W, IP20, COB, 9.500 hs, 14 mA, AC 220-240V, 54 x 14 mm) | ✔ |
| 64 | portadilla de FUENTES: **«1 ficha»** en vez de «1 fichas» —ese era un error mío— | ✔ |

Con esto la **información técnica sube de 97 % a 99,6 %**: 254 de 255 filas.

## Quedó sin corregir — 5

- **BULBO A60 12V/24V (pág. 35)** — siguen las **5 filas con guion** (flujo, eficiencia,
  grado IP, tipo de LED, vida útil). Era la corrección principal que habíamos acordado:
  esos datos no existen, así que las filas hay que **sacarlas**, no dejarlas vacías.
- **AR111 (pág. 13)** — el código dimerizable sigue siendo `TZ-AR111-15W-4K-DIM`, con guion.
  En la planilla y en el técnico es `TZ-AR111-15W-4K DIM`, con espacio.
- **MINIDICRO (pág. 7)** — sigue siendo la única ficha sin **bulto cerrado x 200**.
- **TUBO T5 (págs. 32-33)** — sigue sin la marca **«LIQUIDACIÓN»** que tiene el técnico.
- **BULBO A60 (pág. 34)** — la descripción sigue sin **«sin inversor»**.

## Problemas nuevos que no estaban — 4

**1. La página 36 quedó en blanco.** Completamente vacía. Es la página que explica que el
archivo tenga 66 y no 65.

Puede ser a propósito: con ella, la portadilla de ARTEFACTOS cae en página **impar**, o sea
a la derecha al pasar las hojas, igual que la de LÁMPARAS (pág. 3). Pero entonces la de
FUENTES tendría que estar en impar también y quedó en la **64, par**. Así que o falta una
blanca antes de FUENTES, o sobra esta.

**2. AR111 (pág. 13): la nota tapa un dato técnico.** El parche «Solo 4K DIM» se pegó sobre
la fila **«Medidas»** y borró el valor **Ø111 x 66 mm**. La ficha perdió la medida del
producto. Por la posición, parece que la nota iba una fila más abajo, sobre
«Dimerizable: Según modelo», que es lo que aclara.

**3. BULBO A60 (pág. 34): se perdió un ícono.** El rótulo **«ALTO FLUJO LUMINOSO»** quedó
reemplazado por **«LÁMPARA LED 9W»**, debajo de un ícono de sol. No describe el ícono y
repite lo que ya dice el título. Además va en otra tipografía, más pesada.

**4. El índice quedó prolijo de números pero sucio de impresión.** Los números se
renumeraron bien —38, 40, 42 … 62, 65—, que es lo que corresponde con la página en blanco.
Pero:
- van en **otra tipografía** que los de LÁMPARAS (24, 26 … 34), que quedaron sin tocar, así
  que la columna cambia de letra a la mitad;
- **asoma el borde inferior del número viejo** debajo del nuevo en nueve renglones: 38, 40,
  42, 44, 46, 48, 50, 52 y 65. El recuadro blanco quedó corto.

## Un detalle de fondo

Todos los parches **tapan pero no borran**: el texto viejo sigue en la capa de texto del
PDF. El índice tiene el 37 y el 38, la portadilla de FUENTES tiene «1 fichas» y «1 ficha».
No se ve impreso, pero sale al copiar o buscar texto, y es el mismo problema que arrastra el
catálogo técnico.

## Lo más limpio

Las cuatro correcciones que se hicieron bien, más las cinco pendientes, las puedo aplicar
**desde el fuente**: `armar.py` arma el PDF de cero, así que salen como texto propio del
documento, con la tipografía correcta, sin recuadros, sin restos abajo y sin capa enterrada.
Las que tocan la imagen de una página —las 5 filas con guion del A60 y el código de la
AR111— siguen necesitando que se regenere esa página.
