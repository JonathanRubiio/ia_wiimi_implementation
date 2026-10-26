# Solución inicial — Proyecto I / ACA 1

- **Vinculación**: proyecto principal (Apollo Services), línea autorizada "Uso y
  adaptación de IA para entornos productivos".
- **Clases de referencia**: clase-1, clase-2 (marco metodológico de construcción de
  título, planteamiento del problema y pregunta de investigación).
- **Enunciado**: trabajo/enunciado-aca1.txt

## Lectura del problema

El enunciado de ACA 1 no entrega un tema concreto — solo fija el propósito de la
entrega: formular y delimitar el problema de investigación del anteproyecto y lograr
coherencia inicial entre sus piezas (título, problema, pregunta). Es decir, esta ACA
no pide todavía una solución técnica desarrollada — pide la **formulación correcta del
problema que el anteproyecto se propone estudiar**, siguiendo el método visto en clase:
título preliminar (≤21 palabras, sin punto final) → descripción del problema (nunca la
solución) → pregunta de investigación (un supuesto de solución, medible, delimitada en
tiempo/espacio/población) → objetivos (general + 3-4 específicos) → justificación breve.

Como el equipo decidió vincular este anteproyecto a Apollo Services (el CRM comercial
multicanal con IA ya documentado en `requerimientos/` y `diseno-tecnico/` de este
repo), el problema de investigación se ancla en el problema de negocio real ya descrito
en `requerimientos/01-vision-y-alcance.md`: pymes con equipos comerciales pequeños
pierden oportunidades de venta porque los contactos llegan dispersos por varias redes
sociales (WhatsApp, Instagram, Facebook), sin un punto único de gestión ni
tecnificación para responder a tiempo, lo que rompe el seguimiento estructurado y hace
perder el cierre con el cliente.

Siguiendo la regla explícita de clase ("el problema no es la plataforma que se va a
construir, es lo que pasa antes de que exista esa plataforma"), el problema de
investigación NO es "cómo construir Apollo Services" — es la pérdida de conversión
comercial que sufren estas pymes por falta de un sistema de clasificación y
seguimiento automatizado de sus contactos multicanal.

## Primer enfoque de solución (borrador de las piezas del anteproyecto)

**Título preliminar** (20 palabras, sin punto final):
"Efecto de la clasificación conversacional con IA en la conversión de prospectos a
citas en pymes de servicios de Bogotá"

**Descripción y delimitación del problema** (borrador):
Equipos comerciales pequeños (2-5 personas) de pymes de servicios en Bogotá atienden
WhatsApp, Instagram y Facebook por separado, sin bandeja única ni clasificación
automática de quién es un simple Seguidor y quién es un Prospecto real. Sin ese
filtro, los contactos con intención de compra se mezclan con los que solo interactúan
pasivamente, las respuestas se retrasan y el agendamiento de citas queda sujeto a que
alguien confirme manualmente en un calendario compartido — lo que genera pérdida de
prospectos que nunca llegan a una cita comercial confirmada. Delimitación: equipos
comerciales de 2-5 personas, sector servicios, ciudad de Bogotá, periodo 2026.

**Pregunta de investigación** (borrador):
¿En qué medida la implementación de un sistema de clasificación conversacional basado
en inteligencia artificial, que unifica los canales de contacto y automatiza la
calificación de Seguidor/Prospecto, afecta la tasa de conversión de prospectos a citas
comerciales confirmadas en pymes de servicios de Bogotá?

Variable única (según la recomendación de la Fase de clase de usar 1-2 variables, no
más, dado el tiempo de 12 semanas): tasa de conversión de prospecto a cita comercial
confirmada, en función de la presencia/ausencia del sistema de clasificación
conversacional con IA.

**Objetivo general** (borrador):
Evaluar el efecto de la implementación de un sistema de clasificación conversacional
basado en inteligencia artificial en la tasa de conversión de prospectos a citas
comerciales confirmadas, en pymes de servicios de Bogotá.

**Objetivos específicos** (borrador, 4 — se redactan ya en forma de acción, no de
pregunta, siguiendo la indicación de clase):
1. Caracterizar el proceso comercial actual (sin sistema de clasificación con IA) de
   una pyme de servicios multicanal, identificando los puntos donde se pierden
   prospectos.
2. Describir el diseño del sistema de clasificación conversacional (módulos M1, M2 y
   M6 de Apollo Services) propuesto como instrumento de intervención.
3. Establecer el procedimiento de medición de la tasa de conversión de prospectos a
   citas confirmadas, antes y después de la intervención.
4. Analizar los resultados esperados para determinar la magnitud del efecto y las
   condiciones organizacionales que lo favorecen o lo limitan.

**Justificación** (borrador):
La fuga de prospectos por falta de tecnificación comercial es un problema de negocio
documentado y recurrente en pymes de bajo presupuesto tecnológico (ver
`requerimientos/01-vision-y-alcance.md`). Estudiar el efecto de un sistema de
clasificación conversacional con IA aporta evidencia empírica replicable para que este
tipo de organizaciones decida si una intervención tecnológica de este tipo justifica
su inversión, y sienta una base metodológica que Proyecto II podría desarrollar hasta
la implementación real.

## Pendiente antes de la solución completa (Fase 9)

- Pedir los criterios de aceptación/puntaje reales de ACA 1 (Fase 7) para verificar que
  esta formulación cubre exactamente lo que se califica (p. ej. si exige explícitamente
  marco referencial o solo problema+pregunta+objetivos+justificación).
- Revisar si el enunciado trae lista de control adicional no mencionada en el texto
  pegado por el usuario.
