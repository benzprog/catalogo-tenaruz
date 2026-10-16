# Agregar los 18 códigos nuevos de 12V al catálogo

Decisión del cliente: **sin sección nueva**. Las fichas nuevas entran en ARTEFACTOS.

## Las fichas

| ficha | códigos nuevos | qué es |
|---|---|---|
| MR16 LED 12V | `TZ-MR16-5W-4K`, `TZ-MR16-7W-3K` | existente (LÁMPARAS), pasa de 2 a 4 códigos |
| SPOT 12V MÓVIL | `TZ-TDC005-4K`, `TZ-TDC033-3K`, `TZ-TDC034-4K`, `TZ-TDC031-3K`, `TZ-TDC032-4K` | existente (ARTEFACTOS), pasa de 1 a 6 códigos |
| BULBO A60 LED 12V/24V 9W | `TZ-A6012V24V-9W-3K`, `-6K` | nueva — **va a LÁMPARAS**: es una lámpara E27 y en la planilla del cliente está en esa sección |
| PLAFÓN LED ALUMINIO 12V 2,5W Ø60 | `TZ-TDC003-3K`, `TZ-TDC004-6K` | nueva, ARTEFACTOS |
| PANEL REDONDO EMBUTIR 12V 3W Ø83 BLANCO | `TZ-PNR12V-3W-BL-3K`, `-6K` | nueva, ARTEFACTOS |
| PANEL EMBUTIR REDONDO 12V 3W Ø70 NEGRO | `TZ-TDC011-3K`, `TZ-TDC014-6K` | nueva, ARTEFACTOS |
| MINISPOT COB ALUMINIO 12V 1W Ø20 | `TZ-TDC018-4K`, `TZ-TDC019-4K`, `TZ-TDC010-4K` | nueva, ARTEFACTOS |

Códigos por sección al terminar: LÁMPARAS **33**, ARTEFACTOS **32**, FUENTES **15** = 80.
Hay que actualizar los tres contadores de portadilla (hoy 29 / 18 / 15).

## La paginación

Las cuatro fichas nuevas de ARTEFACTOS van **detrás del SPOT 12V MÓVIL**, para que el
bloque de 12V se lea junto. Cuatro fichas son exactamente cuatro slots, o sea dos páginas:
por eso **todo lo que corre lo hace 2 páginas enteras y conserva su mitad** (lo de arriba
sigue arriba, lo de abajo sigue abajo). No hay que espejar ningún panel.

```
        antes                          después
p11     TUBO T5 (ficha sola)           TUBO T5 (arriba) + BULBO A60 12V/24V (abajo)
p13     spots 220V                     igual
p14     SPOT 12V | SPOT MINI           SPOT 12V (+5 códigos) | PLAFÓN Ø60
p15     REFLECTOR | APL CURVO          PANEL Ø83 | PANEL Ø70
p16     APL RECTO | ESTACA AL          MINISPOT Ø20 | SPOT MINI  (baja de p14)
p17     ESTACA SOLAR (sola)            REFLECTOR | APL CURVO     (la p15 vieja tal cual)
p18     portadilla FUENTES             APL RECTO | ESTACA AL     (la p16 vieja tal cual)
p19     fuentes                        ESTACA SOLAR (sola)       (la p17 vieja tal cual)
p20     contacto                       portadilla FUENTES
p21                                    fuentes
p22                                    contacto
```

20 -> 22 páginas. Renumerar de la 13 para abajo; portada y contacto no llevan número.
Rehacer el índice entero (de 26 a 31 fichas).

**La página 11 es el único reflow incómodo**: hoy el TUBO T5 es una ficha sola con los
paneles a toda altura, y hay que partirla en dos slots para meter el bulbo A60 abajo.

## Fotos: qué SKU va en cada una

