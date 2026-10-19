"""Reemplaza las fotos de producto de las fichas, sin tocar nada más de la página.

Cada foto se dibuja con `q … cm … cm … Do … Q`: el `cm` de afuera es la escala global de
wkhtmltopdf y el de adentro coloca la imagen. Se reescribe **sólo el `cm` de adentro**, que
es el que pertenece a esa foto; el de afuera lo comparte toda la página y moverlo correría
todo. El `cm` interior original es `[W, 0, 0, -H, 0, H]`; compuesto con el de afuera
`[A, 0, 0, D, E, F]` la caja final queda en `x: E .. E+W*A` y `y: F .. F+H*D`, así que para
una caja deseada `(X0, Y0, X1, Y1)` el `cm` nuevo es

    a = (X1-X0)/A    d = -(Y1-Y0)/D    e = (X0-E)/A    f = (Y1-F)/D

**El encuadre es el problema, no el pegado.** Las tomas nuevas son de frente con un haz
dibujado hacia arriba, y ese haz se lleva más de la mitad del cuadro. Metidas enteras en el
hueco de hoy, la lámpara queda bastante más chica que la que reemplaza; y agrandar la caja
hasta compensarlo la haría chocar con el bloque vecino. Por eso cada foto se recorta
alrededor de **su lámpara**, no de su silueta: así la proporción que manda es la de la
lámpara y no la del haz, y las fotos no salen ni deformadas ni más anchas.

El recorte deja un aire alrededor donde todavía se ve algo de haz, y ese aire se **funde**
al color del panel con una rampa, en vez de cortarse en seco: sobre un panel liso el corte
se vería como un borde y el degradé no se ve. La lámpara queda entera adentro de la rampa,
así que no la toca.

El recuadro de la lámpara de cada foto está medido a mano sobre una grilla. Los detectores
automáticos no sirvieron: el haz es opaco, tiene el mismo color que el lente y en varias
tomas es tan liso como el cuerpo blanco, así que por alfa, por saturación o por gradiente
las tres tomas de un mismo producto daban recuadros distintos.
"""
import pathlib
import sys

import numpy as np
import pikepdf
from PIL import Image
from pikepdf import Name

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import recorte  # noqa: E402

ORIGEN = BASE / "origen" / "TZ-Importado_Catalogo.pdf"
SALIDA = BASE / "_paso0.pdf"
FOTOS = BASE / "fotos"

# El catálogo usa dos negros: los paneles de bloques de variante son #1a1a1a y los slots de
# foto única, #1e1e1e. Medido sobre la página, al lado de cada foto. Recomponer sobre el que
# no es deja el recuadro de la caja a la vista.
PANEL_VARIANTE = (26.0, 26.0, 26.0)
PANEL_UNICO = (30.0, 30.0, 30.0)

DESVANECE = 0.14   # banda donde el haz cortado se funde al panel


class Bloque:
    """Una foto a reemplazar.

    `lampara` y `vieja` son el recuadro de la lámpara —(x0, y0, x1, y1) en fracción, con la
    y desde arriba— dentro de la foto nueva y dentro de la caja que ocupa hoy. De esos dos
    sale la escala: la lámpara nueva se dibuja **igual o mayor** que la que reemplaza.

    `factor` la agranda por encima de eso. Los límites recortan contra el panel, el texto y
    el bloque vecino.
    """

    def __init__(self, pagina, xobj, archivo, lampara, vieja, factor=1.0,
                 panel=PANEL_VARIANTE, izq=None, der=None, piso=None, tope=None):
        self.pagina = pagina
        self.xobj = xobj
        self.archivo = archivo
        self.lampara = lampara
        self.vieja = vieja
        self.factor = factor
        self.panel = panel
        self.izq, self.der, self.piso, self.tope = izq, der, piso, tope


