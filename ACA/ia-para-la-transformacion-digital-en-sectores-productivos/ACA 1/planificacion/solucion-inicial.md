# Solución inicial — ACA 1 (borrador de trabajo)

Vinculado al proyecto principal: **Apollo Services** (CRM comercial multicanal con IA). El caso
organizacional del ACA se construye directamente sobre el problema de negocio ya documentado
en `requerimientos/01-vision-y-alcance.md` y la arquitectura ya cerrada en `diseno-tecnico/`.

## 1. Problema organizacional (borrador)
Organización tipo: una pyme con equipo comercial pequeño (ej. 2-4 personas) que vende por
varias redes sociales (WhatsApp, Instagram, Facebook) de forma simultánea. Los contactos llegan
dispersos por cada canal, no hay un punto único de gestión, no hay tecnificación para responder
a tiempo y se pierde el cierre/seguimiento con el cliente potencial por falta de trazabilidad
estructurada. Esto se traduce en pérdida directa de oportunidades de venta — el problema es de
negocio (ventas perdidas), no técnico.

## 2. Sector productivo (borrador)
Sector servicios / comercio minorista con venta B2C vía redes sociales (aplicable también a
sectores como salud estética, educación o inmobiliaria — el producto es agnóstico de vertical,
se vende a cualquier organización con equipo comercial que opere multicanal).

## 3. Solución de IA (borrador)
**Apollo Services**, modelo modular (M1-M6), vendido en sub-paquetes independientes:
- M1 — Bandeja unificada (CRM de conversaciones multicanal).
- M2 — Agente externo que clasifica Seguidor/Prospecto y recolecta datos obligatorios.
- M3 — Agente de bienvenida/categorización de seguidores (evento "seguir").
- M4 — Agente de consulta en lenguaje natural para Gerencia (solo lectura operacional).
- M5 — Dashboard gerencial con estadísticas.
- M6 — Agente de agendamiento y cierre + seguimiento interno post-reunión con el equipo comercial.
Para el MVP del caso (equipo comercial pequeño), el paquete mínimo viable es M1 + M2 + M6.

## 4. Arquitectura (borrador, sujeta a diagrama formal en solucion.md)
Usuario/contacto → canal (WhatsApp / Instagram / Facebook) → API del canal (360dialog /
Meta Graph API) → n8n (motor de orquestación, aloja los agentes) → LLM (Claude + Gemini) →
Supabase/Postgres (base de datos compartida — los módulos nunca se llaman entre sí
directamente, solo observan cambios de estado) → App Next.js (M1 bandeja / M5 dashboard) →
supervisión humana (Líder comercial reasigna casos; Administrador gestiona la plantilla de
compañía).

## 5. Tecnologías (borrador)
n8n (automatización), Claude + Gemini (modelos de IA), Supabase (Postgres + Realtime + Auth +
Storage), Next.js (app web), Google Calendar/Meet (agendamiento), WhatsApp Business API
(360dialog), Instagram/Facebook Graph API, Docker Compose + Caddy (despliegue aislado por
cliente, un stack por organización — no multi-tenant compartido).

## 6. Riesgos preliminares
Dependencia tecnológica de proveedores externos (Meta, Anthropic, Google), saturación del
sistema si el volumen de prospectos supera lo dimensionado (~100 prospectos/mes por cliente),
privacidad de datos personales (pendiente política formal de Habeas Data antes de lanzamiento
comercial), latencia en picos de conversación, manejo manual de secretos `.env` por cliente
(riesgo operativo a escala), costos variables por consumo de tokens.

## 7. Impacto organizacional preliminar
Positivo: visibilidad estadística confiable del embudo comercial (chats respondidos → prospectos
→ reuniones → clientes), reducción de oportunidades perdidas, la Líder comercial pasa de
responder todo manualmente a supervisar y reasignar. Negativo/a vigilar: resistencia inicial del
equipo comercial a sentirse "vigilado" por el dashboard, dependencia de mantener actualizada la
plantilla de compañía (fuente única de contenido dinámico para M2/M3).

## 8. Costos estimados (conceptual, borrador)
Infraestructura VPS compartida por cliente (bajo costo al volumen actual), consumo de tokens de
Claude/Gemini por conversación, costo por conversación iniciada de WhatsApp Business API,
almacenamiento Supabase, Google Calendar sin costo adicional.

## 9. Supervisión humana (borrador)
Políticas RLS controlan el acceso humano (los agentes usan `service_role` y las omiten, pero
operan bajo system prompts con funciones acotadas — M4 nunca escribe/modifica datos, solo
consulta). La Líder comercial revisa y reasigna casos en M1; tras cada reunión, el agente interno
(M6) genera un `resumen_cierre` que el equipo comercial valida.

---
*Este es un borrador rápido para orientar la Fase 7 (criterios de aceptación, ya verbatim en el
enunciado) y servir de base a `solucion.md`, que debe desarrollarse con el rigor completo
exigido por la rúbrica.*
