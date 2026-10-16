"""La ficha del MR16 suma el 4000K y la versión de 7W.

Se rehace sólo la mitad blanca: el panel oscuro lleva los bloques de variante con el halo
de cada temperatura, y redibujarlos a mano nunca queda igual. Queda con cuatro códigos y
dos bloques, que es lo mismo que hace el REFLECTOR —cuatro códigos, dos fotos—.

El flujo luminoso queda aclarado como «350 lm (5W)»: es el dato publicado del de 5W y del
de 7W no hay medición. Inventarlo a partir del vataje no se puede, porque falta la eficacia
del LED.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from catalog import TOP, Catalog  # noqa: E402
from construir import ficha  # noqa: E402
from recorte import NEGRO  # noqa: E402

ENTRADA = BASE / "_paso4.pdf"
SALIDA = BASE / "_paso5.pdf"

MR16 = {
    "clave": "MR16",
    "titulo": "MR16 LED",
    "subtitulo": "12V 5W / 7W",
    "descripcion": "Reemplazo de la dicroica halógena de 12V. Funciona con corriente "
                   "alterna y continua, apta para instalaciones a 12V: paneles solares, "
                   "embarcaciones y motorhome.",
    "filas": [
        ("Potencia", "5W / 7W"), ("Zócalo", "GU5.3"),
        ("Flujo luminoso", "350 lm (5W)"), ("Apertura", "38°"), ("CRI", "≥80 Ra"),
        ("Tipo de LED", "SMD 2835"), ("Vida útil", "25.000 hs"),
        ("Corriente", "≤400 mA"), ("Tensión", "12V"), ("Medidas", "Ø50 x 49 mm"),
    ],
    "codigos": [("TZ-MR16-5W-3K", "5W 3000K"), ("TZ-MR16-5W-4K", "5W 4000K"),
                ("TZ-MR16-5W-6K", "5W 6000K"), ("TZ-MR16-7W-3K", "7W 3000K")],
    "pie": ["BULTO CERRADO x 100"],
    "fotos": [],
}


def main(entrada=ENTRADA, salida=SALIDA):
    cat = Catalog(str(entrada))
    pagina = cat.pdf.pages[4]
    cat.append(pagina, "\n".join(ficha(cat, pagina, TOP, MR16, NEGRO, solo_blanco=True)))
    cat.save(str(salida))
    print(f"guardado {salida}")
    return salida


if __name__ == "__main__":
    main()
