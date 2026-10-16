"""Arma las fichas nuevas de 12V sobre el catálogo TENARUZ.

Todo se dibuja como contenido nativo sobre el PDF, con las fuentes que ya están
embebidas, siguiendo `.claude/skills/catalogo-tenaruz`. Las recetas tipográficas no se
estiman: salen del content stream original.

Dos cosas que decide este archivo y conviene no olvidar:

- **No hay fila sin dato.** El cliente no tiene los lúmenes y no se pueden calcular a
  partir del vataje: falta la eficacia del LED, que va de 60 a 120 lm/W. Así que las
  tablas llevan sólo lo que la planilla afirma. Quedan de cuatro a seis filas, que es lo
  que tiene la ficha de la ESTACA SOLAR ya publicada.
- **Una foto por variante física, no por código.** Es el criterio del REFLECTOR: su panel
  muestra dos fotos para cuatro códigos, y cada foto se rotula con uno. Donde los dos
  códigos sólo cambian la temperatura de color, va una foto sola.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from catalog import BOTTOM, TOP, Catalog  # noqa: E402
from recorte import CREMA, NEGRO, incrustar, recomponer  # noqa: E402

ORIGEN = BASE / "origen" / "TZ-Importado_Catalogo.pdf"
FOTOS = BASE / "fotos"

# recetas leídas del stream original: (recurso, cuerpo efectivo, tracking, color)
ESTILOS = {
    "titulo":    ("/F19", 18.44, -0.405, Catalog.TITLE),
    "subtitulo": ("/F20", 6.34, 1.895, Catalog.SUBTITLE),
    "desc":      ("/F11", 6.92, 0.0, Catalog.BODY),
    "etiqueta":  ("/F11", 6.34, 0.245, Catalog.LABEL),
    "valor":     ("/F20", 6.34, 0.0, Catalog.VALUE),
    "codigo":    ("/F20", 5.76, 0.396, Catalog.VALUE),
    "subcodigo": ("/F11", 5.19, 0.895, Catalog.SUBCODE),
    "pie":       ("/F11", 5.76, 1.496, Catalog.FOOTER),
    "epigrafe":  ("/F11", 5.19, 1.596, Catalog.CAPTION),   # el color real lo fija el panel
    "numero":    ("/F11", 6.34, 0.0, Catalog.WHITE),
}

# El epígrafe bajo la foto cambia de gris según el panel: el #c9c9c9 de los paneles
# oscuros, sobre el crema, casi no se lee. El catálogo usa #6d6d6d ahí (verificado contra
# el epígrafe de la ESTACA SOLAR, que está sobre crema en el original).
EPIGRAFE_OSCURO = (201, 201, 201)
EPIGRAFE_CREMA = (109, 109, 109)

PASO_CODIGO_X = 77.42      # columnas de la grilla de códigos, medidas en la pág 15
PASO_CODIGO_Y = 24.20      # renglones de esa grilla
BAJO_TABLA = 24.78         # del último renglón de la tabla al primer código
BAJO_CODIGO = 9.22         # del código a su subcódigo


def texto(cat, frag, clave, contenido, x, y, derecha=None, centro=None):
    recurso, cuerpo, trk, color = ESTILOS[clave]
    if derecha is not None:
        frag.append(cat.show_right(contenido, recurso, cuerpo, derecha, y, trk, color))
    elif centro is not None:
        frag.append(cat.show_center(contenido, recurso, cuerpo, centro, y, trk, color))
    else:
        frag.append(cat.show(contenido, recurso, cuerpo, x, y, trk, color))


def ficha(cat, pagina, slot, prod, fondo, solo_blanco=False):
    """Dibuja una ficha en su slot. `fondo` es el color del panel de producto.

    Con `solo_blanco` se rehace únicamente la mitad de texto y se deja el panel de
    producto como está: sirve para ampliar una ficha que ya existe sin tocarle las fotos
    ni los bloques de variante, que en las lámparas llevan el halo de cada temperatura.
    """
    frag = [cat.rect(*slot.white_panel, Catalog.WHITE)]
    if not solo_blanco:
        # el panel de producto se tapa sólo hasta dark_cover para no pisar el logo
        frag.append(cat.rect(*slot.dark_cover, fondo))

    # fotos: una por variante física, apiladas si hay más de una
    fotos = [] if solo_blanco else prod["fotos"]
    cx, cy = slot.photo_center
    paso = 230.0 if len(fotos) <= 1 else 268.0 / len(fotos)
    # con varias fotos hay que reservarle lugar al epígrafe de cada una: si la foto ocupa
    # todo el paso, el epígrafe cae dentro de la foto siguiente
    alto_caja = paso if len(fotos) == 1 else paso - 19.0
    for i, (archivo, epigrafe) in enumerate(fotos):
        if archivo.startswith("/"):
            # foto que ya está en el documento: se recoloca, no se vuelve a embeber.
            # Su fondo viene cocido en el JPEG, así que sólo sirve sobre el mismo panel.
            nombre = archivo
            ancho_px, alto_px = prod["medida_foto"]
        else:
            # a la resolución a la que de verdad se imprime: sin pérdida y a 900 px el
            # archivo se iba a 12,9 MB contra los 5,2 del original
            px = round(prod.get("ancho_foto", 210.0) * 300 / 72)
            im = incrustar(cat.pdf, pagina, f"/Im{prod['clave']}{i}",
                           recomponer(FOTOS / archivo, fondo), ancho_px=px)
            nombre = f"/Im{prod['clave']}{i}"
            ancho_px, alto_px = im.size
        ancho = min(prod.get("ancho_foto", 210.0), alto_caja * ancho_px / alto_px)
        alto = ancho * alto_px / ancho_px
        y = cy + (len(fotos) - 1 - 2 * i) * paso / 2
        frag.append(cat.place(nombre, cx - ancho / 2, y - alto / 2, ancho, alto))
        # el epígrafe cuelga de la foto: con una foto alta, la coordenada fija del
        # slot le cae encima (al tubo T5 le partía el cuerpo por la mitad)
        pie_foto = min(slot.caption_y, y - alto / 2 - 14.0) if len(fotos) == 1 \
            else y - alto / 2 - 14.0
        recurso, cuerpo, trk, _ = ESTILOS["epigrafe"]
        gris = EPIGRAFE_CREMA if sum(fondo) > 384 else EPIGRAFE_OSCURO
        frag.append(cat.show_center(epigrafe, recurso, cuerpo, slot.caption_center_x,
                                    pie_foto, trk, gris))

    # panel blanco: titular, bajada y barra de acento
    texto(cat, frag, "titulo", prod["titulo"], slot.text_x, slot.title_y)
    texto(cat, frag, "subtitulo", prod["subtitulo"], slot.text_x, slot.subtitle_y)
    frag.append(cat.rect(*slot.accent_bar, Catalog.TITLE))

    recurso, cuerpo, trk, color = ESTILOS["desc"]
    lineas = cat.wrap(prod["descripcion"], recurso, cuerpo, trk,
                      slot.value_right - slot.text_x)
    tope = 3 if slot is TOP else 2
    if len(lineas) > tope:
        raise SystemExit(f"{prod['clave']}: la descripción ocupa {len(lineas)} renglones "
                         f"y en el slot {slot.name} entran {tope}.")
    for i, linea in enumerate(lineas):
        frag.append(cat.show(linea, recurso, cuerpo, slot.text_x,
                             slot.desc_y - i * slot.desc_leading, trk, color))

    # tabla
    for (etiqueta, valor), y, y_linea in zip(prod["filas"], slot.row_baselines,
                                             slot.row_rules):
        texto(cat, frag, "etiqueta", etiqueta, slot.text_x, y)
        texto(cat, frag, "valor", valor, 0, y, derecha=slot.value_right)
        frag.append(cat.rule(slot.text_x - 0.23, slot.value_right + 0.25, y_linea))

    # códigos: cuelgan de la última fila, no de una coordenada fija
    base = slot.row_baselines[len(prod["filas"]) - 1] - BAJO_TABLA
    # la grilla de códigos es de tres columnas, pero un código largo no entra en 77,42 pt
    # y se pega al de al lado: ahí se pasa a dos columnas y se reparte el ancho igual
    recurso, cuerpo, trk, _ = ESTILOS["codigo"]
    mas_ancho = max(cat.advance(c, recurso, cuerpo, trk) for c, _ in prod["codigos"])
    ancho_util = slot.value_right - slot.text_x
    columnas = 3 if mas_ancho <= PASO_CODIGO_X - 6.0 else 2
    paso_x = ancho_util / columnas
    for i, (codigo, subcodigo) in enumerate(prod["codigos"]):
        x = slot.text_x + (i % columnas) * paso_x
        y = base - (i // columnas) * PASO_CODIGO_Y
        texto(cat, frag, "codigo", codigo, x, y)
        texto(cat, frag, "subcodigo", subcodigo, x, y - BAJO_CODIGO)

    # el pie no se mueve, así que una tabla larga con muchos códigos se le encima:
    # más vale que falle acá y no que salga impreso uno sobre otro
    ultimo = base - ((len(prod["codigos"]) - 1) // columnas) * PASO_CODIGO_Y - BAJO_CODIGO
    techo_pie = slot.footer_y + (len(prod["pie"]) - 1) * 12.67
    if ultimo - techo_pie < 8.0:
        raise SystemExit(
            f"{prod['clave']}: el último subcódigo queda a {ultimo - techo_pie:.1f} pt del "
            f"pie. Sacá una fila de la tabla o un renglón de códigos.")

    for i, linea in enumerate(prod["pie"]):
        texto(cat, frag, "pie", linea, slot.text_x,
              slot.footer_y + (len(prod["pie"]) - 1 - i) * 12.67)

    return frag


def recuadro_numero(cat, frag, slot, numero):
    """El recuadro del folio vive dentro del panel blanco del slot inferior.

    Se tapa con margen —(579.5, -1, 34, 36), que es como lo pinta el original— porque en
    páginas ya editadas pueden convivir dos recuadros con geometrías distintas.
    """
    frag.append(cat.rect(579.5, -1.0, 34.0, 36.0, Catalog.TITLE))
    texto(cat, frag, "numero", numero, 0, slot.page_num_y, centro=slot.page_num_center)