# Recuadro de la lámpara dentro de cada foto nueva, medido sobre una grilla al 10 %.
LAMPARA = {
    "TZ-GU10-7W-3K":        (.18, .33, .82, .97),
    "TZ-GU10-7W-4K":        (.18, .33, .82, .97),
    "TZ-GU10-7W-6K":        (.18, .33, .82, .97),
    "TZ-MR11-3W-3K":        (.05, .18, .95, .95),
    "TZ-MR11-3W-3K-DIM":    (.04, .16, .96, .94),
    "TZ-MR16-5W-3K":        (.15, .27, .85, .95),
    "TZ-MR16-5W-6K":        (.15, .27, .85, .95),
    "TZ-AR70-7W-DIM-3K":    (.25, .20, .75, .95),
    "TZ-AR111-15W-3K":      (.20, .18, .80, .95),
    "TZ-AR111-15W-4K":      (.17, .15, .83, .95),
    "TZ-PLL-18W-3K":        (.01, .31, .98, .61),
    "TZ-PLL-18W-4K":        (.01, .31, .98, .61),
    "TZ-PLL-18W-6K":        (.01, .31, .98, .61),
    "stick-t45":            (.27, .05, .73, .95),
    "TZ-G412V-2W-3K":       (.33, .05, .67, .94),
    "TZ-G412V-2W-4K":       (.33, .05, .67, .94),
    "TZ-G412V-2W-6K":       (.33, .05, .67, .94),
    "TZ-G412V-4W-3K":       (.33, .04, .67, .92),
    "TZ-G412V-4W-4K":       (.35, .05, .65, .93),
    "TZ-G412V-4W-6K":       (.33, .05, .67, .93),
    "TZ-A60E27-12W-DIM-3K": (.22, .03, .78, .97),
}

# Recuadro de la lámpara dentro de la caja que ocupa hoy, por familia de ficha.
GU10 = (.21, .20, .79, .76)
MR11 = (.27, .17, .73, .80)
MR16 = (.25, .17, .75, .77)
AR70 = (.27, .08, .73, .87)
AR111 = (.20, .22, .80, .75)
PLL = (.17, .20, .83, .68)
STICK = (.08, .02, .92, .97)
G4COB = (.17, .22, .83, .75)
G4SMD = (.22, .20, .78, .75)
A60 = (.13, .05, .87, .97)


def _b(pagina, xobj, archivo, vieja, **kw):
    return Bloque(pagina, xobj, archivo, LAMPARA[archivo], vieja, **kw)


# Los límites verticales son el punto medio entre dos cajas vecinas, menos medio aire, así
# cada bloque se queda con su mitad del paso. Los horizontales son el panel de un lado y el
# comienzo del texto del otro.
BLOQUES = [
    # página 4 arriba — DICROICA LED GU10 7W (pedido 2: van más grandes)
    _b(4, "/Im31", "TZ-GU10-7W-3K", GU10, factor=1.15, izq=308, der=408, piso=638, tope=740),
    _b(4, "/Im33", "TZ-GU10-7W-4K", GU10, factor=1.15, izq=308, der=408, piso=533, tope=633),
    _b(4, "/Im35", "TZ-GU10-7W-6K", GU10, factor=1.15, izq=308, der=408, piso=399, tope=528),
    # página 4 abajo — MINIDICRO LED (pedidos 3 y 4)
    _b(4, "/Im37", "TZ-MR11-3W-3K-DIM", MR11, izq=3, der=127, piso=189, tope=345),
    _b(4, "/Im39", "TZ-MR11-3W-3K", MR11, izq=3, der=127, piso=5, tope=184),
    # página 5 — MR16 arriba (pedido 5), AR70 abajo (pedido 6)
    _b(5, "/Im46", "TZ-MR16-5W-3K", MR16, izq=308, der=458, piso=585, tope=740),
    _b(5, "/Im48", "TZ-MR16-5W-6K", MR16, izq=308, der=458, piso=399, tope=580),
    _b(5, "/Im12", "TZ-AR70-7W-DIM-3K", AR70, panel=PANEL_UNICO, izq=5, der=301, piso=98, tope=342),
    # página 6 — AR111 arriba (pedido 7), PLL abajo (pedido 8)
    _b(6, "/Im55", "TZ-AR111-15W-3K", AR111, izq=308, der=463, piso=585, tope=740),
    _b(6, "/Im57", "TZ-AR111-15W-4K", AR111, izq=308, der=463, piso=399, tope=580),
    _b(6, "/Im59", "TZ-PLL-18W-3K", PLL, izq=3, der=301, piso=288, tope=331),
    _b(6, "/Im61", "TZ-PLL-18W-4K", PLL, izq=3, der=301, piso=226, tope=269),
    _b(6, "/Im63", "TZ-PLL-18W-6K", PLL, izq=3, der=301, piso=164, tope=207),
    # página 7 abajo — LED STICK T45 (pedido 1)
    _b(7, "/Im74", "stick-t45", STICK, panel=PANEL_UNICO, izq=5, der=301, piso=66, tope=346),
    # página 8 — BIPIN COB G4 2W arriba (pedido 9), BIPIN LED G4 4W abajo (pedido 10)
    _b(8, "/Im81", "TZ-G412V-2W-3K", G4COB, izq=308, der=351, piso=638, tope=740),
    _b(8, "/Im83", "TZ-G412V-2W-4K", G4COB, izq=308, der=351, piso=533, tope=633),
    _b(8, "/Im85", "TZ-G412V-2W-6K", G4COB, izq=308, der=351, piso=399, tope=528),
    _b(8, "/Im87", "TZ-G412V-4W-3K", G4SMD, izq=3, der=49, piso=242, tope=345),
    _b(8, "/Im89", "TZ-G412V-4W-4K", G4SMD, izq=3, der=49, piso=137, tope=238),
    _b(8, "/Im91", "TZ-G412V-4W-6K", G4SMD, izq=3, der=49, piso=5, tope=133),
    # página 10 abajo — BULBO LED A60 E27 12W DIMERIZABLE (pedido 11)
    _b(10, "/Im113", "TZ-A60E27-12W-DIM-3K", A60, panel=PANEL_UNICO, izq=5, der=301, piso=66, tope=346),
]