| foto | SKU | |
|---|---|---|
| spot cabezal negro | `TZ-SPOT12V-3W-NG-3K`, `TZ-TDC005-4K` | |
| spot cabezal blanco | `TZ-TDC033-3K`, `TZ-TDC034-4K` | |
| spot cabezal platil | `TZ-TDC031-3K`, `TZ-TDC032-4K` | |
| plafón de aplicar redondo **blanco** | `TZ-TDC003-3K`, `TZ-TDC004-6K` | la planilla dice *Platil* |
| panel embutir redondo blanco | `TZ-PNR12V-3W-BL-3K`, `-6K` | |
| panel embutir redondo negro | `TZ-TDC011-3K`, `TZ-TDC014-6K` | es la misma foto que ya usamos en la lista de octubre |
| spot cabezal blanco *(repetida)* | `TZ-TDC018-4K` | **no coincide**: ese código es el minispot Ø20mm |

Faltan las de `TZ-TDC019-4K`, `TZ-TDC010-4K`, `TZ-MR16-5W-4K`, `TZ-MR16-7W-3K`,
`TZ-A6012V24V-9W-3K` y `-6K`.

**Platil = plateado**, acabado aluminio/acero: lo confirma la foto. En la fila «Color» de
la ficha va *Plateado*.

## Lo que falta antes de poder armar las fichas

Las diez fotos están y el cliente confirmó la asignación de SKU. Se verificó además que
las tres fuentes embebidas tienen todos los glifos de los textos nuevos, así que no hace
falta el recurso de incrustar Poppins aparte.

Lo único que falta son números de catálogo que la planilla no trae:

| ficha | se puede escribir hoy | falta |
|---|---|---|
| BULBO A60 12V/24V 9W | Potencia, Rosca, Tensión, Temperatura | flujo luminoso, apertura, CRI, vida útil, medidas |
| PLAFÓN Ø60 | Potencia, Tensión, Material, Medidas, Temperatura | flujo luminoso, apertura, CRI, IP |
| PANEL Ø83 BLANCO | Potencia, Tensión, Color, Medidas, Temperatura | flujo luminoso, apertura, CRI, IP, medida de corte |
| PANEL Ø70 NEGRO | Potencia, Tensión, Color, Medidas, Temperatura | flujo luminoso, apertura, CRI, IP |
| MINISPOT Ø20 | Potencia, Tensión, Material, Color, Medidas, Temperatura | flujo luminoso, apertura, CRI, IP |
| MR16 (amplía) | el 4000K no necesita nada: es el mismo 5W | lúmenes del 7W |
| SPOT CABEZAL (amplía) | los colores no necesitan nada | lúmenes de la versión de 2,5W |

Las medidas del panel Ø70 (Ø70 externo / Ø58 de corte / 12 mm de profundidad) y las del
minispot Ø20 (Ø20 exterior / 25 mm de profundidad / Ø15 de hueco) ya las había dado el
cliente cuando armamos la lista de octubre.

Si esos números no aparecen, las tablas salen de 4 a 6 filas. No desentona: la ficha de la
ESTACA SOLAR tiene 5.

**Ojo**: el pie «FICHA TÉCNICA AMPLIADA A CONFIRMAR» que aparece en la ficha del A60 al
extraer el texto **no se ve** — es texto enterrado de una corrección vieja. No sirve de
precedente para publicar una tabla incompleta.

## Pendientes que el cliente todavía no contestó

- Texto viejo enterrado en 13 de las 16 páginas de fichas (se copia y se busca, no se ve).
- La página de contacto dice `panailuminacion@hotmail.com` y mantiene el 11-4176-4205.
- `TZ-AR111-15W-4K DIM` y `TZ-MR11-3W-3K DIM` están en la lista y no en el catálogo.

## Estado: hecho

22 páginas. La auditoría cierra:

| control | resultado |
|---|---|
| folios | uno por página, de la 2 a la 21; portada y contacto sin número |
| índice contra páginas | las 31 filas caen en la página que dicen |
| códigos contra portadillas | LÁMPARAS 33 · ARTEFACTOS 32 · FUENTES 15 = 80 |
| diferencia contra el original | las páginas 1, 4, 6, 7, 8, 9, 10, 13 y 22 quedan idénticas al pixel; el resto, explicado |
| ficha mudada | el SPOT MINI pasa de la 14 a la 16 con **0 px de diferencia** |

### Las fotos: dos cosas que ensuciaron la página

