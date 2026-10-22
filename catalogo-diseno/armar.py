"""Arma el catálogo de diseño en PDF a partir de las páginas ya diseñadas.

    python3 -I catalogo-diseno/armar.py

Cada archivo de `paginas/` es un **pliego de dos páginas A4 verticales** pegadas lado a
lado, así que se parte al medio y cada mitad va a una página del PDF. El orden es el del
catálogo técnico (`catalogo/TZ-Importado_Catalogo.pdf`), y de ahí sale también el índice.

Dos archivos vienen en un lienzo que no es A4 —el LED STICK en 4:3 y el SPOT MÓVIL en
5:3—. Esos no se estiran: se encajan enteros respetando su proporción y el sobrante se
rellena con el color del borde de la propia imagen, que en estas páginas es blanco, así
que la junta no se ve. Deformarlos para que entren sería lo único que se nota de verdad.

Tapa, índice y portadillas se componen acá con texto real, no con imágenes: son las únicas
páginas que no vinieron diseñadas. La tipografía es Outfit, que es la que usan los títulos
de las páginas generadas.
"""
import io
import pathlib
import sys
import zlib

import numpy as np
import pikepdf
from fontTools.ttLib import TTFont
from PIL import Image
from pikepdf import Array, Dictionary, Name, Stream

BASE = pathlib.Path(__file__).resolve().parent
PAGINAS = BASE / "paginas"
SALIDA = BASE / "CATALOGO_TENARUZ_DISENO.pdf"
CATALOGO = BASE.parent / "catalogo" / "TZ-Importado_Catalogo.pdf"
TIPOS = pathlib.Path("/mnt/skills/examples/canvas-design/canvas-fonts")

ANCHO, ALTO = 595.276, 841.890        # A4 vertical, en puntos
MARGEN = 56.0
TINTA = (0.10, 0.10, 0.10)
GRIS = (0.45, 0.45, 0.45)
LINEA = (0.80, 0.80, 0.80)

# Las 31 fichas del catálogo técnico, en orden. `None` = todavía no está diseñada.
FICHAS = [
    ("LÁMPARAS Y TUBOS LED", "DICROICA LED", "GU10 7W", None),
    ("LÁMPARAS Y TUBOS LED", "MINIDICRO LED", "GU10 3W", "02"),
    ("LÁMPARAS Y TUBOS LED", "MR16 LED", "12V 5W / 7W", "03"),
    ("LÁMPARAS Y TUBOS LED", "AR70 LED", "GU10 7W DIMERIZABLE", "04"),
    ("LÁMPARAS Y TUBOS LED", "AR111 LED", "GU10 15W", "05"),
    ("LÁMPARAS Y TUBOS LED", "PLL LED", "2G11 18W", "06"),
    ("LÁMPARAS Y TUBOS LED", "PLD LED", "G24D 9W", "07"),
    ("LÁMPARAS Y TUBOS LED", "LED STICK T45", "E27 12W", "08"),
    ("LÁMPARAS Y TUBOS LED", "BIPIN COB", "G4 12V 2W", "09"),
    ("LÁMPARAS Y TUBOS LED", "BIPIN LED", "G4 12V 4W", "10"),
    ("LÁMPARAS Y TUBOS LED", "BIPIN COB", "G9 220V 3W", "11"),
    ("LÁMPARAS Y TUBOS LED", "BIPIN LED", "G9 220V 6W", "12"),
    ("LÁMPARAS Y TUBOS LED", "GOTA LED", "E27 5W", "13"),
    ("LÁMPARAS Y TUBOS LED", "BULBO LED A60", "E27 12W DIMERIZABLE", "14"),
    ("LÁMPARAS Y TUBOS LED", "TUBO T5 LED", "18W 1149 mm", "15"),
    ("LÁMPARAS Y TUBOS LED", "BULBO A60 LED", "E27 12V/24V 9W", "16"),
    ("ARTEFACTOS", "SPOT FIJO EMBUTIR", "COB 3W Ø38 mm", "17"),
    ("ARTEFACTOS", "SPOT MÓVIL EMBUTIR", "COB 3W Ø52 mm", "18"),
    ("ARTEFACTOS", "SPOT 12V MÓVIL", "3W / 2,5W", "19"),
    ("ARTEFACTOS", "PLAFÓN LED ALUMINIO", "12V 2,5W Ø60 mm", "20"),
    ("ARTEFACTOS", "PANEL REDONDO EMBUTIR", "12V 3W Ø83 mm BLANCO", "21"),
    ("ARTEFACTOS", "PANEL REDONDO EMBUTIR", "12V 3W Ø70 mm NEGRO", None),
    ("ARTEFACTOS", "SPOT MINI EMBUTIR REDONDO", "PARA MINIDICROICA", None),
    ("ARTEFACTOS", "MINISPOT COB ALUMINIO", "12V 1W Ø20 mm", None),
    ("ARTEFACTOS", "REFLECTOR EXTERIOR LED", "12V · IP65", None),
    ("ARTEFACTOS", "APLIQUE CURVO EXTERIOR", "GU10 · IP65", None),
    ("ARTEFACTOS", "APLIQUE RECTO EXTERIOR", "GU10 · IP65", None),
    ("ARTEFACTOS", "ESTACA ALUMINIO", "1 x GU10 · IP67", None),
    ("ARTEFACTOS", "ESTACA SOLAR LED", "28 LED · IP67", None),
    ("FUENTES SWITCHING", "FUENTE SWITCHING METÁLICA SLIM", "12V / 24V", "30"),
]


