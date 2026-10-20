# 1. Visión y Alcance

## Problema de negocio

Las organizaciones pierden dinero en la interacción con clientes potenciales porque:

- Los contactos llegan por múltiples redes (WhatsApp, Facebook, Instagram, Twitter, LinkedIn, etc.) de forma dispersa.
- No hay tecnificación para responder a tiempo.
- No existe un punto único de gestión de esas conversaciones.
- Se pierde el corte/cierre con el cliente por falta de seguimiento estructurado.

## Visión del producto

El producto se concibe en **3 fases**, trabajadas en paralelo (no secuenciales ni
excluyentes entre sí), para validar todo el flujo de punta a punta desde el inicio:

### Fase 1 — Bandeja unificada + Bot comercial
*(foco detallado de este levantamiento — ver capas 2 a 7)*

- Unificación de conversaciones de redes sociales en un único filtro, estilo CRM.
- Un agente de IA externo conversa con todo contacto, lo clasifica (Seguidor vs
  Prospecto), recolecta sus datos y coordina el agendamiento de una reunión comercial.
- Un agente de IA interno da seguimiento al equipo comercial tras cada reunión, para
  registrar el resultado y mantener la trazabilidad organizacional.

### Fase 2 — Dashboard gerencial
Estadísticas consolidadas de todo el flujo (chats respondidos, prospectos, reuniones,
conversiones a cliente), con dos vías de acceso: dashboard web con login, y consulta en
lenguaje natural vía un canal conversacional (Telegram/WhatsApp).

### Fase 3 — Agente de IA local asistente del equipo
Asistente que acompaña al equipo comercial en el día a día (candidato evaluado: OpenClaw
— openclaw.ai, a definir en diseño técnico).

## Objetivo y métricas de éxito

Visibilidad estadística con alta confianza sobre:

- Cuántos chats se respondieron.
- Cuántos potenciales clientes (Prospectos) ingresaron.
- Cuántos fueron atendidos por el equipo comercial.
- Cuántos de esos se convirtieron en Clientes reales.

## Stakeholders y modelo de negocio

- Producto a vender a **distintas organizaciones**, orientado a equipos comerciales.
- Cada organización usaría el sistema para focalizar sus redes sociales de cara a ventas
  y obtener estadísticas de ese proceso.
- Es un proyecto personal, autofinanciado, concebido para ser comercializado.

## Alcance

- Las 3 fases forman parte de la visión completa del producto y se desarrollan en
  paralelo. El detalle fino de procesos, reglas y casos de uso se centra primero en la
  Fase 1, por ser la base operativa de las otras dos.
- No hay exclusiones adicionales definidas en esta versión.

## Restricciones de negocio

- Sin plazo ni presupuesto fijo — enfoque iterativo ("construir y mejorar en la marcha").
- Sin regulación o integración obligatoria declarada, más allá de la integración deseada
  con Google Calendar/Meet para agendamiento, y de la Ley de Protección de Datos Personales
  de Colombia (ver capa 7 — Requerimientos No Funcionales).
