# Criterios de aceptación — Proyecto I / ACA 1

## Objetivo del trabajo (texto del enunciado de la rúbrica)

Formular y delimitar el problema de investigación del anteproyecto, estableciendo de
manera coherente la pregunta de investigación, los objetivos, la justificación, los
alcances y las limitaciones, con sustento académico y uso adecuado de fuentes bajo
normas APA 7.

## Rúbrica (pegada por el usuario, verbatim)

### 1. Planteamiento y delimitación del problema (1 punto)
- 0.02 — No se desarrolló.
- 0.2 — El problema no está claramente identificado ni delimitado y carece de sustento.
- 0.4 — Se identifica el problema, pero presenta vacíos importantes de contexto,
  delimitación y evidencia.
- 0.6 — El problema está formulado, aunque requiere mejorar su delimitación,
  contextualización o sustento.
- 0.8 — El problema está claramente formulado y delimitado, con sustento pertinente;
  requiere ajustes menores.
- 1.0 — El problema está formulado de manera rigurosa, clara, pertinente,
  contextualizada, delimitada y suficientemente sustentada.

### 2. Introducción (1 punto)
- 0.02 — No se desarrolló.
- 0.2 — No se colocó ninguna referencia.
- 0.4 — Se colocó 4 o menos referencias, adicionalmente tiene mala redacción, mala
  ortografía y falta conectar ideas.
- 0.6 — Se colocaron las 5 referencias, pero no es coherente lo escrito, falta
  redacción, puntuación, mala ortografía.
- 0.8 — Es coherente el texto, pero aún falta mejorar la redacción y guiar más la idea.
- 1.0 — Está correcto.

### 3. Pregunta de investigación y objetivos (1 punto)
- 0.02 — No se desarrollaron.
- 0.2 — La pregunta y los objetivos son incoherentes entre sí, imprecisos o inviables.
- 0.4 — Existe relación parcial entre pregunta y objetivos, pero presentan problemas de
  formulación, alcance o uso de verbos.
- 0.6 — Pregunta y objetivos guardan relación, aunque requieren ajustes de precisión,
  alcance o articulación.
- 0.8 — Son claros, alcanzables y coherentes entre sí; presentan pequeños aspectos por
  mejorar.
- 1.0 — La pregunta, el objetivo general y los objetivos específicos presentan alta
  precisión, coherencia, articulación, viabilidad y correspondencia con el problema.

### 4. Justificación del proyecto (1 punto)
- 0.02 — No se desarrolló.
- 0.2 — No demuestra la necesidad, pertinencia o importancia del proyecto y carece de
  sustento.
- 0.4 — Presenta razones generales, con argumentación limitada y poco respaldo en
  fuentes.
- 0.6 — Explica la pertinencia del proyecto, pero requiere fortalecer la
  argumentación, el aporte o el sustento académico.
- 0.8 — Argumenta adecuadamente la pertinencia académica, profesional y contextual, con
  fuentes apropiadas; requiere ajustes menores.
- 1.0 — Sustenta sólidamente la necesidad, pertinencia, aporte y relevancia del
  proyecto mediante una argumentación clara y fuentes académicas pertinentes.

### 5. Alcances, limitaciones y viabilidad (1 punto)
- 0.02 — No se desarrollaron.
- 0.2 — No se identifican alcances ni limitaciones o son contradictorios con el
  proyecto.
- 0.4 — Se mencionan de manera general, pero no delimitan adecuadamente las
  posibilidades y restricciones del estudio.
- 0.6 — Los alcances y limitaciones son identificables, aunque requieren mayor
  precisión y análisis de la viabilidad.
- 0.8 — Son claros, realistas y coherentes con los objetivos; la viabilidad está
  suficientemente sustentada.
- 1.0 — Delimita críticamente los alcances y limitaciones y demuestra de manera clara
  la viabilidad académica, operativa y temporal del proyecto.

### 6. Calidad académica, fuentes y APA 7 (1 punto)
- 0.02 — No se desarrolló o no permite valoración.
- 0.2 — Presenta deficiencias graves de redacción, argumentación, citación y
  referencias; las fuentes no son pertinentes.
- 0.4 — Presenta errores frecuentes de redacción y APA 7; utiliza pocas fuentes
  pertinentes o las integra de manera inadecuada.
- 0.6 — La redacción es comprensible y emplea fuentes pertinentes, aunque requiere
  mejorar argumentación, citación o aplicación de APA 7.
- 0.8 — Presenta buena redacción académica, fuentes pertinentes y manejo adecuado de
  citación y referencias APA 7; requiere ajustes menores.
- 1.0 — Presenta excelente calidad de escritura y argumentación, fuentes académicas
  pertinentes y actuales, correctamente integradas y referenciadas según APA 7.

**Puntaje total de la rúbrica**: 6 puntos.

## Discrepancia señalada (no resuelta en silencio)

El texto del enunciado pegado por el usuario (`trabajo/enunciado-aca1.txt`) no trae su
propia tabla de ponderación — no hay conflicto de pesos que señalar en ese sentido.

Sí hay una tensión real a resolver con el usuario antes de redactar `solucion.md`: la
rúbrica exige explícitamente **fuentes académicas reales en formato APA 7** (mínimo 5
referencias en la Introducción, criterio 6 completo dedicado a "fuentes académicas
pertinentes y actuales"). Esto choca con la regla de la Fase 8 de `gestion-aca` para
trabajos "vinculados al proyecto principal", que prohíbe investigación externa y limita
las fuentes a `requerimientos/`/`diseno-tecnico/` (documentos internos del proyecto, no
literatura académica citable en APA 7).

**Resolución (confirmada por el usuario)**: el caso de negocio (problema, módulos,
arquitectura) sigue anclado en Apollo Services vía `requerimientos/`/`diseno-tecnico/` —
eso no cambia. Pero para la Introducción, la Justificación y el criterio de "Calidad
académica, fuentes y APA 7" sí se permite investigación externa real (WebSearch/WebFetch)
para encontrar y citar artículos académicos verificables (DOI o URL rastreable) sobre
temas como CRM conversacional con IA, calificación automática de leads/prospectos,
transformación digital en pymes de servicios, atención multicanal. Nunca se fabrica una
fuente ni una cita.

## Tabla de cobertura

| Criterio | Puntaje | Cómo se alcanza (sección de `solucion.md`) |
|---|---|---|
| 1. Planteamiento y delimitación del problema | 1.0 | "Planteamiento y delimitación del problema" |
| 2. Introducción | 1.0 | "Introducción" (5 referencias reales integradas) |
| 3. Pregunta de investigación y objetivos | 1.0 | "Pregunta de investigación y objetivos" |
| 4. Justificación del proyecto | 1.0 | "Justificación del proyecto" |
| 5. Alcances, limitaciones y viabilidad | 1.0 | "Alcances, limitaciones y viabilidad" |
| 6. Calidad académica, fuentes y APA 7 | 1.0 (contenido); formato final se verifica en el documento Word | "Referencias (APA 7)" + redacción de todo el documento |

Puntaje de cobertura de contenido: 6/6. Pendiente real: que el formato APA 7 (sangría
francesa, interlineado, tipografía) se aplique correctamente al generar el `.docx` en
la Fase 10 — se verifica leyendo el PDF, no se asume.
