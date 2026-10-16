"""ARTEFACTOS: entran cuatro fichas nuevas de 12V y la sección corre dos páginas.

Las cuatro van **detrás del SPOT 12V**, para que el bloque de 12 volts se lea junto. Cuatro
fichas son exactamente cuatro slots, o sea dos páginas enteras: por eso todo lo que corre
conserva su mitad —lo de arriba sigue arriba, lo de abajo sigue abajo— y **ningún panel
necesita espejarse**.

Las páginas de esta sección no tienen su contenido en el stream: lo dibujan con Form
XObjects compartidos (la 14 usa `/S14` y `/S15`, la 15 usa `/S15` y `/S16`...). Así que la
ficha del SPOT MINI, que baja de la 14 a la 16, **no se redibuja**: se repiten los mismos
operadores de recorte y traslación sobre la página nueva. Tipografía, fotos y colores
quedan exactos porque son literalmente el mismo dibujo.

El logo oscuro de los paneles crema tampoco es una imagen suelta: vive dentro de `/S17`, en
la posición del slot inferior. Para ponerlo donde haga falta se recorta a la caja del logo
y se dibuja el form trasladado, que es como lo resuelve la página 17 del original.
"""
import pathlib
import sys

import re
import zlib

import pikepdf

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from catalog import BOTTOM, TOP, Catalog  # noqa: E402
from construir import ficha, recuadro_numero  # noqa: E402
from recorte import CREMA  # noqa: E402

ENTRADA = BASE / "_paso1.pdf"
SALIDA = BASE / "TZ-Importado_Catalogo.pdf"

# ── las fichas ───────────────────────────────────────────────────────────────
SPOT12V = {
    "clave": "SPOT12V",
    "titulo": "SPOT",
    "subtitulo": "12V MÓVIL 3W / 2,5W",
    "descripcion": "Mini cabezal orientable de 12V para iluminación decorativa de "
                   "precisión, con articulación. En negro, blanco y plateado.",
    "filas": [
        # sin "Color de luz": con seis códigos la tabla de diez filas empuja el último
        # subcódigo sobre el pie, y la temperatura ya la dice cada subcódigo
        ("Potencia", "3W / 2,5W"),
        ("Tensión", "DC 12V"), ("CRI", "≥80 Ra"), ("Flujo luminoso", "240 lm (3W)"),
        ("Apertura", "30°"), ("Protección", "IP20"), ("Material", "Aluminio"),
        ("Color", "Negro / Blanco / Plateado"), ("Medidas", "Ø25 x 50 mm"),
    ],
    "codigos": [("TZ-SPOT12V-3W-NG-3K", "3W 3000K NEGRO"),
                ("TZ-TDC033-3K", "3W 3000K BLANCO"),
                ("TZ-TDC031-3K", "3W 3000K PLATEADO"),
                ("TZ-TDC005-4K", "2,5W 4000K NEGRO"),
                ("TZ-TDC034-4K", "2,5W 4000K BLANCO"),
                ("TZ-TDC032-4K", "2,5W 4000K PLATEADO")],
    "pie": ["PRESENTACIÓN: CAJA INDIVIDUAL"],
    "fotos": [("spot-cabezal-negro.webp", "TZ-SPOT12V-3W-NG-3K"),
              ("spot-cabezal-blanco.png", "TZ-TDC033-3K"),
              ("spot-cabezal-platil.png", "TZ-TDC031-3K")],
    "ancho_foto": 120.0,
}

# El plafón no lleva fila de Color: la planilla lo llama «Platil» y la foto que mandó el
# cliente es blanca. Antes que afirmar un color que la foto desmiente, no se afirma.
PLAFON = {
    "clave": "PLAFON",
    "titulo": "PLAFÓN LED",
    "subtitulo": "ALUMINIO 12V 2,5W Ø60 mm",
    "descripcion": "Plafón de aplicar en aluminio para 12V, de perfil muy bajo. Para "
                   "embarcaciones, motorhome y mobiliario.",
    "filas": [
        ("Potencia", "2,5W"), ("Tensión", "DC 12V"),
        ("Temperatura", "3000K / 6000K"), ("Material", "Aluminio"),
        ("Medidas", "Ø60 x 8 mm"),
    ],
    "codigos": [("TZ-TDC003-3K", "3000K CÁLIDO"), ("TZ-TDC004-6K", "6000K FRÍO")],
    "pie": ["BULTO CERRADO x 50"],
    "fotos": [("plafon-o60.png", "TZ-TDC003-3K")],
    "ancho_foto": 170.0,
}

