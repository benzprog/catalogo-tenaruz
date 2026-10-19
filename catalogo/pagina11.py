"""Página 11: el TUBO T5 pasa al slot superior y abajo entra el bulbo A60 12V/24V.

Hoy la 11 es una ficha sola con los paneles a toda altura —blanco a la izquierda, oscuro a
la derecha—, que es el patrón del catálogo para una media página libre. Meter una ficha
abajo obliga a dos cosas:

1. **Rearmar el TUBO T5 dentro del slot superior.** No alcanza con repintar la mitad de
   abajo: la ficha estaba compuesta a lo alto de la hoja y su tabla, sus códigos y su pie
   caían por debajo del medio. Se vuelve a dibujar con la grilla del slot, y la foto del
   tubo se recoloca —no se vuelve a embeber— porque su fondo oscuro ya viene en el JPEG.
2. **Espejar la mitad de abajo**: el panel oscuro pasa a la izquierda y el blanco a la
   derecha, como en cualquier slot inferior. El panel oscuro nuevo queda sin logo, porque
   el de la página vive arriba a la derecha, así que se recoloca el mismo XObject (`/Im9`,
   la versión blanca) en `BOTTOM.logo_pos`.

El recuadro del folio viaja dentro del panel blanco del slot inferior: al repintarlo se
borra, así que se vuelve a pintar con su número.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from catalog import BOTTOM, TOP, Catalog  # noqa: E402
from construir import ORIGEN, ficha, recuadro_numero  # noqa: E402
from recorte import NEGRO  # noqa: E402

TUBO = {
    "clave": "T5",
    "titulo": "TUBO T5 LED",
    "subtitulo": "18W 1149 mm",
    "descripcion": "Reemplazo de los fluorescentes T5, con conexión a una punta directo "
                   "a 220V. Se diferencia del T8 tradicional por su diámetro menor.",
    "filas": [
        ("Potencia", "18W"), ("Zócalo", "G5"), ("Cuerpo", "Vidrio opalino"),
        ("Flujo luminoso", "2050 lm"), ("Eficiencia", "113,88 lm/W"),
        ("Apertura", "120°"), ("Vida útil", "19.999 hs"), ("Corriente", "0,15 A"),
        ("Tensión", "220-240V"), ("Medidas", "1149 x Ø16 mm"),
    ],
    "codigos": [("TZ-T5-18W-4K", "4000K NEUTRO")],
    "pie": ["LIQUIDACIÓN", "BULTO CERRADO x 40"],
    "fotos": [("/Im120", "TZ-T5-18W-4K")],
    "medida_foto": (102, 992),
}

A60 = {
    "clave": "A60",
    "titulo": "BULBO A60 LED",
    "subtitulo": "E27 12V/24V 9W",
    "descripcion": "Bulbo A60 para instalaciones de 12 y 24 volts: paneles solares, "
                   "embarcaciones y motorhome. Misma rosca E27, sin inversor.",
    "filas": [
        ("Potencia", "9W"),
        ("Rosca", "E27"),
        ("Tensión", "DC 12V / 24V"),
        ("Temperatura", "3000K / 6000K"),
    ],
    "codigos": [("TZ-A6012V24V-9W-3K", "3000K CÁLIDO"),
                ("TZ-A6012V24V-9W-6K", "6000K FRÍO")],
    "pie": ["BULTO CERRADO x 100"],
    "fotos": [("bulbo-a60-12v24v.webp", "TZ-A6012V24V-9W-3K")],
    "ancho_foto": 150.0,
}


def main(entrada=BASE / "_paso0.pdf", salida=BASE / "_paso1.pdf"):
    cat = Catalog(str(entrada))
    pagina = cat.pdf.pages[10]

    frag = ficha(cat, pagina, TOP, TUBO, NEGRO)
    frag.append(cat.rect(*BOTTOM.dark_panel, NEGRO))      # espejar la mitad de abajo
    frag += ficha(cat, pagina, BOTTOM, A60, NEGRO)
    frag.append(cat.place("/Im9", *BOTTOM.logo_pos))      # el logo blanco de esta página
    recuadro_numero(cat, frag, BOTTOM, "11")

    cat.append(pagina, "\n".join(frag))
    cat.save(str(salida))
    print(f"guardado {salida}")
    return salida


if __name__ == "__main__":
    main()