# ---------------------------------------------------------------- tipografía


class Tipo:
    """Una TrueType incrustada entera, con codificación WinAnsi.

    Alcanza para el español: acentos, Ø y · están todos en cp1252. Se incrusta completa y
    no en subset porque son tres páginas de texto y el archivo pesa lo mismo.
    """

    def __init__(self, pdf, ruta, nombre):
        datos = ruta.read_bytes()
        tt = TTFont(ruta)
        upem = tt["head"].unitsPerEm
        cmap, hmtx = tt.getBestCmap(), tt["hmtx"]
        self.ancho = {}
        anchos = []
        for c in range(32, 256):
            try:
                g = cmap.get(ord(bytes([c]).decode("cp1252")))
            except (UnicodeDecodeError, ValueError):
                g = None
            w = round(hmtx[g][0] * 1000 / upem) if g else 0
            anchos.append(w)
            self.ancho[c] = w
        cab, os2 = tt["head"], tt["OS/2"]
        k = 1000 / upem
        ff = Stream(pdf, datos)
        ff.Length1 = len(datos)
        desc = Dictionary(
            Type=Name.FontDescriptor, FontName=Name("/" + nombre), Flags=32,
            FontBBox=Array([int(cab.xMin * k), int(cab.yMin * k),
                            int(cab.xMax * k), int(cab.yMax * k)]),
            ItalicAngle=0, Ascent=int(os2.sTypoAscender * k),
            Descent=int(os2.sTypoDescender * k),
            CapHeight=int(getattr(os2, "sCapHeight", 700)), StemV=80,
            FontFile2=pdf.make_indirect(ff))
        self.obj = pdf.make_indirect(Dictionary(
            Type=Name.Font, Subtype=Name.TrueType, BaseFont=Name("/" + nombre),
            FirstChar=32, LastChar=255, Widths=Array(anchos),
            Encoding=Name.WinAnsiEncoding, FontDescriptor=pdf.make_indirect(desc)))

    def mide(self, texto, cuerpo, letra=0.0):
        b = texto.encode("cp1252", "replace")
        return sum(self.ancho.get(c, 0) for c in b) * cuerpo / 1000 + letra * max(len(b) - 1, 0)


def _esc(texto):
    b = texto.encode("cp1252", "replace")
    return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def texto(recurso, cadena, x, y, cuerpo, color=TINTA, letra=0.0):
    """`recurso` es el nombre del recurso de fuente, p. ej. "/F1"."""
    r, g, b = color
    # el Tc se emite siempre: es estado del texto y persiste entre bloques, así que
    # omitirlo deja el espaciado del renglón anterior y ensancha lo que viene después
    partes = [b"BT", f"{r:.3f} {g:.3f} {b:.3f} rg".encode(),
              f"{recurso} {cuerpo:.2f} Tf".encode(), f"{letra:.3f} Tc".encode()]
    partes += [f"1 0 0 1 {x:.2f} {y:.2f} Tm".encode(), b"(" + _esc(cadena) + b") Tj", b"ET"]
    return b"\n".join(partes)


def regla(x0, y, x1, color=LINEA, grosor=0.6):
    r, g, b = color
    return (f"{r:.3f} {g:.3f} {b:.3f} RG {grosor} w "
            f"{x0:.2f} {y:.2f} m {x1:.2f} {y:.2f} l S").encode()


# ---------------------------------------------------------------- imágenes


