# Solución — ACA 1: Ecosistema de IA empresarial

**Vinculación**: este ACA está vinculado al proyecto principal del equipo, **Apollo Services**
(CRM comercial multicanal con IA), ya en fase de diseño técnico cerrado. Todo el contenido de
este documento se basa en las decisiones de negocio y técnicas ya tomadas y documentadas en
`requerimientos/` y `diseno-tecnico/` del repositorio del proyecto — no se usan fuentes externas
ni se inventan datos; los costos y cifras de este documento provienen de la investigación
tecnológica real (`diseno-tecnico/01-investigacion-tecnologica.md`, octubre 2026) hecha para el
proyecto.

---

## 1. Problema organizacional

**Bienestar Integral S.A.S.** es una pyme del sector salud estética (dos sedes, Bogotá y
Medellín) con un equipo comercial de 3 personas encargado de convertir consultas de potenciales
pacientes en citas agendadas. La organización promociona sus tratamientos (odontología estética,
dermatología, nutrición) por WhatsApp Business, Instagram y Facebook simultáneamente.

El problema real: los contactos llegan dispersos en tres canales distintos, sin un punto único
de gestión. Cada integrante del equipo comercial revisa manualmente cada red por separado, no
hay forma de saber a tiempo real cuántos contactos están sin responder, y no existe trazabilidad
estructurada de quién es Seguidor, quién es Prospecto con interés real, ni en qué punto del
proceso de agendamiento quedó cada uno. El resultado medible: pacientes potenciales que escriben
y no reciben respuesta a tiempo, o que agendan pero cuya cita nunca queda confirmada formalmente
en una agenda compartida, se pierden como oportunidad de venta sin que nadie en la organización
lo note hasta que ya es tarde. Es un problema de negocio (pérdida de ingresos por fuga de
prospectos), no un problema técnico de ninguna de las plataformas individuales.

## 2. Sector económico

Sector **servicios — salud estética**, con un modelo comercial B2C intensivo en redes sociales.
Se ubica en este sector porque su actividad principal es la prestación de servicios de salud
estética a pacientes particulares, y su canal de captación y conversión de clientes es,
mayoritariamente, digital y conversacional (no una sala de ventas física). Este tipo de
organización es representativo del segmento objetivo de Apollo Services: equipos comerciales
pequeños (2 a 5 personas) que dependen de redes sociales para vender, sin capacidad ni interés en
construir su propia infraestructura de IA desde cero.

## 3. Solución basada en inteligencia artificial

La solución es **Apollo Services**, desplegado para Bienestar Integral S.A.S. con el paquete
mínimo viable de tres módulos (de los seis que ofrece el producto de forma independiente):

- **M1 — Bandeja unificada**: centraliza en un único tablero, tipo CRM, las conversaciones de
  WhatsApp, Instagram y Facebook, reemplazando la revisión manual canal por canal.
- **M2 — Agente de respuesta a potenciales clientes**: agente conversacional que atiende todo
  contacto entrante, lo clasifica como *Seguidor* (sin intención de compra inmediata) o
  *Prospecto* (interesado en un tratamiento), y recolecta los datos obligatorios de la encuesta
  (tratamiento de interés, sede preferida, disponibilidad) antes de escalar a agendamiento.
- **M6 — Agente de agendamiento y cierre**: una vez el Prospecto tiene los datos completos,
  coordina la fecha de la cita con el paciente, la confirma con la Líder comercial, agenda la
  cita en Google Calendar (con enlace de Meet si la primera valoración es virtual) y, tras la
  cita, hace seguimiento con el equipo comercial para registrar el resultado (agendó tratamiento,
  no agendó, reagendó).

No se requiere desarrollo de software nuevo desde cero: los tres módulos ya están diseñados como
flujos de n8n reutilizables sobre la misma base de datos compartida (Supabase), por lo que el
esfuerzo de puesta en marcha para este cliente es de configuración (plantilla de la compañía,
credenciales de sus canales, preguntas de la encuesta), no de construcción de producto nuevo.

