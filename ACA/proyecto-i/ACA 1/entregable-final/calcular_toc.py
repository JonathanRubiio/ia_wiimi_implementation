"""Ubica la pagina de cada titulo de la tabla de contenido en el PDF ya generado y
escribe toc_paginas.json para la segunda pasada de generar_anteproyecto_aca1_final.py.
Uso: uv run --with pypdf python calcular_toc.py <pdf>
"""
import json
import os
import sys

from pypdf import PdfReader

TITULOS = [
    "Resumen", "Abstract", "Declaración de originalidad y autonomía",
    "Declaración de exoneración de responsabilidad", "Introducción",
    "Planteamiento del problema", "Diagnóstico de la situación actual",
    "Predicción o pronóstico de la situación descrita",
    "Formulación o Pregunta de Investigación", "Objetivos", "Objetivo general",
    "Objetivos específicos", "Justificación", "Alcances y Limitaciones del Proyecto",
    "Referencias bibliográficas",
]

paginas = [pg.extract_text().splitlines() for pg in PdfReader(sys.argv[1]).pages]
resultado = {}
inicio = 2  # se salta portada y tabla de contenido
for titulo in TITULOS:
    for i in range(inicio, len(paginas)):
        if any(linea.strip() == titulo for linea in paginas[i]):
            resultado[titulo] = i + 1
            inicio = i
            break
faltantes = [t for t in TITULOS if t not in resultado]
if faltantes:
    sys.exit(f"Titulos no encontrados: {faltantes}")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toc_paginas.json")
json.dump(resultado, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(resultado)
