# Solución — Proyecto I / ACA 1

- **Vinculación**: proyecto principal (Apollo Services) para el caso de negocio (problema,
  módulos, arquitectura) + investigación académica externa real para Introducción,
  Justificación y Calidad académica/APA 7 (ver resolución de la discrepancia en
  `criterios-aceptacion.md`).
- **Clases usadas como referencia**: clase-1, clase-2 (marco metodológico de título,
  planteamiento del problema, pregunta de investigación y objetivos).
- **Fecha**: 2026-10-26.
- **Enunciado**: trabajo/enunciado-aca1.txt

## 1. Requisitos extraídos del enunciado y la rúbrica

1. Planteamiento y delimitación del problema: formulado de manera rigurosa, clara,
   pertinente, contextualizada, delimitada y sustentada (1 punto).
2. Introducción: coherente, bien redactada, con **al menos 5 referencias** académicas
   integradas (1 punto).
3. Pregunta de investigación y objetivos: precisos, coherentes entre sí, articulados,
   viables, y en correspondencia directa con el problema (1 punto).
4. Justificación del proyecto: necesidad, pertinencia, aporte y relevancia sustentados
   con argumentación clara y fuentes académicas pertinentes (1 punto).
5. Alcances, limitaciones y viabilidad: delimitación crítica y viabilidad académica,
   operativa y temporal demostrada (1 punto).
6. Calidad académica, fuentes y APA 7: redacción académica, fuentes pertinentes y
   actuales, correctamente integradas y referenciadas en formato APA 7 (1 punto).

Puntaje total: 6 puntos.

## 2. Descomposición del problema

El trabajo exige entregar, como un documento único y coherente, las primeras piezas del
anteproyecto: título preliminar, introducción con sustento bibliográfico, planteamiento
del problema, pregunta de investigación, objetivos, justificación, y alcances/
limitaciones/viabilidad — todo bajo norma APA 7. Siguiendo la regla de clase de que
"título, pregunta de investigación y objetivo general deben hablar exactamente de lo
mismo", el desarrollo se organiza para que esos tres elementos compartan terminología
desde el inicio, evitando que cada sección se redacte de forma aislada.

El caso de estudio se ancla en el problema de negocio real ya documentado en
`requerimientos/01-vision-y-alcance.md` y `requerimientos/08-modulos-y-arquitectura-comercial.md`
de este repositorio (Apollo Services): pymes con equipos comerciales pequeños pierden
oportunidades de venta por la dispersión de contactos entre redes sociales y la ausencia
de un sistema de clasificación y seguimiento automatizado. Para sustentar
académicamente ese problema y justificar su relevancia se incorporan 5 artículos reales,
verificados con DOI, sobre adopción de IA en pymes y chatbots conversacionales en
atención al cliente.

## 3. Solución completa

### Título preliminar

**"Efecto de la clasificación conversacional con inteligencia artificial en la
conversión de prospectos a citas comerciales en pymes de servicios de Bogotá"**

(20 palabras, sin punto final; cumple los 5 criterios vistos en clase: tema —
clasificación conversacional con IA—, población — pymes de servicios—, propósito —
conversión de prospectos a citas—, lugar — Bogotá—; se omite deliberadamente la
temporalidad por restricción de extensión, sin que eso afecte la comprensión del
estudio.)

### Introducción

Las organizaciones de servicios que operan con equipos comerciales pequeños enfrentan
un reto creciente: atender simultáneamente varios canales digitales de contacto
(WhatsApp, Instagram, Facebook) sin perder oportunidades de venta por falta de
tecnificación. La adopción de inteligencia artificial (IA) en pequeñas y medianas
empresas (pymes) ha sido documentada como un proceso heterogéneo, condicionado por la
madurez digital, la capacidad organizacional y la disponibilidad de recursos de cada
empresa (Popa, Popa, Ciocodeică y Mihălcescu, 2025; Sánchez, Calderón y Herrera, 2025).
A pesar de estas barreras, la literatura reciente muestra que la IA aplicada a la
atención al cliente —particularmente los chatbots conversacionales— puede mejorar
tanto la experiencia del consumidor como las tasas de conversión, al responder con
mayor rapidez y consistencia que un equipo humano sobrecargado (Ghosh, Ness y
Salunkhe, 2024; Ramki, Gopi, R., Markan, Natarajan y Rajalakshmi, 2024).

En paralelo, estudios sobre adopción sostenible de IA en pymes advierten que el
beneficio de estas tecnologías no es automático: depende de que la organización
desarrolle capacidades dinámicas que le permitan integrar la herramienta a su proceso
comercial real, y no solo adquirirla como una solución aislada (Cimino, Corvello,
Troise, Thomas y Tani, 2025). Este anteproyecto retoma esa discusión aplicándola a un
caso concreto: Apollo Services, un ecosistema de agentes de IA conversacional diseñado
para unificar la gestión comercial multicanal de pymes de servicios, documentado
previamente como solución de negocio independiente de este trabajo académico. A partir
de ese caso, se busca formular y delimitar el problema de investigación que permitirá,
en fases posteriores de la especialización (Proyecto II), medir el efecto real de este
tipo de intervención tecnológica sobre la conversión comercial.