- **El fondo de las fotos no es plano.** Las del plafón y el panel Ø83 traen un degradé de
  hasta nueve niveles, así que con un umbral fijo contra el blanco medio imagen entra como
  producto y, peor, a un producto **blanco sobre blanco** se le comen pedazos del aro: al
  panel Ø83 le quedaron manchones crema encima del marco. Lo que vale no es el valor sino
  la conexión: el fondo toca el borde de la imagen y el producto no. Ahora se saca la
  región parecida al borde **que llega hasta el borde**, y de lo que queda se conserva sólo
  la mancha más grande, porque son fotos de un solo objeto.
- **Afuera de la silueta hay que pintar el destino liso.** La cuenta que respeta el
  antialias sólo vale donde el píxel es mezcla de producto y fondo; aplicada afuera
  arrastra las sombras y los reflejos de la foto.
- **Y los paneles se repintan enteros, no hasta `dark_cover`.** Ese recorte existe para no
  pisar el logo, pero deja sin pintar la franja de arriba: ahí sobrevivía el borde de la
  foto vieja del SPOT MINI y quedaba un arco flotando sobre el plafón. Se repinta todo y se
  vuelve a colocar el logo.

### El gris del epígrafe depende del panel

El código bajo la foto va en `#c9c9c9` sobre los paneles oscuros y en **`#6d6d6d` sobre
los crema**. Usar el primero en los dos lados deja el SKU casi invisible: da 1,42:1 de
contraste contra el crema, cuando el mínimo legible para texto grande es 3:1. Con el gris
correcto queda en 4,44:1. La referencia está en el propio catálogo: el epígrafe de la
ESTACA SOLAR, que es original y va sobre crema, usa `#6d6d6d`.

### Lo que costó

- **La página 11.** El TUBO T5 ocupaba la hoja entera; su tabla, sus códigos y su pie caían
  por debajo del medio. Hubo que rearmar la ficha en el slot superior y espejar la mitad
  de abajo.
- **El logo de los paneles crema.** La primera versión lo traía dibujando `/S17` recortado
  a la caja del logo, como hace la página 17 del original. Se ve bien, pero **el recorte no
  saca el texto de la capa**: las páginas nuevas se llevaban entera la ficha de la estaca
  solar y su número. Ahora se arma con la máscara del logo y la tinta en el gris del
  documento.
- **Las correcciones no están sólo en los forms.** La página 14 traía en su propio stream
  la descripción reescrita del SPOT MINI y su pie de dos renglones. Copiando sólo el form,
  la ficha se mudaba con el texto viejo: daba 10.461 px de diferencia. Copiando también
  esos siete grupos, da 0.
- **`Stream.write(datos, filter=...)` espera los datos YA codificados.** Pasarle bytes
  crudos con `/FlateDecode` deja el stream ilegible.
- **El epígrafe no puede ir en la coordenada fija del slot** cuando la foto es alta: al
  tubo T5 le partía el cuerpo por la mitad.
- **Sin pérdida y a 900 px el archivo se iba a 12,9 MB.** Bajando cada foto a la resolución
  a la que de verdad se imprime quedan 8,5, contra 5,2 del original.

### Lo que queda pendiente

- **Texto viejo enterrado**: el catálogo venía con 12 páginas de 20 así y ahora son 16 de
  22. Lo que agregué son las fichas que tapé para reemplazarlas (el SPOT 12V viejo, el SPOT
  MINI debajo del plafón, el índice y las listas de portadilla anteriores). No se ve, pero
  sale al copiar y pegar y al buscar. `limpiar_capa_texto.py` de la skill lo resuelve; hay
  que pasarlo también por dentro de los forms.
- **Sin lúmenes** en las cinco fichas nuevas: el cliente no los tiene y no se derivan del
  vataje. Si aparecen, es agregar una fila.
- El plafón `TZ-TDC003` va sin fila de Color: la planilla lo llama «Platil» y la foto es
  blanca.
- `TZ-AR111-15W-4K DIM` y `TZ-MR11-3W-3K DIM` están en la lista de precios y no en el
  catálogo.
- La página de contacto sigue con `panailuminacion@hotmail.com` y el 11-4176-4205.
