# Páginas que faltan diseñar

El cliente las va generando; cuando avise **LISTO** se vuelve a correr `armar.py` y la
paginación y el índice se recalculan solos.

**Van 29 de las 30 fichas. Falta 1.**

| # | ficha | sección | estado |
|---|---|---|---|
| 01 | **DICROICA LED GU10 7W** | LÁMPARAS | **falta** |
| 22 | PANEL REDONDO EMBUTIR 12V 3W Ø70 mm NEGRO | ARTEFACTOS | recibida · 96 dpi |
| 23 | SPOT MINI EMBUTIR REDONDO PARA MINIDICROICA | ARTEFACTOS | recibida · 90 dpi |
| 24 | MINISPOT COB ALUMINIO 12V 1W Ø20 mm | ARTEFACTOS | recibida · 121 dpi |
| 25 | REFLECTOR EXTERIOR LED 12V · IP65 | ARTEFACTOS | recibida · **218 dpi** |
| 26 | APLIQUE CURVO EXTERIOR GU10 · IP65 | ARTEFACTOS | recibida · 90 dpi |
| 27 | APLIQUE RECTO EXTERIOR GU10 · IP65 | ARTEFACTOS | recibida · 90 dpi |
| 28 | ESTACA ALUMINIO 1 x GU10 · IP67 | ARTEFACTOS | recibida · 94 dpi |
| 29 | ESTACA SOLAR LED 28 LED · IP67 | ARTEFACTOS | recibida · 90 dpi |

## Códigos verificados contra la planilla

| página | códigos | resultado |
|---|---|---|
| 22 | `TZ-TDC011-3K`, `TZ-TDC014-6K` | están, y son el Ø70 negro |
| 24 | `TZ-TDC018-4K`, `TZ-TDC019-4K`, `TZ-TDC010-4K` | están; blanco, negro y plateado en su lugar |
| 25 | `TZ-FL12V-10W-3K`, `TZ-FL12V-30W-6K` | están |
| 28 | `TZ-ESTAL-GU10`, `TZ-ESTAL-GU10-MINI` | están |
| 29 | `TZ-SLS007-3K` | está |
| 23 | `TZ-SPOTMINI-BL`, `TZ-SPOTMINI-NG` | están, y coinciden medidas y «sin zócalo» |

## Resolución: dispar

El generador no da un tamaño parejo. Medido como dpi efectivo al encajar cada media página
en A4:

- **218 dpi** — REFLECTOR EXTERIOR (3600 x 2546). La mejor de todas, y la única que se
  acerca a calidad de imprenta.
- **121 dpi** — MINISPOT COB.
- **90 a 98 dpi** — las 21 del ZIP y las otras tres nuevas.

Mientras el catálogo mezcle 90 y 218, la diferencia se va a notar al pasar de una página a
otra. Si se quiere parejo hay que regenerar las viejas al tamaño de la del REFLECTOR, que
es lo que conviene averiguar: qué se hizo distinto en esa.

Las que no vienen en proporción A4 no se estiran: entran enteras y el sobrante se rellena
con el color del borde de la propia imagen. Hoy son la 08, 18, 22 y 28.