PANEL83 = {
    "clave": "PANEL83",
    "titulo": "PANEL REDONDO",
    "subtitulo": "EMBUTIR 12V 3W Ø83 mm · BLANCO",
    "descripcion": "Panel redondo de embutir para 12V, de bajo perfil y luz difusa "
                   "pareja. Marco blanco, pensado para cielorrasos de motorhome, "
                   "trailers y embarcaciones.",
    "filas": [
        ("Potencia", "3W"), ("Tensión", "DC 12V"),
        ("Temperatura", "3000K / 6000K"), ("Color", "Blanco"),
        ("Medidas", "Ø83 mm"),
    ],
    "codigos": [("TZ-PNR12V-3W-BL-3K", "3000K CÁLIDO"),
                ("TZ-PNR12V-3W-BL-6K", "6000K FRÍO")],
    "pie": ["BULTO CERRADO x 100"],
    "fotos": [("panel-embutir-o83-blanco.png", "TZ-PNR12V-3W-BL-3K")],
    "ancho_foto": 180.0,
}

PANEL70 = {
    "clave": "PANEL70",
    "titulo": "PANEL REDONDO",
    "subtitulo": "EMBUTIR 12V 3W Ø70 mm · NEGRO",
    "descripcion": "La misma línea de paneles en marco negro y diámetro menor. Corte de "
                   "Ø58 mm y sólo 12 mm de profundidad.",
    "filas": [
        ("Potencia", "3W"), ("Tensión", "DC 12V"),
        ("Temperatura", "3000K / 6000K"), ("Color", "Negro"),
        ("Medidas", "Ø70 x 12 mm"), ("Corte", "Ø58 mm"),
    ],
    "codigos": [("TZ-TDC011-3K", "3000K CÁLIDO"), ("TZ-TDC014-6K", "6000K FRÍO")],
    "pie": ["BULTO CERRADO x 50"],
    "fotos": [("panel-embutir-o70-negro.png", "TZ-TDC011-3K")],
    "ancho_foto": 180.0,
}

MINISPOT = {
    "clave": "MINISPOT",
    "titulo": "MINISPOT COB",
    "subtitulo": "ALUMINIO 12V 1W Ø20 mm",
    "descripcion": "Minispot de embutir de 1W con clips de resorte. Veinte milímetros de "
                   "diámetro para mobiliario, vitrinas y cielorrasos de poca "
                   "profundidad.",
    "filas": [
        ("Potencia", "1W"), ("Tensión", "DC 12V"), ("Temperatura", "4000K"),
        ("Material", "Aluminio"), ("Color", "Blanco / Negro / Plateado"),
        ("Medidas", "Ø20 x 25 mm"), ("Hueco", "Ø15 mm"),
    ],
    "codigos": [("TZ-TDC018-4K", "4000K BLANCO"), ("TZ-TDC019-4K", "4000K NEGRO"),
                ("TZ-TDC010-4K", "4000K PLATEADO")],
    "pie": ["BULTO CERRADO x 9"],
    "fotos": [("minispot-o20-blanco.png", "TZ-TDC018-4K"),
              ("minispot-o20-negro.webp", "TZ-TDC019-4K"),
              ("minispot-o20-platil.png", "TZ-TDC010-4K")],
    "ancho_foto": 110.0,
}