def incrustar(pdf, imagen, ancho_max=1600, calidad=92):
    """Embebe la imagen. Con `calidad` va en JPEG; con `calidad=None`, sin pérdida.

    Acá sí conviene JPEG, al revés que en el catálogo técnico: allá las fotos eran recortes
    pegados sobre un panel liso y el ruido de la compresión se veía como un recuadro
    fantasma contra ese fondo plano. Acá la página **entera** es la imagen, no hay fondo
    debajo con el que pueda no coincidir. Sin comprimir el archivo da 30 MB y no entra en un
    mail; en JPEG 92 da menos de 3 MB y la diferencia no se ve.
    """
    if imagen.width > ancho_max:
        alto = round(imagen.height * ancho_max / imagen.width)
        imagen = imagen.resize((ancho_max, alto), Image.LANCZOS)
    if calidad is None:
        x = Stream(pdf, zlib.compress(imagen.tobytes(), 9))
        x.Filter = Name.FlateDecode
    else:
        buf = io.BytesIO()
        imagen.save(buf, "JPEG", quality=calidad, subsampling=0, optimize=True)
        x = Stream(pdf, buf.getvalue())
        x.Filter = Name.DCTDecode
    x.Type, x.Subtype = Name.XObject, Name.Image
    x.Width, x.Height = imagen.size
    x.ColorSpace, x.BitsPerComponent = Name.DeviceRGB, 8
    return pdf.make_indirect(x)


def borde(a):
    """El color del marco de la imagen, para rellenar lo que sobre sin que se note."""
    m = max(2, min(a.shape[:2]) // 80)
    tiras = np.concatenate([a[:m].reshape(-1, 3), a[-m:].reshape(-1, 3),
                            a[:, :m].reshape(-1, 3), a[:, -m:].reshape(-1, 3)])
    return np.median(tiras, axis=0) / 255.0


def logo_negro(pdf):
    """El logo del catálogo técnico, que viene blanco con máscara, pasado a tinta."""
    tec = pikepdf.open(CATALOGO)
    xo = tec.pages[3]["/Resources"]["/XObject"]["/Im9"]
    im = pikepdf.PdfImage(xo).as_pil_image().convert("RGBA")
    a = np.asarray(im).astype(float)
    alfa = (a[..., 3:4] / 255.0)
    tinta = np.array(TINTA) * 255.0
    comp = tinta * alfa + 255.0 * (1 - alfa)
    return incrustar(pdf, Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8), "RGB"),
                     calidad=None)


def hoja(pdf, recursos, flujo):
    pagina = pikepdf.Page(pdf.make_indirect(Dictionary(
        Type=Name.Page, MediaBox=Array([0, 0, ANCHO, ALTO]),
        Resources=recursos, Contents=pdf.make_stream(flujo))))
    pdf.pages.append(pagina)
    return pagina


def hoja_imagen(pdf, fuentes, logo, arreglo, mitad):
    """Una página con media imagen de pliego, encajada sin deformar."""
    im = Image.open(arreglo).convert("RGB")
    w, h = im.size
    corte = w // 2
    im = im.crop((0, 0, corte, h)) if mitad == 0 else im.crop((corte, 0, w, h))
    fondo = borde(np.asarray(im).astype(float))

    escala = min(ANCHO / im.width, ALTO / im.height)
    cw, ch = im.width * escala, im.height * escala
    x, y = (ANCHO - cw) / 2, (ALTO - ch) / 2

    xobj = incrustar(pdf, im)
    nombre = Name("/Ix")
    recursos = Dictionary(XObject=Dictionary({str(nombre): xobj}),
                          Font=Dictionary({"/F1": fuentes[0].obj, "/F2": fuentes[1].obj}))
    r, g, b = fondo
    flujo = b"\n".join([
        f"{r:.4f} {g:.4f} {b:.4f} rg 0 0 {ANCHO:.2f} {ALTO:.2f} re f".encode(),
        b"q", f"{cw:.3f} 0 0 {ch:.3f} {x:.3f} {y:.3f} cm".encode(),
        b"/Ix Do", b"Q"])
    return hoja(pdf, recursos, flujo)


# ---------------------------------------------------------------- páginas compuestas


def _recursos(pdf, fuentes, logo):
    return Dictionary(XObject=Dictionary({"/Lg": logo}),
                      Font=Dictionary({"/F1": fuentes[0].obj, "/F2": fuentes[1].obj}))


def _logo(x, y, ancho=118.0):
    alto = ancho * 90 / 341
    return b"\n".join([b"q", f"{ancho:.2f} 0 0 {alto:.2f} {x:.2f} {y:.2f} cm".encode(),
                       b"/Lg Do", b"Q"])


def portada(pdf, fuentes, logo):
    negrita, normal = fuentes
    y = 430.0
    partes = [b"1 1 1 rg 0 0 %.2f %.2f re f" % (ANCHO, ALTO),
              _logo(MARGEN, ALTO - MARGEN - 31),
              texto("/F1", "CATÁLOGO", MARGEN, y, 58),
              texto("/F2", "DE PRODUCTOS", MARGEN, y - 62, 58, GRIS),
              regla(MARGEN, y - 96, MARGEN + 190),
              texto("/F2", "ILUMINACIÓN LED", MARGEN, y - 128, 11, GRIS, letra=2.6),
              texto("/F1", "2026", MARGEN, MARGEN, 13, TINTA, letra=1.8)]
    ancho_pie = normal.mide("TENARUZ.COM.AR", 9, 2.2)
    partes.append(texto("/F2", "TENARUZ.COM.AR", ANCHO - MARGEN - ancho_pie, MARGEN + 2,
                        9, GRIS, letra=2.2))
    return hoja(pdf, _recursos(pdf, fuentes, logo), b"\n".join(partes))