## 4. Arquitectura del ecosistema de IA

**Figura 1** (flujo completo, desde la entrada del paciente hasta la respuesta final):

```
Paciente (WhatsApp / Instagram / Facebook)
        │
        ▼
  API del canal (Meta Cloud API vía 360dialog, mismo Graph API para WhatsApp/IG/FB)
        │  webhook entrante
        ▼
   n8n (motor de orquestación — aloja los agentes M2 y M6)
        │
        ├──▶ si el mensaje trae audio o imagen → Gemini Flash (normalización a texto plano)
        │                                              │
        │          ◀───────────────────────────────────┘
        ▼
   Claude (motor conversacional único, M2) — clasifica Seguidor/Prospecto,
   recolecta datos de la encuesta según la Plantilla de Compañía
        │
        ▼
   Supabase / PostgreSQL (base de datos compartida)
   — M2 escribe `contacto`, `seguidor` o `prospecto` con `datos_completos = true`
        │  (M6 no es invocado directamente por M2: observa el cambio de estado)
        ▼
   n8n — M6 detecta `datos_completos = true`, coordina fecha con el paciente,
   confirma con la Líder comercial, crea el evento en Google Calendar (OAuth2
   por organización, con enlace de Meet si aplica)
        │
        ▼
   Supabase — se registra la `Oportunidad` y, tras la cita, el `resumen_cierre`
        │
        ▼
   App Next.js — sección M1 (bandeja: Líder ve y reasigna conversaciones) y
   sección M5-lite interna (vista de estado de Prospectos/Oportunidades)
        │
        ▼
   Supervisión humana — Líder comercial y equipo comercial validan clasificación,
   reasignan casos y confirman el resultado de cada reunión
```

Principio de diseño clave (ya cerrado en el proyecto, capa 8 de requerimientos): **los módulos
nunca se llaman directamente entre sí**. M2 no invoca a M6; M2 solo escribe el estado
(`datos_completos = true`) en la base de datos compartida, y M6 reacciona a ese estado de forma
autónoma. Esto permite vender M1, M2 o M6 de forma independiente, y que cada uno siga
funcionando aunque otro módulo no haya sido contratado por el cliente, siempre que el dato que
necesita exista en la base de datos (sin importar quién lo puso ahí).

## 5. Tecnologías involucradas

| Componente | Tecnología | Rol en el ecosistema |
|---|---|---|
| Canal de comunicación | WhatsApp Business (Meta Cloud API vía 360dialog), Instagram y Facebook (Meta Graph API) | Punto de entrada/salida de la conversación con el paciente |
| API/puente | Meta Cloud API / Graph API (mismo webhook para los 3 canales) | Transporta el mensaje entrante hacia el motor de automatización y la respuesta de vuelta |
| Motor de automatización | n8n (self-hosted) | Orquesta los flujos de M2 y M6, triggers por webhook y por Schedule (cron) |
| Modelo de lenguaje (conversacional) | Claude (Sonnet/Haiku) | Único motor conversacional de M2 — mantiene un tono consistente sin importar el canal de origen |
| Modelo de lenguaje (normalización de medios) | Gemini Flash | Convierte audio/imagen entrante a texto plano antes de que lo vea Claude — reduce costo y evita que Claude necesite soporte de audio nativo (no lo tiene) |
| Base de datos compartida | Supabase self-hosted (Postgres + Realtime + Auth + Storage) | Única fuente de verdad del estado (`contacto`, `prospecto`, `Oportunidad`, `resumen_cierre`); los módulos reaccionan a sus cambios vía Realtime, no se llaman entre sí |
| Calendario | Google Calendar API (OAuth2 por organización) + Google Meet | Agenda la cita y genera el enlace de videollamada automáticamente vía `conferenceData.createRequest` |
| Interfaz / dashboard | App Next.js (sección M1: bandeja de conversaciones) | Interfaz para que la Líder comercial supervise y reasigne casos |
| Infraestructura cloud | Docker Compose (Supabase + n8n + app) detrás de un reverse proxy Caddy, un stack aislado por cliente | Despliegue dedicado para Bienestar Integral S.A.S., sin compartir base de datos con otros clientes de Apollo Services |