def logo_oscuro(pdf, pagina, slot, fuente):
    """Coloca el logo TENARUZ en su versión oscura, la de los paneles crema.

    La primera versión lo traía dibujando `/S17` recortado a la caja del logo, como hace la
    página 17 del original. Se ve bien, pero **el recorte no saca el texto de la capa**: la
    página se llevaba entera la ficha de la estaca solar y su número de página, y aparecían
    al copiar y pegar.

    El logo es monocromo —tinta blanca más una máscara de transparencia—, así que se arma
    uno nuevo con la misma máscara y la tinta en el gris oscuro del documento. La silueta
    es exactamente la misma porque la máscara es la misma.
    """
    nombre = "/ImLogoOsc"
    recursos = pagina.obj["/Resources"]
    if "/XObject" not in recursos:
        recursos["/XObject"] = pikepdf.Dictionary()
    if nombre not in recursos["/XObject"]:
        mascara = fuente["/SMask"]
        ancho, alto = int(fuente.Width), int(fuente.Height)
        tinta = pikepdf.Stream(pdf, zlib.compress(bytes([26, 26, 26]) * (ancho * alto), 9))
        tinta.Type, tinta.Subtype = pikepdf.Name.XObject, pikepdf.Name.Image
        tinta.Width, tinta.Height = ancho, alto
        tinta.ColorSpace, tinta.BitsPerComponent = pikepdf.Name.DeviceRGB, 8
        tinta.Filter = pikepdf.Name.FlateDecode
        tinta.SMask = mascara
        recursos["/XObject"][nombre] = pdf.make_indirect(tinta)
    x, y, w, h = slot.logo_pos
    return f"q {w} 0 0 {h} {x} {y} cm {nombre} Do Q"


def correcciones(pagina, x_min=306.0, y_max=396.0):
    """Los operadores de corrección de la página que caen en la mitad inferior.

    No alcanza con repetir el dibujo del form: la página 14 trae en su propio stream las
    correcciones de contenido que se le hicieron después —la descripción reescrita del SPOT
    MINI y su pie de dos renglones—. Copiando sólo el form, la ficha se mudaba con el texto
    viejo. Se copian los grupos `q ... Q` cuyas coordenadas caen en la mitad de abajo, tal
    cual están, para que el dibujo sea el mismo.
    """
    datos = pagina.obj["/Contents"]
    flujos = list(datos) if isinstance(datos, pikepdf.Array) else [datos]
    salida = []
    for f in flujos:
        crudo = bytes(f.read_bytes()).decode("latin-1")
        # se buscan los grupos `q ... Q` sin otro `q` adentro: son las tapas y los bloques
        # de texto sueltos. Los de afuera envuelven el stream entero y no sirven de filtro.
        pila = []
        for m in re.finditer(r"[qQ]", crudo):
            if m.group() == "q":
                pila.append(m.start())
                continue
            if not pila:
                continue
            a = pila.pop()
            if any(crudo.find("q", a + 1, m.start()) > 0 for _ in (0,)) and \
                    "q" in crudo[a + 1:m.start()]:
                continue                              # tiene grupos adentro: no es hoja
            grupo = crudo[a:m.end()]
            if "Do" in grupo:                         # los form se dibujan aparte
                continue
            # El ancla de un bloque de texto es su PRIMER Td: los que siguen son avances
            # relativos de cada glifo, con x chiquita, y arruinaban el filtro. En un
            # rectángulo, los dos primeros números son la esquina, no el tamaño.
            if "BT" in grupo:
                m0 = re.search(r"([\d.]+)\s+([\d.]+)\s+Td", grupo)
                ancla = (float(m0.group(1)), float(m0.group(2))) if m0 else None
            else:
                m0 = re.search(r"([\d.]+)\s+([\d.]+)\s+[\d.]+\s+[\d.]+\s+re", grupo)
                ancla = (float(m0.group(1)), float(m0.group(2))) if m0 else None
            if ancla is None or ancla[0] > 570:       # el recuadro del folio se repinta aparte
                continue
            if ancla[0] >= x_min and ancla[1] < y_max:
                salida.append(grupo)
    return salida


