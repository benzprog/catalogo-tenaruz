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

| foto | SKU |
|---|---|
| spot cabezal negro | `TZ-SPOT12V-3W-NG-3K`, `TZ-TDC005-4K` |
| spot cabezal blanco | `TZ-TDC033-3K`, `TZ-TDC034-4K` |
| spot cabezal platil | `TZ-TDC031-3K`, `TZ-TDC032-4K` |

**Platil = plateado**, acabado aluminio/acero: lo confirma la foto. En la fila «Color» de
la ficha va *Plateado*.

## Lo que falta antes de poder armar las fichas

- **CRI, flujo luminoso, apertura y grado IP** de los cinco productos nuevos. La planilla
  no los trae y no se inventan: si no están, esas filas no van.
- Las fotos **como archivo**. Las que llegan pegadas en el chat se ven pero no quedan en
  disco, y para montarlas sobre el panel hay que recortarlas contra su propio fondo.

## Pendientes que el cliente todavía no contestó

- Texto viejo enterrado en 13 de las 16 páginas de fichas (se copia y se busca, no se ve).
- La página de contacto dice `panailuminacion@hotmail.com` y mantiene el 11-4176-4205.
- `TZ-AR111-15W-4K DIM` y `TZ-MR11-3W-3K DIM` están en la lista y no en el catálogo.
