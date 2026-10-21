---
name: apa-format
description: Normas de formato APA 7ma edición para documentos formales del proyecto (marco teórico, informes). Usar cuando el usuario pida "formato APA" o al generar un documento de tipo académico/teórico (ej. marco teórico) vía la skill doc-generator. No aplica a pitch decks ni documentos de costos, que no llevan citas ni formato académico.
---

# Formato APA (7ma edición)

Checklist a aplicar cuando el documento lo requiera (marco teórico, informes formales
con fuentes citadas) — no es el formato por defecto de todo lo que se genere en este
proyecto.

## Formato de página y tipografía

- Fuente: Times New Roman 12pt (o Calibri 11pt como alternativa aceptada en la 7ma ed.).
- Márgenes de 2.54 cm (1 pulgada) en los 4 lados.
- Interlineado doble en todo el cuerpo del documento.
- Sangría de primera línea de 1.27 cm (0.5") en cada párrafo.
- Numeración de página en la esquina superior derecha, desde la portada.

## Portada (página de título)

- Título del trabajo (negrita, centrado, en el tercio superior de la página).
- Nombre del autor.
- Afiliación (en este proyecto: el nombre del producto/organización, no una
  universidad — adaptar el campo sin forzar una afiliación académica inexistente).
- Fecha.

## Encabezados (niveles APA)

| Nivel | Formato |
|---|---|
| 1 | Centrado, negrita, Mayúscula Inicial |
| 2 | Alineado a la izquierda, negrita, Mayúscula Inicial |
| 3 | Alineado a la izquierda, negrita, cursiva, Mayúscula Inicial |
| 4 | Con sangría, negrita, termina en punto. El texto continúa en la misma línea. |

## Citas dentro del texto

- Cita narrativa: `Autor (año) afirma que...`
- Cita parentética: `(Autor, año)`
- Cita textual corta (<40 palabras): entre comillas, con `(Autor, año, p. X)`.
- Cita textual larga (≥40 palabras): bloque con sangría de 1.27 cm, sin comillas,
  interlineado doble, cita al final.

## Referencias (página final)

- Título "Referencias" (nivel 1, centrado, negrita) en página nueva.
- Orden alfabético por apellido del primer autor.
- Sangría francesa (la primera línea sin sangría, las siguientes con 1.27 cm).
- Formato base: `Apellido, Inicial. (Año). Título en cursiva. Editorial/Fuente. URL/DOI si aplica.`

## Aplicación en este proyecto

Cuando `doc-generator` produzca un `.docx` que requiera formato APA, usar `python-docx`
para fijar: fuente y tamaño en los estilos `Normal`/`Heading 1-4`, interlineado doble
(`paragraph_format.line_spacing = 2.0`), sangría de primera línea
(`paragraph_format.first_line_indent`), y generar la sección de Referencias ordenada
alfabéticamente al final. No improvisar un formato "parecido a APA" — seguir esta
checklist punto por punto.