def encabezado(fuentes):
    normal = fuentes[1]
    rotulo = "Catálogo de Productos"
    return b"\n".join([
        _logo(MARGEN, ALTO - MARGEN - 18, 84),
        texto("/F2", rotulo, ANCHO - MARGEN - normal.mide(rotulo, 9), ALTO - MARGEN - 8, 9, GRIS)])


def divisor(pdf, fuentes, logo, seccion, cuantas):
    negrita, normal = fuentes
    cuerpo = 40 if normal.mide(seccion, 40) < ANCHO - 2 * MARGEN else 30
    partes = [b"1 1 1 rg 0 0 %.2f %.2f re f" % (ANCHO, ALTO),
              encabezado(fuentes),
              texto("/F1", seccion, MARGEN, 440, cuerpo),
              regla(MARGEN, 410, MARGEN + 190),
              texto("/F2", f"{cuantas} fichas", MARGEN, 386, 11, GRIS, letra=1.4)]
    return hoja(pdf, _recursos(pdf, fuentes, logo), b"\n".join(partes))


def indice(pdf, fuentes, logo, filas):
    """filas: lista de ('seccion', nombre) y ('ficha', titulo, detalle, pagina)."""
    negrita, normal = fuentes
    partes = [b"1 1 1 rg 0 0 %.2f %.2f re f" % (ANCHO, ALTO),
              encabezado(fuentes),
              texto("/F1", "Índice", MARGEN, ALTO - 150, 34),
              regla(MARGEN, ALTO - 176, MARGEN + 120)]
    y = ALTO - 224
    for fila in filas:
        if fila[0] == "seccion":
            y -= 10
            partes.append(texto("/F1", fila[1], MARGEN, y, 10, GRIS, letra=2.2))
            y -= 20
        else:
            _, titulo, detalle, pag = fila
            partes.append(texto("/F2", titulo, MARGEN + 10, y, 11))
            x = MARGEN + 10 + normal.mide(titulo, 11) + 9
            partes.append(texto("/F2", detalle, x, y, 8.5, GRIS))
            n = str(pag)
            partes.append(texto("/F2", n, ANCHO - MARGEN - normal.mide(n, 10), y, 10, GRIS))
            y -= 19
    return hoja(pdf, _recursos(pdf, fuentes, logo), b"\n".join(partes))


# ---------------------------------------------------------------- armado


def main(salida=SALIDA):
    presentes = [f for f in FICHAS if f[3] and (PAGINAS / f"{f[3]}.png").exists()]
    faltan = [f for f in FICHAS if f not in presentes]

    # paginación: tapa, índice, y por sección una portadilla más dos páginas por ficha
    secciones = []
    for seccion, _, _, _ in FICHAS:
        if seccion not in secciones:
            secciones.append(seccion)
    numero, mapa, filas = 3, {}, []
    for seccion in secciones:
        delas = [f for f in presentes if f[0] == seccion]
        if not delas:
            continue
        filas.append(("seccion", seccion))
        numero += 1                                   # la portadilla
        for ficha in delas:
            mapa[ficha[3]] = numero
            filas.append(("ficha", ficha[1], ficha[2], numero))
            numero += 2

    pdf = pikepdf.Pdf.new()
    fuentes = (Tipo(pdf, TIPOS / "Outfit-Bold.ttf", "Outfit-Bold"),
               Tipo(pdf, TIPOS / "Outfit-Regular.ttf", "Outfit-Regular"))
    logo = logo_negro(pdf)

    portada(pdf, fuentes, logo)
    indice(pdf, fuentes, logo, filas)
    for seccion in secciones:
        delas = [f for f in presentes if f[0] == seccion]
        if not delas:
            continue
        divisor(pdf, fuentes, logo, seccion, len(delas))
        for ficha in delas:
            arreglo = PAGINAS / f"{ficha[3]}.png"
            for mitad in (0, 1):
                hoja_imagen(pdf, fuentes, logo, arreglo, mitad)
            print(f"  pág {mapa[ficha[3]]:3d}-{mapa[ficha[3]]+1:<3d} {ficha[1]} {ficha[2]}")

    pdf.save(salida)
    print(f"\n{len(pdf.pages)} páginas -> {salida}")
    if faltan:
        print(f"\nfaltan {len(faltan)} fichas por diseñar:")
        for seccion, titulo, detalle, _ in faltan:
            print(f"  [{seccion}] {titulo} {detalle}")
    return salida


if __name__ == "__main__":
    main(*sys.argv[1:])