## 6. Riesgos identificados

- **Dependencia tecnológica de Meta**: WhatsApp dejó de ser 100% gratuito desde octubre de 2026
  (1.000 mensajes de servicio gratis/mes/número, luego se cobra) — si el volumen de pacientes
  crece, el costo por conversación de Bienestar Integral S.A.S. crece con él. Riesgo operativo y
  de costos, no mitigable del lado del producto.
- **Saturación del sistema**: el stack está dimensionado para el volumen declarado del proyecto
  (~100 prospectos/mes por cliente). Una campaña de descuentos o temporada alta en la clínica
  podría generar un pico de concurrencia que el VPS asignado a este cliente no soporte si no se
  redimensiona a tiempo.
- **Errores de la IA (alucinaciones, falsos positivos en la clasificación)**: M2 puede clasificar
  mal a un paciente con intención real de compra como "solo Seguidor" (o viceversa), o entender
  mal un dato de la encuesta — por eso el flujo nunca permite que la IA tome la decisión final de
  agendar sin que la Líder comercial confirme (punto 9).
- **Privacidad de datos personales**: Bienestar Integral S.A.S. maneja datos de salud de sus
  pacientes (tipo de tratamiento consultado). El proyecto tiene pendiente, a nivel general, validar
  con asesoría legal una Política de Tratamiento de Datos Personales (Habeas Data, Colombia) antes
  del lanzamiento comercial — para un cliente del sector salud este riesgo es más sensible que el
  promedio y debe resolverse antes de poner en producción.
- **Latencia en la respuesta**: si llega una imagen (ej. una radiografía o foto de un diagnóstico
  previo) y Gemini Flash tarda en normalizarla a texto, el paciente puede percibir el chatbot como
  lento — mitigado por el diseño de separar la normalización de medios del motor conversacional
  (sección 4), pero sigue siendo un punto de latencia real a monitorear.
- **Manejo manual de secretos**: las credenciales de WhatsApp/Instagram/Facebook/Calendar de
  Bienestar Integral S.A.S. se gestionan hoy en un archivo `.env.<cliente>` manual, no en un
  gestor de secretos — aceptable al volumen actual de clientes del proyecto, pero es un riesgo
  operativo que crece si Apollo Services suma más clientes simultáneos.

## 7. Impacto organizacional

**Positivo**: el equipo comercial de Bienestar Integral S.A.S. deja de perder tiempo revisando
tres redes por separado; la Líder comercial gana visibilidad en tiempo real de cuántos contactos
están sin responder y puede reasignar casos desde un único tablero. El agendamiento deja de
depender de que alguien recuerde confirmar manualmente en un calendario compartido — reduce
directamente la fuga de prospectos que originó el problema (punto 1).

**Negativo / a vigilar**: el rol del equipo comercial cambia — de "responder todo manualmente"
pasa a "supervisar y confirmar lo que la IA ya adelantó", lo cual puede generar resistencia
inicial si no se comunica bien que el sistema no los reemplaza sino que filtra el trabajo
repetitivo (clasificación inicial, recolección de datos básicos). También aparece una
**dependencia tecnológica nueva**: si Apollo Services o alguno de sus proveedores (Meta, Claude,
Google Calendar) tiene una caída, el proceso comercial de Bienestar Integral S.A.S. se ve
directamente afectado, algo que antes no ocurría cuando el proceso era 100% manual.

## 8. Costos generales estimados (conceptual)

No se requieren valores exactos de facturación del cliente, sino la identificación de los
elementos de costo reales del stack ya investigado para el proyecto:

- **Consumo de tokens de los modelos de IA**: al volumen estimado para un cliente de este tamaño
  (≈100 casos/mes, entre 12 y 25 mensajes por caso ≈ 1.500–2.500 turnos/mes), el costo de LLM es
  marginal sin importar si se usa Claude Sonnet/Haiku o Gemini Flash para la normalización — la
  prioridad de elección fue capacidad (que Gemini soporte audio/imagen nativamente), no precio.
- **Costo por conversación de WhatsApp Business**: desde oct-2026, 1.000 mensajes de servicio
  gratis/mes/número y luego tarifa por conversación (referencia ~0.004–0.025 USD/mensaje según
  tipo) — variable según cuánto exceda Bienestar Integral S.A.S. ese umbral gratuito.
- **Instagram/Facebook (M3, no incluido en este MVP)**: si en una fase posterior se contrata M3,
  el nivel Normal (Instant Reply nativo de Meta) es gratuito; el nivel Premium (ManyChat
  Follow-to-DM) también es gratuito pero sujeto a elegibilidad (cuenta con ~1.000+ seguidores).
- **Infraestructura cloud**: un VPS por cliente corriendo el stack Docker Compose (Supabase + n8n
  + app) — costo fijo mensual bajo, independiente del volumen de conversaciones dentro del rango
  dimensionado.
- **Almacenamiento**: incluido en el mismo Supabase self-hosted (Storage), sin servicio adicional
  — solo crece si se almacenan muchos adjuntos de audio/imagen de los pacientes.
- **Calendario**: Google Calendar API no tiene costo adicional para este volumen de uso.

## 9. Supervisión humana (Human in the Loop)

La supervisión humana está diseñada en dos capas, consistentes con cómo ya está construido el
producto:

1. **Restricción por funciones acotadas, no solo por texto**: M2 no tiene una función genérica
   de "ejecutar cualquier acción" — solo puede invocar funciones específicas y auditable
   (`clasificar_contacto()`, `registrar_dato_encuesta()`), igual que M6 solo puede
   `agendar_cita()`, `confirmar_con_lider()`, `marcar_resultado_reunion()`. Ninguno de los
   agentes tiene una función de escritura libre en la base de datos ni de ejecución de comandos
   —el mismo principio que llevó a descartar frameworks de agente autónomo sin restricción de
   herramientas para este producto.
2. **Punto de intervención humana explícito**: la Líder comercial de Bienestar Integral S.A.S.
   revisa y reasigna conversaciones desde la bandeja (M1) antes de que lleguen a agendamiento
   definitivo, y confirma manualmente cada cita que M6 propone antes de que quede en firme en el
   calendario compartido. Tras cada reunión, el `resumen_cierre` que genera el agente de
   seguimiento es validado por el equipo comercial, no se asume como verdad definitiva — esto es
   lo que garantiza que un falso positivo de clasificación (punto 6) no termine convertido en una
   cita mal agendada sin que nadie lo revise.

Este componente es, además, el que permite que si en el futuro Bienestar Integral S.A.S. decide
ampliar el paquete contratado a M3, M4 o M5, no cambie el principio de que ningún agente decide
de forma definitiva sobre un paciente real sin que una persona del equipo comercial lo confirme.

## Conclusiones

El ecosistema de IA propuesto no reemplaza al equipo comercial de Bienestar Integral S.A.S.:
automatiza la parte repetitiva y propensa a error humano (clasificación inicial, recolección de
datos, coordinación de fecha), y libera al equipo para enfocarse en lo que la IA no puede hacer
— la relación con el paciente y la decisión final sobre cada caso. La arquitectura modular del
proyecto (módulos independientes que reaccionan a estado compartido en base de datos, nunca se
llaman entre sí) permite que esta organización empiece con el paquete mínimo (M1+M2+M6) y
escale a más módulos sin necesidad de rediseñar lo ya construido.