### Planteamiento y delimitación del problema

**Contexto**: los equipos comerciales de pymes de servicios (2 a 5 personas, perfil
representativo observado en organizaciones como las que documenta
`requerimientos/01-vision-y-alcance.md`) atienden manualmente conversaciones
provenientes de múltiples redes sociales. Cada canal se revisa por separado, sin una
bandeja unificada ni un criterio homogéneo para distinguir un contacto meramente
curioso (Seguidor) de uno con intención real de compra (Prospecto).

**Descripción del problema**: esta atención dispersa genera tres consecuencias
documentadas en el levantamiento de requerimientos del proyecto: (1) contactos que no
reciben respuesta a tiempo, (2) ausencia de un punto único de gestión y trazabilidad de
las conversaciones, y (3) pérdida del cierre comercial porque el agendamiento de citas
queda sujeto a que alguien confirme manualmente en un calendario compartido. Siguiendo
el principio metodológico trabajado en clase (clase-2), el problema no es "construir
una plataforma de IA" — la plataforma es la posible solución— sino la **pérdida de
conversión comercial por ausencia de un sistema de clasificación y seguimiento
automatizado de contactos multicanal**. Esta descripción es consistente con lo que la
literatura reciente identifica como barrera estructural de las pymes para beneficiarse
de la IA: no es la tecnología en sí lo escaso, sino la capacidad organizacional para
integrarla a procesos ya existentes (Cimino et al., 2025; Sánchez et al., 2025).

**Delimitación**: equipos comerciales de 2 a 5 personas, en pymes del sector servicios,
ubicadas en Bogotá, durante el periodo 2026. Se excluyen explícitamente del alcance de
esta formulación los canales que no forman parte del ecosistema evaluado (ej.
LinkedIn, fuera de alcance del caso de negocio por restricciones propias de esa
plataforma, documentado en `requerimientos/01-vision-y-alcance.md`).

### Pregunta de investigación y objetivos

**Pregunta de investigación**: ¿En qué medida la implementación de un sistema de
clasificación conversacional basado en inteligencia artificial, que unifica los
canales de contacto y automatiza la calificación de Seguidor/Prospecto, afecta la tasa
de conversión de prospectos a citas comerciales confirmadas en pymes de servicios de
Bogotá?

La pregunta cumple los criterios trabajados en clase: es concreta (una sola variable
dependiente — tasa de conversión de prospecto a cita confirmada— en función de la
presencia/ausencia del sistema de clasificación), medible (la conversión se cuenta
como proporción de prospectos que llegan a una cita confirmada sobre el total de
prospectos clasificados), y delimitada en población, sector y ciudad.

**Objetivo general**: Evaluar el efecto de la implementación de un sistema de
clasificación conversacional basado en inteligencia artificial en la tasa de
conversión de prospectos a citas comerciales confirmadas, en pymes de servicios de
Bogotá.

**Objetivos específicos**:
1. Caracterizar el proceso comercial actual (sin sistema de clasificación con IA) de
   una pyme de servicios multicanal, identificando los puntos donde se pierden
   prospectos.
2. Describir el diseño del sistema de clasificación conversacional (módulos de bandeja
   unificada, clasificación Seguidor/Prospecto y agendamiento, documentados en
   `diseno-tecnico/` de Apollo Services) propuesto como instrumento de intervención.
3. Establecer el procedimiento de medición de la tasa de conversión de prospectos a
   citas confirmadas, antes y después de la intervención.
4. Analizar los resultados esperados para determinar la magnitud del efecto y las
   condiciones organizacionales que lo favorecen o lo limitan, en línea con lo que la
   literatura reporta sobre capacidades dinámicas como factor mediador del beneficio de
   la IA (Cimino et al., 2025).

Título, pregunta y objetivo general comparten explícitamente los mismos términos
centrales —clasificación conversacional con IA, conversión de prospectos, citas
comerciales, pymes de servicios de Bogotá— cumpliendo la regla de coherencia exigida en
clase y en el criterio 3 de la rúbrica.

### Justificación del proyecto

La pertinencia de este anteproyecto se sustenta en tres planos. Primero, en el plano
práctico: la pérdida de prospectos por atención multicanal desorganizada es un problema
de negocio real y vigente, no hipotético, documentado en el levantamiento de
requerimientos de un proyecto en desarrollo activo (Apollo Services). Segundo, en el
plano académico: la literatura reciente coincide en que la adopción de IA en pymes
depende de variables organizacionales más que puramente tecnológicas (Popa et al.,
2025; Sánchez et al., 2025), pero hay relativamente poca evidencia empírica centrada en
el efecto directo sobre la conversión comercial en el contexto específico de pymes de
servicios latinoamericanas — este anteproyecto aporta un caso delimitado que puede
contribuir a cerrar ese vacío. Tercero, en el plano profesional: estudios sobre
chatbots conversacionales en atención al cliente muestran mejoras medibles en
satisfacción y conversión cuando la herramienta está bien integrada al proceso de
negocio (Ghosh et al., 2024; Ramki et al., 2024), lo que valida que medir ese efecto en
un caso real tiene valor replicable para otras pymes con restricciones similares de
presupuesto tecnológico.

