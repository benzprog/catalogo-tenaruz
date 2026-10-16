"""Rehace el índice entero con las cinco fichas nuevas y la paginación corrida.

Se redibuja completo en vez de insertar filas: la página ya venía con capas encimadas de
ediciones anteriores y sumar otra sólo empeora la capa de texto. El paso se reparte entre
las filas que haya, así que al pasar de 26 a 31 entradas se achica solo.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from catalog import Catalog  # noqa: E402

ARCHIVO = BASE / "TZ-Importado_Catalogo.pdf"

# medido sobre el índice original
X_TITULO = 68.03
X_NUMERO = 543.55          # los números van alineados a la derecha
RULE_X = (68.04, 543.60)
RULE_DY = 9.47
Y_INICIO = 604.00          # línea de base del primer encabezado de sección
Y_FINAL = 24.98
SALTO_ENCABEZADO = 23.05
SALTO_SECCION = 32.00
GRIS_NUMERO = (154, 154, 154)

SECCIONES = [
    ("LÁMPARAS Y TUBOS LED", [
        ("DICROICA LED GU10 7W", 4),
        ("MINIDICRO LED GU10 3W", 4),
        ("MR16 LED 12V 5W / 7W", 5),
        ("AR70 LED GU10 7W DIMERIZABLE", 5),
        ("AR111 LED GU10 15W", 6),
        ("PLL LED 2G11 18W", 6),
        ("PLD LED G24D 9W", 7),
        ("LED STICK T45 E27 12W", 7),
        ("BIPIN COB G4 12V 2W", 8),
        ("BIPIN LED G4 12V 4W", 8),
        ("BIPIN COB G9 220V 3W", 9),
        ("BIPIN LED G9 220V 6W", 9),
        ("GOTA LED E27 5W", 10),
        ("BULBO LED A60 E27 12W DIMERIZABLE", 10),
        ("TUBO T5 LED 18W 1149 mm", 11),
        ("BULBO A60 LED E27 12V/24V 9W", 11),
    ]),
    ("ARTEFACTOS", [
        ("SPOT FIJO EMBUTIR COB 3W Ø38 mm", 13),
        ("SPOT MÓVIL EMBUTIR COB 3W Ø52 mm", 13),
        ("SPOT 12V MÓVIL 3W / 2,5W", 14),
        ("PLAFÓN LED ALUMINIO 12V 2,5W Ø60 mm", 14),
        ("PANEL REDONDO EMBUTIR 12V 3W Ø83 mm BLANCO", 15),
        ("PANEL REDONDO EMBUTIR 12V 3W Ø70 mm NEGRO", 15),
        ("MINISPOT COB ALUMINIO 12V 1W Ø20 mm", 16),
        ("SPOT MINI EMBUTIR REDONDO PARA MINIDICROICA", 16),
        ("REFLECTOR EXTERIOR LED 12V · IP65", 17),
        ("APLIQUE CURVO EXTERIOR GU10 · IP65", 17),
        ("APLIQUE RECTO EXTERIOR GU10 · IP65", 18),
        ("ESTACA ALUMINIO 1 x GU10 · IP67", 18),
        ("ESTACA SOLAR LED 28 LED · IP67", 19),
    ]),
    ("FUENTES SWITCHING", [
        ("FUENTE SWITCHING METÁLICA SLIM 12V", 21),
        ("FUENTE SWITCHING METÁLICA SLIM 24V", 21),
    ]),
]


def main(entrada=ARCHIVO, salida=BASE / "_paso3.pdf"):
    cat = Catalog(str(entrada))
    pagina = cat.pdf.pages[1]

    filas = sum(len(f) for _, f in SECCIONES)
    saltos = filas - len(SECCIONES)
    fijo = SALTO_ENCABEZADO * len(SECCIONES) + SALTO_SECCION * (len(SECCIONES) - 1)
    paso = (Y_INICIO - Y_FINAL - fijo) / saltos
    print(f"{filas} fichas en {len(SECCIONES)} secciones -> paso {paso:.2f} pt")

    for texto, recurso in ([(t, "/F20") for t, _ in SECCIONES]
                           + [(t, "/F11") for _, f in SECCIONES for t, _ in f]):
        faltan = cat.check_glyphs(texto, recurso)
        if faltan:
            raise SystemExit(f"faltan glifos {faltan} en {recurso} para {texto!r}")

    frag = [cat.rect(60.0, 0.0, 552.0, 606.0, cat.WHITE)]     # borra el bloque entero
    y = Y_INICIO
    for i, (encabezado, items) in enumerate(SECCIONES):
        if i:
            y -= SALTO_SECCION
        frag.append(cat.show(encabezado, "/F20", 6.34, X_TITULO, y, 1.595, cat.BODY))
        frag.append(cat.rule(*RULE_X, y - RULE_DY))
        y -= SALTO_ENCABEZADO
        for j, (titulo, num) in enumerate(items):
            if j:
                y -= paso
            if cat.advance(titulo, "/F11", 7.49, -0.004) > X_NUMERO - X_TITULO - 24:
                raise SystemExit(f"{titulo!r} se pasa de la columna del índice")
            frag.append(cat.show(titulo, "/F11", 7.49, X_TITULO, y, -0.004, cat.BODY))
            frag.append(cat.show_right(str(num), "/F11", 6.34, X_NUMERO, y, 0.0,
                                       GRIS_NUMERO))
            frag.append(cat.rule(*RULE_X, y - RULE_DY))
    # la tapa llega hasta abajo y se come el recuadro del folio: se repinta
    frag.append(cat.rect(579.5, -1.0, 34.0, 36.0, cat.TITLE))
    frag.append(cat.show_center("2", "/F11", 6.34, 596.5, 14.61, 0.0, cat.WHITE))
    print(f"última línea de base: {y:.2f} (objetivo {Y_FINAL})")

    cat.append(pagina, "\n".join(frag))
    cat.save(str(salida))
    print(f"guardado {salida}")
    return salida


if __name__ == "__main__":
    main()