def _mul(m, n):
    a, b, c, d, e, f = m
    A, B, C, D, E, F = n
    return [a * A + b * C, a * B + b * D, c * A + d * C, c * B + d * D,
            e * A + f * C + E, e * B + f * D + F]


def _recorrer(pagina):
    """Las operaciones de la página y, por cada `Do` de imagen, su contexto."""
    ops = pikepdf.parse_content_stream(pagina)
    pila, cm = [], [1, 0, 0, 1, 0, 0]
    previo, i_cm = list(cm), None
    hallados = {}
    for i, (o, op) in enumerate(ops):
        s = str(op)
        if s == "q":
            pila.append(list(cm))
        elif s == "Q":
            cm = pila.pop() if pila else [1, 0, 0, 1, 0, 0]
        elif s == "cm":
            previo, i_cm = list(cm), i
            cm = _mul([float(x) for x in o], cm)
        elif s == "Do":
            hallados[i] = (str(o[0]), list(previo), i_cm, list(cm))
    return ops, hallados


def _caja(cm):
    a, b, c, d, e, f = cm
    pts = [(e, f), (a + e, b + f), (a + c + e, b + d + f), (c + e, d + f)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def preparar(b):
    """La foto compuesta sobre el color del panel, recortada al contenido.

    **No se recorta la silueta por umbral.** Estas tomas traen canal alfa, y el alfa ya
    describe el desvanecido del haz píxel a píxel. Pasarlas por el recorte de `recorte.py`
    —que separa el producto de un fondo blanco con un umbral— convierte ese degradé en un
    contorno binario, y sobre el panel liso el haz termina cortado en un trapecio de borde
    recto. Componer con el alfa lo resuelve solo y además respeta el antialias del contorno.

    El recorte posterior saca sólo el margen transparente, no el haz: el haz se apaga solo
    dentro del cuadro.

    Devuelve la imagen y el recuadro de la lámpara **dentro de ese recorte**, en fracciones.
    """
    ruta = FOTOS / f"{b.archivo}.webp"
    im = Image.open(ruta).convert("RGBA")
    W, H = im.size
    a = np.asarray(im).astype(float)
    alfa = a[..., 3]

    if alfa.min() > 250:                      # sin alfa útil: fondo blanco a recortar
        entera = recorte.recomponer(ruta, b.panel, margen=1.0)
    else:
        fondo = np.array(b.panel, dtype=float)
        k = (alfa / 255.0)[..., None]
        comp = a[..., :3] * k + fondo * (1 - k)
        entera = Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8), "RGB")

    ys, xs = np.where(alfa > 3)
    sx0, sy0 = int(xs.min()), int(ys.min())
    sx1, sy1 = int(xs.max()) + 1, int(ys.max()) + 1
    img = entera.crop((sx0, sy0, sx1, sy1))

    fx0, fy0, fx1, fy1 = b.lampara
    cw, ch = sx1 - sx0, sy1 - sy0
    dentro = ((fx0 * W - sx0) / cw, (fy0 * H - sy0) / ch,
              (fx1 * W - sx0) / cw, (fy1 * H - sy0) / ch)
    return img, dentro


