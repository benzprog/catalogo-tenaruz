"""Recorta una foto de producto de su fondo y la recompone sobre el panel del catálogo.

Las fotos nuevas vienen sobre blanco; los paneles del catálogo son negro `#1e1e1e` en
LÁMPARAS y crema `#f1ede8` en ARTEFACTOS. Pegar la foto tal cual deja un recuadro blanco,
así que hay que separarla del fondo.

Es la misma idea que `recorte_fondo.py` de la skill, al revés: allá el fondo era el negro
del panel y el destino el crema; acá el fondo es el blanco de la foto y el destino, el
panel. Lo que se conserva es la cuenta que evita la orla:

    obs = producto*a + fondo*(1-a)   ->   sal = obs + (destino - fondo)*(1-a)

El umbral va alto porque el JPEG deja anillos alrededor del contorno, y la silueta se lima
con disco y radio chico: el radio lo limita la parte más fina de la foto, que en estos
productos son los clips de resorte del minispot.

Se embeben con Flate y no con JPEG: sobre una superficie plana y grande, el punto de
diferencia que deja la compresión se ve como un recuadro fantasma.
"""
import zlib

import numpy as np
import pikepdf
from PIL import Image
from pikepdf import Dictionary, Name, Stream
from scipy import ndimage

NEGRO = (30.0, 30.0, 30.0)        # #1e1e1e, paneles de LÁMPARAS
CREMA = (241.0, 237.0, 232.0)     # #f1ede8, paneles de ARTEFACTOS


def disco(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r + 0.5


def fondo_de(a):
    """El color del fondo, tomado de las esquinas y no supuesto blanco."""
    h, w = a.shape[:2]
    m = max(2, min(h, w) // 100)
    esquinas = np.concatenate([a[:m, :m].reshape(-1, 3), a[:m, -m:].reshape(-1, 3),
                               a[-m:, :m].reshape(-1, 3), a[-m:, -m:].reshape(-1, 3)])
    return np.median(esquinas, axis=0)


def silueta(a, fondo, umbral=12.0, lima=2):
    """La silueta del producto: todo lo que no sea fondo conectado al borde.

    Un umbral fijo contra el blanco no sirve. El fondo de estas fotos **no es plano**: tiene
    un degradé de hasta nueve niveles, así que la mitad de la imagen se aparta más de 4 del
    valor de las esquinas. Con un corte fijo, un producto blanco sobre blanco pierde pedazos
    del aro —al panel Ø83 le quedaron manchones— y el fondo lejano entra como producto.

    Lo que sí vale es la conexión: el fondo toca el borde de la imagen y el producto no. Se
    toma como fondo la región parecida al valor del borde **que llega hasta el borde**, y
    todo lo demás es producto.

    Y se conserva sólo la mancha más grande: son fotos de un solo objeto, y al plafón le
    había quedado un arco suelto flotando arriba.
    """
    d = np.abs(a - fondo).max(axis=2)
    candidato = d <= umbral
    lab, n = ndimage.label(candidato)
    if n:
        borde = set(lab[0].tolist()) | set(lab[-1].tolist()) | \
            set(lab[:, 0].tolist()) | set(lab[:, -1].tolist())
        borde.discard(0)
        fondo_real = np.isin(lab, list(borde))
    else:
        fondo_real = np.zeros_like(candidato)

    m = ndimage.binary_fill_holes(~fondo_real)
    lab, n = ndimage.label(m)
    if n > 1:                                   # una sola mancha: la más grande
        tam = ndimage.sum(m, lab, range(1, n + 1))
        m = lab == (int(np.argmax(tam)) + 1)
    m = ndimage.binary_closing(m, disco(lima + 1))
    m = ndimage.binary_opening(m, disco(lima))
    return ndimage.binary_fill_holes(m)


def recomponer(ruta, destino, umbral=12.0, lima=2, margen=0.015):
    """Devuelve la foto recortada y recompuesta sobre `destino`, en RGB.

    Afuera de la silueta se pinta el destino **liso**. La cuenta que respeta el antialias
    del borde sólo vale donde el píxel es mezcla de producto y fondo; aplicada afuera
    arrastra las sombras y los reflejos de la foto, que sobre el crema se ven como manchas.
    """
    im = Image.open(ruta)
    if im.mode in ("RGBA", "LA", "P"):
        im = Image.alpha_composite(Image.new("RGBA", im.size, "white"),
                                   im.convert("RGBA"))
    a = np.asarray(im.convert("RGB"), dtype=float)
    fondo = fondo_de(a)
    m = silueta(a, fondo, umbral, lima)

    adentro = ndimage.binary_erosion(m, disco(1))
    borde = m & ~adentro                        # la orla donde vale la mezcla
    cob = np.clip(np.abs(a - fondo).max(axis=2) / max(umbral, 1.0), 0, 1)
    cob = np.where(adentro, 1.0, np.where(borde, cob, 0.0))[..., None]
    sal = np.where(cob > 0, a + (np.array(destino) - fondo) * (1 - cob),
                   np.array(destino, dtype=float))

    ys, xs = np.where(m)
    if len(ys):
        alto, ancho = a.shape[:2]
        dy, dx = int(alto * margen), int(ancho * margen)
        y0, y1 = max(0, ys.min() - dy), min(alto, ys.max() + 1 + dy)
        x0, x1 = max(0, xs.min() - dx), min(ancho, xs.max() + 1 + dx)
        sal = sal[y0:y1, x0:x1]
    return Image.fromarray(np.clip(sal, 0, 255).astype(np.uint8), "RGB")


def incrustar(pdf, pagina, nombre, imagen, ancho_px=900):
    """Embebe la imagen con Flate (sin pérdida) y la registra en la página."""
    if imagen.width > ancho_px:
        alto = round(imagen.height * ancho_px / imagen.width)
        imagen = imagen.resize((ancho_px, alto), Image.LANCZOS)
    crudo = imagen.tobytes()
    # `write(datos, filter=...)` espera los datos YA codificados con ese filtro:
    # pasarlos crudos deja el stream ilegible ("unknown compression method")
    x = Stream(pdf, zlib.compress(crudo, 9))
    x.Type, x.Subtype = Name.XObject, Name.Image
    x.Width, x.Height = imagen.size
    x.ColorSpace, x.BitsPerComponent = Name.DeviceRGB, 8
    x.Filter = Name.FlateDecode
    recursos = pagina["/Resources"]
    if "/XObject" not in recursos:
        recursos["/XObject"] = Dictionary()
    recursos["/XObject"][nombre] = pdf.make_indirect(x)
    return imagen