### Alcances, limitaciones y viabilidad

**Alcances**: esta ACA 1 formula y delimita el problema de investigación (incluyendo
título, pregunta, objetivos y justificación); no mide todavía resultados reales — eso
corresponde al desarrollo metodológico y a la ejecución, que se abordan en ACA
posteriores de esta materia y, de ser necesario, en Proyecto II.

**Limitaciones**: (1) el estudio se centra en un único caso de intervención (Apollo
Services aplicado a una pyme de servicios), por lo que sus hallazgos no son
generalizables sin validación adicional en otros sectores; (2) la medición de la
variable de conversión depende de que la organización lleve un registro consistente de
sus interacciones antes y después de la intervención, lo cual es un requisito
operativo que debe confirmarse con la empresa caso antes de avanzar a la fase de
desarrollo metodológico; (3) la propuesta se limita a dos canales ya cubiertos por el
sistema (WhatsApp e Instagram/Facebook) y no evalúa canales adicionales fuera del
alcance documentado del proyecto (ej. LinkedIn).

**Viabilidad**: es académicamente viable porque el caso de negocio ya existe
documentado y operativo (no requiere construir el sistema desde cero para la
especialización); es operativamente viable porque los módulos de clasificación y
agendamiento ya están diseñados como flujos reutilizables; y es temporalmente viable
dentro de las 12 semanas del curso porque el alcance de esta ACA se limita a la
formulación del problema, no a su ejecución completa — la recomendación de 1 a 2
variables de la Fase de planteamiento de clase (clase-2) se respeta al centrar el
estudio en una sola variable dependiente medible.

### Referencias (APA 7)

Cimino, A., Corvello, V., Troise, C., Thomas, A., & Tani, M. (2025). Artificial
intelligence adoption for sustainable growth in SMEs: An extended dynamic capability
framework. *Corporate Social Responsibility and Environmental Management, 32*(5),
6120–6138. https://doi.org/10.1002/csr.70019

Ghosh, S., Ness, S., & Salunkhe, S. (2024). The role of AI enabled chatbots in
omnichannel customer service. *Journal of Engineering Research and Reports, 26*(6),
1–10. https://doi.org/10.9734/jerr/2024/v26i61184

Popa, R.-G., Popa, I.-C., Ciocodeică, D.-F., & Mihălcescu, H. (2025). Modeling AI
adoption in SMEs for sustainable innovation: A PLS-SEM approach integrating TAM,
UTAUT2, and contextual drivers. *Sustainability, 17*(15), 6901.
https://doi.org/10.3390/su17156901

Ramki, R., Gopi, V., R., V., Markan, R., Natarajan, S., & Rajalakshmi, M. (2024).
AI-powered chatbots in customer service: Impact on brand loyalty and conversion
rates. *Economic Sciences, 20*(2). https://doi.org/10.69889/vs5gtv52

Sánchez, E., Calderón, R., & Herrera, F. (2025). Artificial intelligence adoption in
SMEs: Survey based on TOE–DOI framework, primary methodology and challenges. *Applied
Sciences, 15*(12), 6465. https://doi.org/10.3390/app15126465

## 4. Autorevisión contra el enunciado y los criterios de aceptación

| Criterio | Nivel alcanzado | Evidencia |
|---|---|---|
| 1. Planteamiento y delimitación del problema | Máximo (1.0) | Contexto, descripción (evita confundir problema con solución) y delimitación explícita (población, sector, ciudad, periodo) en la sección correspondiente. |
| 2. Introducción | Máximo (1.0), sujeto a redacción final en el documento entregable | Incorpora las 5 referencias exigidas, integradas en el argumento (no solo citadas al final). |
| 3. Pregunta de investigación y objetivos | Máximo (1.0) | Pregunta medible y delimitada; objetivo general y 4 específicos coherentes y en la misma terminología que el título. |
| 4. Justificación del proyecto | Máximo (1.0) | Tres planos (práctico, académico, profesional), cada uno sustentado con fuente académica real. |
| 5. Alcances, limitaciones y viabilidad | Máximo (1.0) | Alcance delimitado explícitamente a la formulación (no a la ejecución); 3 limitaciones concretas; viabilidad argumentada en 3 dimensiones. |
| 6. Calidad académica, fuentes y APA 7 | Alto, pendiente de verificación tipográfica final en el documento Word (sangría francesa, cursivas) | 5 fuentes reales verificadas por DOI vía CrossRef, referenciadas en formato APA 7. |

No queda ningún criterio sin cobertura de contenido. El único ajuste que depende del
paso de generación del documento (Fase 10) es que el formato APA 7 real (sangría
francesa en la lista de referencias, interlineado doble, fuente Times New Roman 12pt)
se aplique correctamente en el `.docx` — eso se verifica leyendo el PDF generado, no
se asume.
