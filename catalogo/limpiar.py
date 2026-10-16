"""Deja un solo número de página en la capa de texto de cada página.

Renumerar se hace tapando el recuadro y dibujando el número nuevo encima, así que cada
renumeración deja el anterior debajo: las páginas que corrieron dos lugares quedaron con
el folio viejo y el nuevo, y los dos salen al copiar y pegar o al buscar.

Se conserva el último bloque que dibuja un número dentro del recuadro —el que se ve— y se
borran los anteriores. El render no cambia: lo que se borra ya estaba tapado.

El filtro por posición (x>570, y<40) es imprescindible: sin él entra también la columna de
números del índice, que son 31 y sí se ven.
"""
import pathlib
import re
import sys

import pikepdf

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / ".claude/skills/catalogo-tenaruz/scripts"))

from pdftext import load_fonts  # noqa: E402

ENTRADA = BASE / "_paso5.pdf"
SALIDA = BASE / "TZ-Importado_Catalogo.pdf"


def main(entrada=ENTRADA, salida=SALIDA):
    pdf = pikepdf.open(str(entrada))
    fuentes = load_fonts(pdf, 4)

    def texto_de(bloque):
        salida_txt, mapa = [], {}
        for m in re.finditer(r"(/F\d+)\s+[\d.]+\s+Tf|<([0-9A-Fa-f]+)>\s*Tj", bloque):
            if m.group(1):
                mapa = fuentes.get(m.group(1), {}).get("cid2uni", {})
            else:
                h = m.group(2)
                for i in range(0, len(h), 4):
                    salida_txt.append(mapa.get(int(h[i:i + 4], 16), ""))
        return "".join(salida_txt).replace("\t", " ").strip()

    total = 0
    for idx, pagina in enumerate(pdf.pages):
        datos = pagina.obj["/Contents"]
        flujos = list(datos) if isinstance(datos, pikepdf.Array) else [datos]

        numeros = []
        for j, f in enumerate(flujos):
            crudo = f.read_bytes().decode("latin-1")
            for m in re.finditer(r"BT.*?ET", crudo, re.S):
                bloque = m.group(0)
                if not texto_de(bloque).isdigit():
                    continue
                # hay que mirar TODOS los posicionamientos del bloque: el primero suele
                # ser el `1 0 0 1 0 0 Tm` que resetea la matriz, no la posición real
                puntos = [(float(a), float(b)) for a, b in re.findall(
                    r"([-\d.]+)\s+([-\d.]+)\s+(?:Td|Tm)", bloque)]
                if any(x > 570 and y < 40 for x, y in puntos):
                    numeros.append((j, m.start(), m.end()))
        if len(numeros) < 2:
            continue

        sobran = numeros[:-1]
        for j, f in enumerate(flujos):
            recortes = sorted((a, b) for k, a, b in sobran if k == j)
            if not recortes:
                continue
            crudo = f.read_bytes().decode("latin-1")
            partes, i = [], 0
            for a, b in recortes:
                partes.append(crudo[i:a])
                i = b
            partes.append(crudo[i:])
            f.write("".join(partes).encode("latin-1"))
        total += len(sobran)
        print(f"  pág {idx + 1}: {len(sobran)} folio(s) viejo(s) borrado(s)")

    pdf.save(str(salida))
    print(f"{total} folios viejos borrados -> {salida}")
    return salida


if __name__ == "__main__":
    main()
