# Fidelidad del catálogo de diseño contra el técnico

Comparadas las **30 fichas**, una por una, contra su ficha del catálogo técnico
(`catalogo/TZ-Importado_Catalogo.pdf`). De cada una se contrastó: título y subtítulo,
descripción, **cada fila** de la tabla técnica, la lista de códigos, el bulto cerrado y la
foto del producto.

## Los números

| qué | resultado |
|---|---|
| **Productos (fichas)** | **30 de 30 — 100 %** |
| **Códigos (SKU)** | **82 de 82 presentes — 100 %**; 81 escritos exactamente igual — 98,8 % |
| **Información técnica** | **247 de 255 filas idénticas — 97 %** (más los 60 datos de la ficha de fuentes, todos correctos) |
| **Fotos** | **30 de 30 corresponden al producto — 100 %** |

Las 255 filas son la suma de las tablas técnicas de las fichas 1 a 29; la 30 (fuentes) se
cuenta aparte porque su tabla son 15 modelos con cuatro datos cada uno, y los 60 coinciden.

## Hay que regenerar

**1. BIPIN COB G9 220V 3W** — es el problema serio. La página trae **4 filas** de
especificaciones y el técnico tiene **10**. Faltan flujo luminoso (250 lm), eficiencia
(83 lm/W), grado IP (IP20), tipo de LED (COB), vida útil (9.500 hs), corriente (14 mA) y
medidas (54 x 14 mm). Además pone «Tensión 220V» donde el técnico dice «AC 220-240V».
Es la única ficha que pierde datos que **sí existen**.

**2. LED STICK T45** — dos defectos en la misma página:
- el título dice **«LED STICKT45»**, sin espacio;
- al pie dice **«Cantidad por bulto: 1.100»** y la tabla de la misma página dice «x 100».
  Se contradice sola, y 1.100 no sale de ningún lado.

**3. BULBO A60 E27 12V/24V** — las 5 filas con guion (flujo, eficiencia, IP, tipo de LED,
vida útil). Ya verificado: esos datos **no existen** ni en el técnico ni en la planilla, así
que la corrección es sacar las filas, no completarlas. La descripción además perdió
«sin inversor».

## Correcciones menores

- **AR111 LED** — el código dimerizable figura como `TZ-AR111-15W-4K-DIM`, con guion. En la
  planilla y en el técnico es **`TZ-AR111-15W-4K DIM`**, con espacio. Importa para quien
  copie el SKU a un pedido.
- **MINIDICRO LED** — falta el **bulto cerrado x 200**. Es la única ficha sin esa línea.
- **TUBO T5 LED** — el técnico lo marca **«LIQUIDACIÓN»** y la página de diseño no. Decisión
  comercial, no error de dato.

## Lo que se revisó y está bien

- Las **82 referencias** aparecen en alguna ficha, con su temperatura y color correctos.
- Ninguna foto muestra un producto distinto del que declara la ficha. Las temperaturas de
  color de cada variante coinciden con su código en las 30.
- Los bultos cerrados coinciden en 29 de 30 (falta el del MINIDICRO).
- Las descripciones coinciden o están reescritas sin cambiar el sentido. Donde difieren, la
  versión de diseño agrega información correcta: el MR16 suma «a batería» y el BIPIN COB G4
  explica el diámetro de 1 cm, que es coherente con las medidas declaradas (41 x 10 mm).
- La ficha de **fuentes switching** agrega una tabla de «especificaciones generales» que el
  técnico no tiene (entrada 175-250V ~50/60Hz, bornera por tornillo, cuerpo metálico slim).
  No está inventada: se lee en el rótulo impreso del producto en su propia foto.

## Una que se revisó y quedó sin confirmar

En el **MINISPOT COB** la foto grande está rotulada `TZ-TDC018-4K`, que es el **blanco**, y a
simple vista parece el plateado. Medida la luminancia del cuerpo: el hero da 179, la
variante blanca 167 y la plateada 175. La diferencia es demasiado chica para afirmarlo —en
estos renders el aluminio blanco y el plateado se parecen mucho, y en el catálogo técnico
pasa lo mismo—. **No se reporta como error.** Si el cliente sabe cuál es, se confirma en un
segundo.
