"""Arma el catálogo entero, paso por paso.

    python3 -I catalogo/build.py

Cada paso lee el archivo del anterior y escribe el siguiente, así se puede correr de nuevo
desde el original sin arrastrar nada.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import artefactos  # noqa: E402
import indice  # noqa: E402
import limpiar  # noqa: E402
import mr16  # noqa: E402
import pagina11  # noqa: E402
import portadillas  # noqa: E402

PASOS = [
    ("página 11: el tubo T5 al slot superior y el bulbo A60 12V/24V abajo", pagina11.main),
    ("ARTEFACTOS: cuatro fichas nuevas de 12V y la sección corre dos páginas", artefactos.main),
    ("índice: 31 fichas con la paginación nueva", indice.main),
    ("portadillas: listas y contadores de LÁMPARAS y ARTEFACTOS", portadillas.main),
    ("MR16: suma el 4000K y la versión de 7W", mr16.main),
    ("limpieza: un solo folio por página en la capa de texto", limpiar.main),
]

if __name__ == "__main__":
    for titulo, paso in PASOS:
        print(f"\n== {titulo}")
        paso()