def pagina_nueva(pdf, modelo):
    """Una página en blanco con la caja, los recursos y el grupo de otra."""
    obj = pikepdf.Dictionary(
        Type=pikepdf.Name.Page,
        MediaBox=modelo.obj["/MediaBox"],
        Resources=pikepdf.Dictionary(
            Font=modelo.obj["/Resources"]["/Font"],
            XObject=pikepdf.Dictionary()),
        Contents=pdf.make_stream(b" "),
    )
    if "/Group" in modelo.obj:
        obj["/Group"] = modelo.obj["/Group"]
    return pikepdf.Page(pdf.make_indirect(obj))


def paneles(cat, arriba_crema_derecha=True):
    """Los cuatro paneles de una página de ARTEFACTOS, en su disposición de siempre."""
    return [
        cat.rect(*TOP.white_panel, Catalog.WHITE),
        cat.rect(*TOP.dark_panel, CREMA),
        cat.rect(*BOTTOM.dark_panel, CREMA),
        cat.rect(*BOTTOM.white_panel, Catalog.WHITE),
    ]


def main(entrada=ENTRADA, salida=SALIDA):
    cat = Catalog(str(entrada))
    pdf = cat.pdf

    p14 = pdf.pages[13]
    forms = p14.obj["/Resources"]["/XObject"]
    s15 = forms["/S15"]                      # trae la ficha del SPOT MINI
    logo = pdf.pages[16].obj["/Resources"]["/XObject"]["/ImLogo"]   # logo con su máscara

    # hay que leerlas antes de tocar la 14, que se repinta
    correcciones_14 = correcciones(p14)
    print(f"  correcciones de la mitad inferior de la 14 que se mudan: {len(correcciones_14)}")

    nuevas = [pagina_nueva(pdf, p14) for _ in range(2)]
    for n, pg in enumerate(nuevas):
        pg.obj["/Resources"]["/XObject"]["/S15"] = s15
        pdf.pages.insert(14 + n, pg)

    p15, p16 = pdf.pages[14], pdf.pages[15]

    # ── página 14: el SPOT 12V se rehace con sus seis códigos, y abajo entra el plafón
    frag = ficha(cat, p14, TOP, SPOT12V, CREMA)
    frag += ficha(cat, p14, BOTTOM, PLAFON, CREMA)
    frag.append(logo_oscuro(pdf, p14, BOTTOM, logo))   # el panel de abajo se repintó entero
    recuadro_numero(cat, frag, BOTTOM, "14")
    cat.append(p14, "\n".join(frag))

    # ── página 15 nueva: los dos paneles redondos
    frag = paneles(cat)
    frag += ficha(cat, p15, TOP, PANEL83, CREMA) + [logo_oscuro(pdf, p15, TOP, logo)]
    frag += ficha(cat, p15, BOTTOM, PANEL70, CREMA) + [logo_oscuro(pdf, p15, BOTTOM, logo)]
    recuadro_numero(cat, frag, BOTTOM, "15")
    cat.append(p15, "\n".join(frag))

    # ── página 16 nueva: el minispot arriba y, abajo, el SPOT MINI que baja de la 14.
    #    No se redibuja: se repiten los operadores con que la 14 lo dibujaba.
    frag = paneles(cat)
    frag += ficha(cat, p16, TOP, MINISPOT, CREMA) + [logo_oscuro(pdf, p16, TOP, logo)]
    frag += ["q 306 0 306 396 re W n 1 0 0 1 306 -396 cm /S15 Do Q",
             "q 0 0 306 396 re W n 1 0 0 1 -306 -396 cm /S15 Do Q"]
    frag += correcciones_14
    recuadro_numero(cat, frag, BOTTOM, "16")
    cat.append(p16, "\n".join(frag))

    # ── renumerar lo que corrió: viejas 15..19 -> 17..21. La de contacto no lleva número.
    for indice, numero in zip(range(16, 21), range(17, 22)):
        frag = []
        recuadro_numero(cat, frag, BOTTOM, str(numero))
        cat.append(pdf.pages[indice], "\n".join(frag))

    cat.save(str(salida))
    print(f"guardado {salida} ({len(pdf.pages)} páginas)")
    return salida


if __name__ == "__main__":
    main()
