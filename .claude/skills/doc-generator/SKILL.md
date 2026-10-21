---
name: doc-generator
description: Genera documentos administrativos reales (.docx, .pptx, .xlsx) a partir del contenido ya desarrollado en requerimientos/ y diseno-tecnico/ — pitch del proyecto, marco teórico, documento de costos, informes. Usa python-docx/python-pptx/openpyxl con los colores/tipografía de marca/brand-tokens.json. Usar cuando se pida crear un documento administrativo, pitch, marco teórico o de costos del proyecto.
---

# Generador de documentos (Word / PowerPoint / Excel)

## Herramientas disponibles (ya instaladas en este entorno)

- `python-docx` 1.2.0 — documentos Word.
- `python-pptx` — presentaciones PowerPoint.
- `openpyxl` 3.1.5 — hojas de cálculo Excel.

No usar pandoc (no está instalado) ni depender de LibreOffice para generar el contenido
— solo para una conversión puntual si hiciera falta (`soffice --headless --convert-to`),
nunca como vía principal.

## Antes de generar cualquier documento

1. Leer `marca/brand-tokens.json` (si no existe, invocar primero la skill `branding` —
   no inventar colores ni tipografía al vuelo).
2. Identificar de qué documentos fuente sale el contenido: `requerimientos/` para
   negocio/visión, `diseno-tecnico/` para lo técnico, `notas-recoleccion.md` para
   contexto crudo si hace falta una cita textual de una decisión.
3. Si el documento es de tipo teórico/académico (ej. marco teórico), aplicar también la
   skill `apa-format`.

## Tipos de documento ya identificados para este proyecto

| Documento | Formato | Contenido fuente principal |
|---|---|---|
| Pitch del proyecto | `.pptx` | `requerimientos/01-vision-y-alcance.md` (problema, objetivo), `requerimientos/08` (módulos) |
| Marco teórico | `.docx` (formato APA) | Síntesis de los conceptos usados (SDD, arquitectura modular, Habeas Data, etc.) a lo largo de `requerimientos/` y `diseno-tecnico/` |
| Documento de costos | `.xlsx` | `diseno-tecnico/01` (costos de APIs/herramientas por módulo), `diseno-tecnico/07` (infraestructura por cliente) |
| Informe de estado | `.docx` | README de `requerimientos/` y `diseno-tecnico/`, estado de cada capa |

Esta lista no es cerrada — ampliar la tabla cuando se pida un nuevo tipo de documento.

## Convenciones al generar

- **Word (`python-docx`)**: definir los estilos `Normal`/`Title`/`Heading 1-3` una sola
  vez al inicio del script con la tipografía y colores de marca, en vez de aplicar
  formato manual párrafo por párrafo.
- **PowerPoint (`python-pptx`)**: usar un slide master/layout consistente; el color de
  fondo y de acento salen de `brand-tokens.json`, nunca de colores por defecto de la
  librería.
- **Excel (`openpyxl`)**: encabezados de tabla con el color primario de marca y texto en
  blanco/contraste adecuado; usar `NamedStyle` para no repetir el formato celda por
  celda.
- Todo script generador se guarda en `scripts/generar_<nombre-documento>.py` (crear la
  carpeta `scripts/` en la raíz del proyecto si no existe) — no como código desechable
  solo dentro de la respuesta del chat, para que el documento se pueda regenerar cuando
  cambie el contenido fuente.
- El archivo de salida va a `documentos/<nombre-documento>.<ext>` (crear `documentos/`
  si no existe) — nunca mezclado con `requerimientos/` o `diseno-tecnico/`, que son las
  fuentes de verdad en markdown, no los entregables finales.

## Flujo de trabajo

1. Confirmar con el usuario qué documento se necesita y su propósito (a quién va
   dirigido) si no es evidente.
2. Leer las fuentes relevantes.
3. Escribir (o actualizar) el script generador en `scripts/`.
4. Ejecutarlo y verificar que el archivo de salida se creó en `documentos/`.
5. Confirmar al usuario el resultado — no asumir que un documento generado una vez
   sirve para siempre: si el contenido fuente cambia, el script se vuelve a correr.
