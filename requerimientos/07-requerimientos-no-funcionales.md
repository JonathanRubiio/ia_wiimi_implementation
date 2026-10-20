# 7. Requerimientos No Funcionales

## Volumetría

Referencia inicial para dimensionar la primera versión: ~100 posibles clientes al mes,
con 12–25 mensajes conversacionales por caso.

## Tiempo de respuesta

El Agente externo no necesita responder de forma instantánea; un rango de **30 a 120
segundos** es aceptable para no perder la naturalidad de la conversación.

## Protección de datos personales (Colombia — Ley 1581 de 2012, Habeas Data)

- Antes de capturar datos de un **Prospecto** (nombre, correo, teléfono, empresa), el
  agente debe pedir **consentimiento explícito**, con un mensaje tipo: "¿deseas continuar
  con una consultoría? Tus datos se usarán para que el equipo comercial te contacte".
- Para **Seguidores**: se guarda solo lo mínimo necesario para categorizarlos, sin
  tratamiento pleno de datos personales, ya que no avanzan en el funnel comercial.
- **Pendiente**: validar con asesoría legal una Política de Tratamiento de Datos
  Personales antes del lanzamiento comercial. No bloquea el inicio del diseño técnico.

## Arquitectura de despliegue

- El sistema **no es multi-tenant compartido**. Cada organización cliente del producto
  tiene su propia infraestructura/instancia independiente (base de datos y despliegue
  propios).
- Cuando se vende el producto a una nueva organización, se **duplica la infraestructura
  completa** para ese cliente específico.
- Esto simplifica el modelo de datos (sin aislamiento multi-tenant a nivel de esquema),
  pero implica que el proceso de alta de una nueva instancia debe ser repetible y
  plantillable.

## Autoservicio de conexión de redes

Que el Administrador pueda conectar/desconectar redes sociales por sí mismo es un
**plus deseable, no un requisito obligatorio** de la primera versión. Puede configurarse
manualmente al desplegar cada instancia si el autoservicio aún no está disponible.

## Resiliencia ante caída del bot

- **Monitoreo de salud + alerta inmediata** al Administrador/Líder por otro canal cuando
  el Agente externo deja de responder.
- **Mensaje automático de contingencia** al cliente ("en breve te contactamos") para que
  no perciba silencio total mientras el agente está caído.
- La atención mientras tanto pasa a ser manual (estado `atencion_manual`).

## Licenciamiento por módulo (feature-gating)

El Panel de Administración se despliega siempre con la **misma estructura base
completa** para cualquier organización; las funciones de los módulos (M1–M6, capa 8) no
contratados quedan **deshabilitadas** según el plan o servicios comprados, en vez de
construir paneles distintos por cliente.

## Capacidad multimodal

El Agente externo debe poder procesar **texto, audio e imágenes** enviados por el
cliente. Ese contenido no se usa para tomar decisiones de flujo — solo alimenta, como
referencia, el Resumen de cliente.

## Candidatos tecnológicos mencionados (no son decisión de esta fase)

A evaluar en la fase de diseño técnico, una vez cerrado este levantamiento:

- **WhatsApp**: canal externo principal hacia clientes en Colombia.
- **Telegram**: canal interno candidato para la interacción del equipo comercial con el
  Agente interno de seguimiento y el Agente conversacional de Gerencia.
- **n8n**: candidato para orquestar el Agente externo.
- **OpenClaw** (openclaw.ai): agente de IA local, candidato para el Agente interno de
  seguimiento y para la Fase 3 (asistente del equipo).
- **Google Calendar / Google Meet**: integración deseada para el agendamiento de
  reuniones.