def _colocar(b, actual, img, dentro):
    """La caja donde va la foto nueva, con la proporción de la imagen intacta.

    La escala sale de exigir que la lámpara nueva no quede más chica que la que reemplaza
    **en ninguna de las dos medidas**: se toma la mayor de las dos escalas y nunca se
    estira una sola. El pie de la lámpara se mantiene donde estaba, así las lámparas de los
    bloques apilados siguen apoyando en la misma línea y el crecimiento se va hacia arriba,
    que es donde está el aire. Después se recorta contra los límites, primero corriendo la
    caja y, si aun así no entra, achicándola de forma proporcional.
    """
    X0, Y0, X1, Y1 = actual
    vx0, vy0, vx1, vy1 = b.vieja
    dx0, dy0, dx1, dy1 = dentro
    fw, fh = dx1 - dx0, dy1 - dy0
    cw, ch = X1 - X0, Y1 - Y0
    aspecto = img.width / img.height

    vieja_w, vieja_h = (vx1 - vx0) * cw, (vy1 - vy0) * ch
    cx = X0 + (vx0 + vx1) / 2 * cw
    piso = Y1 - vy1 * ch                        # el pie de la lámpara de hoy

    # Se iguala el **área** de la lámpara, no cada medida por separado. Forzar las dos
    # medidas infla las tomas de tres cuartos, que son anchas por naturaleza: el MR11
    # terminaba 2,4 veces más ancho que la foto que reemplaza y tocando el borde del panel.
    # Con el área, la lámpara nueva pesa lo mismo que la vieja y conserva su proporción.
    ancho = b.factor * ((vieja_w * vieja_h * aspecto) / (fw * fh)) ** 0.5
    alto = ancho / aspecto
    # la lámpara no está centrada en el recorte, así que se la ubica por su propio recuadro
    x0 = cx - (dx0 + dx1) / 2 * ancho
    x1 = x0 + ancho
    y1 = piso + dy1 * alto
    y0 = y1 - alto

    for _ in range(4):
        if b.izq is not None and x0 < b.izq:
            x1 += b.izq - x0
            x0 = b.izq
        if b.der is not None and x1 > b.der:
            x0 -= x1 - b.der
            x1 = b.der
        if b.piso is not None and y0 < b.piso:
            y1 += b.piso - y0
            y0 = b.piso
        if b.tope is not None and y1 > b.tope:
            y0 -= y1 - b.tope
            y1 = b.tope
        exceso = 1.0
        if b.izq is not None and b.der is not None:
            exceso = max(exceso, (x1 - x0) / (b.der - b.izq))
        if b.piso is not None and b.tope is not None:
            exceso = max(exceso, (y1 - y0) / (b.tope - b.piso))
        if exceso <= 1.0:
            break
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        w, h = (x1 - x0) / exceso, (y1 - y0) / exceso
        x0, x1, y0, y1 = mx - w / 2, mx + w / 2, my - h / 2, my + h / 2

    return (x0, y0, x1, y1), (vieja_w, vieja_h), ((x1 - x0) * fw, (y1 - y0) * fh)


def main(entrada=ORIGEN, salida=SALIDA):
    entrada = pathlib.Path(entrada)
    salida = pathlib.Path(salida)
    pdf = pikepdf.open(entrada)

    por_pagina = {}
    for b in BLOQUES:
        por_pagina.setdefault(b.pagina, []).append(b)

    for npag, bloques in sorted(por_pagina.items()):
        pagina = pdf.pages[npag - 1]
        ops, hallados = _recorrer(pagina)
        cambios = {}
        for b in bloques:
            objetivo = [(i, d) for i, d in hallados.items() if d[0] == b.xobj]
            if len(objetivo) != 1:
                raise SystemExit(f"página {npag}: {b.xobj} aparece {len(objetivo)} veces")
            i_do, (_, afuera, i_cm, cm) = objetivo[0]
            A, _, _, D, E, F = afuera

            img, dentro = preparar(b)
            caja, vieja, nueva = _colocar(b, _caja(cm), img, dentro)
            x0, y0, x1, y1 = caja

            nombre = Name(f"/Tz{npag}{b.xobj[3:]}")
            recorte.incrustar(pdf, pagina, nombre, img, ancho_px=1200)
            cambios[i_do] = nombre
            # ojo con el signo: la matriz de afuera tiene D negativo, así que el cuadrado
            # unidad entra al revés y `unit(0,0)` cae en el **pie** de la caja, no en el techo
            cambios[i_cm] = [(x1 - x0) / A, 0, 0, (y1 - y0) / D,
                             (x0 - E) / A, (y0 - F) / D]
            print(f"  p{npag} {b.xobj:7s} {b.archivo:22s} lámpara "
                  f"{vieja[0]:5.1f}x{vieja[1]:5.1f} -> {nueva[0]:5.1f}x{nueva[1]:5.1f} pt"
                  f"   caja {x1-x0:6.1f}x{y1-y0:6.1f}")

        nuevas = []
        for i, (o, op) in enumerate(ops):
            if i in cambios:
                v = cambios[i]
                nuevas.append(([v] if isinstance(v, Name)
                               else [pikepdf.Object.parse(f"{x:.6f}".encode()) for x in v], op))
            else:
                nuevas.append((o, op))
        pagina.Contents = pdf.make_stream(pikepdf.unparse_content_stream(nuevas))

    pdf.save(salida)
    print(f"  escrito {salida}")


if __name__ == "__main__":
    main(*sys.argv[1:])
