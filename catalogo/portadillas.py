"""Rehace las listas y los contadores de las portadillas de sección.

Las portadillas dibujan su contenido con un form escalado 1,9, así que un `/F11 12 Tf` de
adentro son `12 x 0,576271 x 1,9 = 13,139` pt en la página. Las listas se **redibujan
enteras** en coordenadas de página, no se les agregan renglones sueltos: en ARTEFACTOS las
cuatro fichas nuevas van en el medio y empujan a las que siguen, y además el original
compone glifo por glifo con sus propios desplazamientos, de modo que una línea agregada
nunca calza exactamente con las de al lado. Redibujando todas, todas quedan iguales.

El contador no se deduce: se cuenta contra los códigos que hay. LÁMPARAS pasa de 29 a 33
(MR16 4000K y 7W, más las dos del bulbo A60 12V/24V) y ARTEFACTOS de 18 a 32 (cinco del
spot cabezal, dos del plafón, dos y dos de los paneles y tres del minispot).
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from catalog import Catalog  # noqa: E402

ENTRADA = BASE / "_paso3.pdf"
SALIDA = BASE / "_paso4.pdf"

CUERPO = 13.139            # 12 pt dentro del form, por la escala global y el cm de 1,9
TRACKING = 1.1286
PASO = 26.28               # entre renglones de la lista
SALTO_CONTADOR = 51.47     # del último renglón al contador
GRIS_LISTA = (92, 92, 92)
GRIS_CONTADOR = (154, 154, 154)

PORTADILLAS = [
    # (índice de página, x, línea de base del primer renglón, tope del borrado, items, códigos)
    (2, 68.6593, 487.42, 505.0, [
        "DICROICA LED · GU10 7W",
        "MINIDICRO LED · GU10 3W",
        "MR16 LED · 12V 5W / 7W",
        "AR70 LED · GU10 7W DIMERIZABLE",
        "AR111 LED · GU10 15W",
        "PLL LED · 2G11 18W",
        "PLD LED · G24D 9W",
        "LED STICK T45 · E27 12W",
        "BIPIN COB · G4 12V 2W",
        "BIPIN LED · G4 12V 4W",
        "BIPIN COB · G9 220V 3W",
        "BIPIN LED · G9 220V 6W",
        "GOTA LED · E27 5W",
        "BULBO LED A60 · E27 12W DIMERIZABLE",
        "TUBO T5 LED · 18W 1149 mm",
        "BULBO A60 LED · E27 12V/24V 9W",
    ], 33),
    (11, 68.0600, 441.96, 460.0, [
        "SPOT FIJO EMBUTIR · COB 3W Ø38 mm",
        "SPOT MÓVIL EMBUTIR · COB 3W Ø52 mm",
        "SPOT · 12V MÓVIL 3W / 2,5W",
        "PLAFÓN LED · ALUMINIO 12V 2,5W Ø60 mm",
        "PANEL REDONDO · EMBUTIR 12V 3W Ø83 mm BLANCO",
        "PANEL REDONDO · EMBUTIR 12V 3W Ø70 mm NEGRO",
        "MINISPOT COB · ALUMINIO 12V 1W Ø20 mm",
        "SPOT MINI EMBUTIR · REDONDO PARA MINIDICROICA",
        "REFLECTOR EXTERIOR · LED 12V · IP65",
        "APLIQUE CURVO · EXTERIOR GU10 · IP65",
        "APLIQUE RECTO · EXTERIOR GU10 · IP65",
        "ESTACA ALUMINIO · 1 x GU10 · IP67",
        "ESTACA SOLAR LED · 28 LED · IP67",
    ], 32),
]


def main(entrada=ENTRADA, salida=SALIDA):
    cat = Catalog(str(entrada))
    for indice, x, y0, tope, items, codigos in PORTADILLAS:
        pagina = cat.pdf.pages[indice]
        for texto in items + [f"{codigos} CÓDIGOS"]:
            faltan = cat.check_glyphs(texto, "/F11")
            if faltan:
                raise SystemExit(f"faltan glifos {faltan} para {texto!r}")

        frag = [cat.rect(40.0, 18.0, 540.0, tope - 18.0, cat.CREAM)]
        y = y0
        for texto in items:
            frag.append(cat.show(texto, "/F11", CUERPO, x, y, TRACKING, GRIS_LISTA))
            y -= PASO
        y += PASO - SALTO_CONTADOR
        frag.append(cat.show(f"{codigos} CÓDIGOS", "/F11", CUERPO, x, y, TRACKING,
                             GRIS_CONTADOR))
        if y < 34.0:
            raise SystemExit(f"pág {indice+1}: el contador queda en y={y:.1f}, muy al pie")
        print(f"pág {indice+1}: {len(items)} renglones, contador {codigos} en y={y:.2f}")
        cat.append(pagina, "\n".join(frag))

    cat.save(str(salida))
    print(f"guardado {salida}")
    return salida


if __name__ == "__main__":
    main()
