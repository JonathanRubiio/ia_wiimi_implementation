# Notas de recolección — Borrador de trabajo

## Etapa 1 — Visión y Alcance

_(cerrada)_

### Problema de negocio

Las organizaciones pierden dinero en la interacción con clientes potenciales porque:

- Los contactos llegan por múltiples redes (WhatsApp, Facebook, Instagram, Twitter, LinkedIn, etc.) de forma dispersa.
- No hay tecnificación para responder a tiempo.
- No hay un punto único de gestión de esas conversaciones.
- Se pierde el corte / cierre con el cliente por falta de seguimiento estructurado.

### Visión del producto (multi-fase)

El producto se concibe en 3 fases de producto (distintas de las 7 etapas de este levantamiento):

**Fase 1 — Bandeja unificada + Bot comercial (foco actual del levantamiento)**

- Unificación de conversaciones de redes sociales en un único filtro tipo CRM.
- **Canal 1 (IA de calificación):** interactúa primero con quien escribe, lo categoriza (ej. cliente potencial, busca empleo, otro). Foco inicial: detectar clientes potenciales.
- **Canal 2 (IA de levantamiento + enlace comercial):** si es cliente potencial, hace una encuesta corta (nombre, empresa, qué desea) y entrega el contacto a una líder de área comercial, quien focaliza el caso a un usuario comercial.
- **Agendamiento autónomo:** el bot, en el mismo punto de contacto, decide agendar una reunión (Google Calendar / Meet) sin intervención manual, y notifica a la usuaria gerencial (vía agente, mencionado como "open claw" — term a confirmar) con contexto del cliente antes de la reunión.
- **Seguimiento post-reunión:** tras la reunión, el agente pregunta qué sucedió (pasa a cierre / sigue como prospecto / no hubo acuerdo) y guarda el resultado en una BD compartida para trazabilidad organizacional.

**Fase 2 — Dashboard gerencial**

- Estadísticas de todo lo anterior para gerencia.

**Fase 3 — Agente de IA local asistente del equipo**

- Asistente (mencionado como "open claw") que acompaña al equipo comercial en el día a día.

> Pendiente aclarar: si "open claw" es el nombre del agente propio a construir o una herramienta externa de terceros.

### Objetivo / métricas de éxito

Visibilidad estadística con alta confianza sobre:

- Cuántos chats se respondieron.
- Cuántos potenciales clientes ingresaron.
- Cuántos fueron atendidos por el equipo comercial.
- Cuántos de esos se convirtieron en clientes reales.

### Stakeholders / modelo de negocio

- Producto a vender (SaaS) a **distintas organizaciones**, orientado a equipos comerciales.
- Cada organización cliente usaría el sistema para focalizar sus redes y obtener estadísticas de ventas sobre redes sociales.
- Implica naturaleza **multi-tenant** (a confirmar en Actores).

### Alcance

- Las 3 fases se trabajan **en paralelo** (no es secuencial excluyente): se avanza en todas a la vez para verificar que todo el flujo esté siendo tratado. El detalle fino (procesos/reglas/casos de uso) se centra primero en Fase 1 por ser la base operativa de las otras dos.
- Sin exclusiones adicionales explícitas todavía.

### Candidatos tecnológicos mencionados (NO son decisión — se evalúan en fase de diseño técnico, después de cerrar specs)

- **WhatsApp**: canal externo principal hacia clientes en Colombia.
- **Telegram**: canal interno candidato para que el equipo comercial interactúe con el agente de seguimiento.
- **n8n**: candidato para orquestar el agente externo (Canal 1+2, calificación → encuesta → agendamiento).
- **OpenClaw (openclaw.ai)**: agente de IA local, candidato para el agente interno de seguimiento post-reunión (y para la Fase 3, asistente del equipo), por sus conexiones/integraciones.
- **Google Calendar / Google Meet**: integración deseada para agendamiento automático de reuniones.

### Restricciones de negocio

- Proyecto personal, autofinanciado, pensado para vender.
- Sin plazo ni presupuesto fijo — enfoque iterativo ("trabajar y en la marcha mejorarlo").
- Sin regulación o integración obligatoria declarada aún, más allá de Google Calendar/Meet como integración deseada para agendamiento.

---

## Etapa 2 — Actores y Roles

_(cerrada)_

- **Organización**: una sola organización por ahora (no multi-tenant).
- **Contacto/Visitante**: cualquier persona que escribe a alguna red social de la organización. Lo atiende siempre el agente externo primero.
- **Seguidor**: clasificación final del contacto cuando el agente externo determina que NO es cliente potencial (ej. busca empleo). Recibe un mensaje de cierre/finalización.
- **Cliente potencial / Prospecto**: clasificación final del contacto cuando el agente externo determina que SÍ es cliente potencial. Pasa al resto del flujo (encuesta, agendamiento).
- **Agente IA externo (Canal 1 + Canal 2 — mismo agente, conversación continua con el cliente)**: habla con el contacto por WhatsApp u otra red social, lo clasifica (Seguidor vs Prospecto), si es Prospecto hace una encuesta corta (nombre, empresa, necesidad) y agenda la reunión (Calendar/Meet) de forma autónoma, sin botón ni intervención manual.
- **Agente IA interno de seguimiento (distinto del agente externo, candidato: OpenClaw vía Telegram)**: un día después de la reunión, contacta al comercial (no al cliente) para preguntar qué pasó (cierre / sigue prospecto / sin acuerdo) y guarda el resultado en la BD compartida.
- **Líder de área comercial**: rol único (una sola persona por ahora). Recibe el prospecto calificado con su contexto antes de la reunión, decide si atiende ella misma o lo focaliza a un usuario comercial, y es quien participa en la reunión (ella o la persona a quien asignó).
- **Usuario comercial**: atiende al cliente directamente solo cuando la líder lo asigna (no siempre interviene).
- **Administrador**: da de alta usuarios, conecta las redes sociales de la organización, configura el bot. *(pendiente confirmar si es la misma persona que la Líder comercial o un rol técnico aparte)*
- **Gerencia**: NO participa en reuniones ni en el flujo operativo. Solo consume el dashboard y resúmenes estadísticos (Fase 2). Puede haber **más de una persona** con este rol.

**Resuelto:**

- **Administrador**: rol técnico aparte, es el dueño del producto. Controla qué personas tienen qué permisos (alta de usuarios, conexión de redes, configuración del bot).
- **"Focalizar"**: la Líder reasigna la propiedad de la conversación de WhatsApp (dentro del inbox unificado tipo CRM) a un Usuario comercial, quien continúa hablando directamente con el cliente por ese mismo hilo. No es un mensaje aparte por Telegram — es una reasignación dentro del propio sistema.

## Etapa 3 — Procesos de Negocio

_(cerrada)_

### Flujo principal (Fase 1) — confirmado

1. Contacto escribe por una red social (WhatsApp principalmente en Colombia).
2. Agente externo conversa y clasifica: **Seguidor** (no prospecto, recibe mensaje de cierre) vs **Prospecto**.
3. Si Prospecto: agente hace encuesta corta (nombre, empresa, necesidad).
4. Agente agenda la reunión automáticamente (Calendar/Meet), sin intervención manual.
5. Líder comercial recibe el caso con contexto antes de la reunión.
6. Líder decide: atender ella misma, o **focalizar** (reasignar la conversación dentro del inbox) a un Usuario comercial.
7. Se realiza la reunión.
8. Un día después, Agente interno de seguimiento pregunta al comercial qué pasó (cierre / sigue prospecto / sin acuerdo).
9. Resultado se guarda en la BD compartida → alimenta estadísticas (Fase 2).

### Sub-flujo: conversación abandonada

- Si el contacto abandona antes de terminar la encuesta → se guarda como **prospecto parcial** con la fase en que quedó.
- Rutina automática: 24h después del último contacto, se le envía un mensaje retomando esa fase.

### Sub-flujo: falla el agendamiento automático

- Si el agente no logra agendar (cliente no da disponibilidad, no hay cupo, etc.) → se envía aviso a un **grupo aparte** donde está la Líder comercial: "no se pudo agendar cita con [cliente], realiza el proceso manual".
- Luego el bot le pregunta a la Líder (como parte de la misma rutina) la fecha y hora en que quedó la reunión manual, para mantener el registro.
- **Regla configurable** (candidata a Etapa 5): tiempo máximo permitido para concretar/agendar una reunión con el cliente (ej. 7–14 días) — debe ser un parámetro configurable por el Administrador, no un valor fijo.

### Sub-flujo: seguimiento post-reunión (rutina)

- Rutina diaria, al inicio del día.
- Solo se activa si existe una reunión ya realizada pendiente de calificar (si no hay ninguna, no se envía nada).
- Si el comercial no responde, el bot insiste diariamente hasta obtener respuesta (no hay escalamiento a la Líder descrito aún).

### Capacidad transversal requerida

- El agente externo debe poder procesar **texto, audio e imágenes** que envíe el cliente (no solo texto).

**Resuelto:**

- La Líder, al focalizar, **no pierde visibilidad**: queda como supervisora del hilo.
- Audio/imagen del cliente: **no son interpretativos para decisiones de flujo**. Lo único que el agente interpreta para decidir es la clasificación del contacto (Seguidor vs Prospecto). El contenido de audio/imagen solo alimenta, como referencia, un **formulario/resumen de cliente predefinido** (parametrizado) que ve el comercial.
- **Seguidores**: se guardan y se categorizan (no se descartan), por si a futuro se activa algún flujo con ellos (ej. remarketing).

## Etapa 4 — Modelo de Dominio / Glosario

_(cerrada)_

### Entidades confirmadas

- **Organización**: empresa que usa el sistema (single-tenant por ahora).
- **Usuario**: con rol Administrador, Líder comercial o Usuario comercial.
- **Canal/Red Social**: WhatsApp, Instagram, etc., conectado a la Organización.
- **Contacto**: toda persona que escribe por primera vez. Nace siempre como candidato a **Seguidor**.
- **Seguidor** (tabla propia): Contacto clasificado como no-prospecto. Se guarda/categoriza (no se descarta) por si sirve a futuro.
- **Prospecto** (tabla propia, separada de Seguidor): Contacto clasificado como cliente potencial. Tiene estado propio: `parcial` (abandonó la encuesta) / `en_proceso` / termina convertido en **Cliente real** o en `sin_acuerdo`.
- **Oportunidad** (nueva, necesaria): cada idea/necesidad de desarrollo distinta que plantea un mismo Prospecto. Un Prospecto puede tener **varias Oportunidades en paralelo o en el tiempo** (ej. pide un desarrollo, luego otro). Cada Oportunidad agrupa sus propias Reuniones hasta llegar a un cierre (gana/pierde).
- **Conversación/Hilo**: unificado, vinculado al Contacto/Prospecto y a un Canal; tiene propietario (Líder o Usuario comercial) y la Líder queda siempre como supervisora aunque reasigne.
- **Mensaje**: texto/audio/imagen dentro de una Conversación.
- **Resumen de Cliente (formulario)**: recapitulación de lo preguntado por el agente, entregado al comercial como contexto. *(ver pregunta abajo sobre si es por Prospecto o por Oportunidad)*
- **Reunión**: pertenece a una Oportunidad (no directo al Prospecto). Fecha/hora, enlace Meet, estado (agendada automática / manual / realizada). Una Oportunidad puede tener **varias reuniones** hasta el cierre.
- **Resultado de Seguimiento**: cierre / sigue prospecto / sin acuerdo — resultado reportado tras cada Reunión, que actualiza el estado de la Oportunidad.
- **Rutina**: proceso automático recurrente (reintento 24h por abandono, aviso de falla de agendamiento, seguimiento diario post-reunión).
- **Parámetro de Configuración**: valores ajustables por el Administrador (ej. días máximos para concretar reunión).

**Resuelto:**

- **Resumen de Cliente**: datos generales (nombre, empresa, correo) viven en el **Prospecto** y se reutilizan. Cada **Oportunidad** es independiente y tiene su propio detalle/necesidad.
- Varias Oportunidades del mismo Prospecto comparten el **mismo hilo/conversación de WhatsApp**.
- **Oportunidad tiene estado propio** (activa/en_proceso vs cerrada). Las Oportunidades cerradas **dejan de ser visibles** en la vista de trabajo (se archivan, no se eliminan).
- **Prospecto → Cliente** es una transformación de ciclo de vida (mismo patrón que Contacto→Seguidor/Prospecto: pasa de una tabla/estado a otro), confirmado por el usuario ("los prospectos se transforman a cliente").

### Glosario fijado

| Término           | Definición                                                                                                                                     |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Seguidor           | Contacto clasificado como no-prospecto; se guarda igual, no se descarta.                                                                        |
| Prospecto          | Contacto clasificado como cliente potencial; estados: parcial / en_proceso / convertido a Cliente / sin_acuerdo.                                |
| Oportunidad        | Cada idea/necesidad de desarrollo distinta que plantea un mismo Prospecto; agrupa sus propias Reuniones; tiene estado activa/cerrada.           |
| Focalizar          | Reasignar la propiedad de una conversación de la Líder a un Usuario comercial (la Líder queda como supervisora).                             |
| Rutina             | Proceso automático recurrente disparado por tiempo o evento (reintento 24h, aviso de falla de agendamiento, seguimiento diario post-reunión). |
| Resumen de Cliente | Recapitulación de lo preguntado por el agente, entregado al comercial como contexto antes de la reunión.                                      |

## Etapa 5 — Reglas de Negocio

_(cerrada)_

### Reglas confirmadas

- **Campos obligatorios** para que el agente pueda avanzar a agendar reunión: correo, nombre del cliente, empresa/emprendimiento, necesidad. Sin estos datos completos, no se agenda.
- **Identificador principal del Prospecto/Cliente**: teléfono (número de WhatsApp) y/o correo — cualquiera de los dos sirve para correlacionar y reconocer a la misma persona si vuelve a escribir después de un tiempo.
- **Contacto recurrente**: si el Prospecto ya existe (por teléfono o correo) y vuelve a escribir sobre la misma idea → se retoma esa Oportunidad existente. Si trae una idea distinta → se crea una nueva Oportunidad para el mismo Prospecto.
- **Reasignación**: solo la Líder de área comercial puede asignar/reasignar un caso a un Usuario comercial (un Usuario comercial no puede reasignar a otro).
- **Límite de reintentos** en la rutina de abandono (24h): tras **3 intentos** sin respuesta del cliente, la Oportunidad/Prospecto pasa a estado **`no_atiende`** (se da por perdido el contacto).
- **Acceso al dashboard** (Fase 2): solo **Gerencia**. Dos vías de acceso:
  1. Dashboard web tradicional con login.
  2. **Agente conversacional de Gerencia** (nuevo, vía Telegram o WhatsApp): Gerencia pregunta en lenguaje natural (ej. "¿cuántos leads se consiguieron hoy?", "¿cuántas reuniones hizo comercial?") y el agente responde consultando la BD compartida — búsqueda natural, no reportes fijos.
- **Parámetro configurable**: tiempo máximo para concretar/agendar reunión (ej. 7–14 días), ajustable por el Administrador.

### Estados consolidados de Prospecto/Oportunidad

`parcial` → `en_proceso` → (`no_atiende` | `sin_acuerdo` | `cerrada_ganada` → Prospecto se transforma en **Cliente`)

**Resuelto:**

- **Correo y teléfono son únicos** en el sistema. Antes de crear un Prospecto nuevo, se valida si el número o el correo ya existen; si alguno coincide, es el mismo cliente.
- El estado `no_atiende` **se puede reactivar** si el cliente vuelve a escribir por su cuenta. Al reactivarse, se envía un mensaje predeterminado de reactivación ("hola, qué tal, te estábamos esperando") y se retoma el flujo desde ahí.
- El **Agente conversacional de Gerencia** puede dar detalle de un caso puntual, pero solo a nivel de **resumen** (no a fondo).
- **No hay límite** de Oportunidades activas simultáneas por Prospecto.

## Etapa 6 — Casos de Uso / Historias

_(cerrada)_

### UC1 — Clasificación inicial del contacto

**Como** Agente IA externo, **quiero** clasificar a todo contacto nuevo, **para** separar Seguidores de Prospectos.

- **Given** un Contacto escribe por primera vez a un Canal conectado,
  **When** el agente conversa con él,
  **Then** lo clasifica como Seguidor o Prospecto y, si es Seguidor, envía mensaje de cierre y lo guarda categorizado (no se descarta).

### UC2 — Encuesta de levantamiento de datos

**Como** Agente IA externo, **quiero** recolectar los datos obligatorios del Prospecto, **para** poder agendar la reunión.

- **Given** un Contacto fue clasificado como Prospecto,
  **When** el agente pregunta nombre, correo, empresa/emprendimiento y necesidad,
  **Then** no avanza a agendar hasta tener los 4 datos completos.
- **Given** el Prospecto abandona la encuesta a medias,
  **When** pasan 24h desde el último contacto,
  **Then** se dispara la rutina de reintento retomando la fase en que quedó; tras 3 reintentos sin respuesta pasa a `no_atiende`.

### UC3 — Identificación de contacto recurrente

**Como** sistema, **quiero** reconocer a un Prospecto que ya existe, **para** no duplicar su registro.

- **Given** llega un mensaje de un teléfono o correo ya registrado,
  **When** el sistema lo valida contra los registros existentes,
  **Then** lo asocia al Prospecto existente; si la idea es la misma, retoma la Oportunidad abierta; si es una idea nueva, crea una Oportunidad nueva bajo el mismo Prospecto.
- **Given** un Prospecto en estado `no_atiende` vuelve a escribir por su cuenta,
  **When** el sistema lo detecta,
  **Then** reactiva su estado y envía el mensaje predeterminado de reactivación ("hola, qué tal, te estábamos esperando") antes de continuar el flujo.

### UC4 — Agendamiento de reunión (con confirmación de la Líder)

**Como** Agente IA externo, **quiero** coordinar la reunión entre el cliente y la Líder, **para** agendarla sin que el cliente tenga que esperar un proceso manual largo.

- **Given** un Prospecto completó la encuesta,
  **When** el agente le pregunta "¿qué día y hora te sirve?",
  **Then** envía esa propuesta a la Líder junto con el Resumen del cliente.
- **Given** la Líder recibe la propuesta de fecha/hora,
  **When** ella revisa sus reuniones ya existentes (disponibilidad real),
  **Then** le indica al bot qué fecha confirmar (la propuesta del cliente u otra que ella defina).
- **Given** la Líder confirmó una fecha,
  **When** el bot se la comunica al cliente,
  **Then** agenda el evento en Calendar/Meet con esa fecha confirmada.
- **Given** no se llega a una fecha viable dentro del plazo configurado (cliente no responde, no hay acuerdo de fecha),
  **When** se cumple ese plazo,
  **Then** notifica al grupo de la Líder para manejar el agendamiento totalmente manual, y luego le solicita fecha/hora para registrar esa reunión manual en el sistema.

> Nota: esto reemplaza la idea inicial de "agendamiento 100% autónomo sin intervención humana" — la Líder **siempre confirma la fecha final** porque es quien conoce su disponibilidad real frente a otras reuniones ya agendadas. Lo autónomo es que el bot inicia, negocia y cierra el ciclo con el cliente sin que nadie tenga que abrir el sistema manualmente para escribirle.

### UC5 — Asignación y reasignación de casos

**Como** Líder de área comercial, **quiero** decidir quién atiende cada Prospecto, **para** repartir la carga del equipo.

- **Given** un Prospecto calificado llega a la Líder,
  **When** ella decide focalizarlo a un Usuario comercial,
  **Then** la propiedad de la conversación pasa a ese Usuario comercial y la Líder queda como supervisora del hilo.
- **Given** un Usuario comercial intenta reasignar un caso a otro,
  **When** lo intenta,
  **Then** el sistema lo bloquea — solo la Líder puede asignar/reasignar.

### UC6 — Seguimiento post-reunión

**Como** Agente IA interno de seguimiento, **quiero** preguntar al comercial qué pasó en la reunión, **para** mantener actualizado el estado de la Oportunidad.

- **Given** una reunión ya se realizó y está pendiente de calificar,
  **When** inicia el día siguiente,
  **Then** el agente pregunta al comercial el resultado (cierre / sigue prospecto / sin acuerdo) y actualiza el estado de la Oportunidad.
- **Given** no hay ninguna reunión pendiente de calificar,
  **When** inicia el día,
  **Then** la rutina no envía ningún mensaje.
- **Given** el comercial no responde,
  **When** pasa un día más,
  **Then** la rutina insiste diariamente hasta obtener respuesta.

### UC7 — Conversión a Cliente

**Como** sistema, **quiero** marcar cuándo un Prospecto se convierte en Cliente, **para** alimentar las estadísticas de cierre.

- **Given** una Oportunidad se marca como cerrada-ganada,
  **When** se registra el resultado,
  **Then** el Prospecto se transforma en Cliente (conserva su historial y datos generales).

### UC8 — Consulta en lenguaje natural de Gerencia

**Como** Gerencia, **quiero** preguntar en lenguaje natural por Telegram/WhatsApp, **para** obtener estadísticas sin entrar a un dashboard.

- **Given** Gerencia pregunta algo como "¿cuántos leads se consiguieron hoy?",
  **When** el agente interpreta la consulta contra la BD compartida,
  **Then** responde con el dato agregado; si la pregunta es sobre un caso puntual, responde con un resumen (no el detalle completo).

### UC9 — Dashboard web

**Como** Gerencia, **quiero** ver un dashboard con login, **para** revisar estadísticas de forma visual.

- **Given** Gerencia inicia sesión en el dashboard,
  **When** accede,
  **Then** ve chats respondidos, prospectos ingresados, casos atendidos por comercial y conversiones a Cliente.

### UC10 — Administración del sistema

**Como** Administrador, **quiero** gestionar usuarios, canales y parámetros, **para** mantener operando el sistema.

- **Given** el Administrador necesita dar de alta un usuario o conectar un nuevo canal,
  **When** accede a la configuración,
  **Then** puede crear usuarios con rol (Líder/Usuario comercial), conectar redes sociales y ajustar parámetros (ej. plazo máximo de agendamiento).

**Resuelto:**

- **UC2 (datos incompletos)**: la Líder puede tomar el caso igual de forma manual; al hacerlo cambia el estado a **`atencion_manual`**, y el bot deja de referenciar/actuar sobre ese caso — todo pasa a manejarse manualmente desde ahí.
- **UC4 (agendamiento)**: ver nota arriba — el bot pregunta día/hora al cliente, pero la **Líder siempre confirma la fecha final** según su disponibilidad real frente a otras reuniones ya agendadas.
- **Gerencia puede tener más de una persona** con ese rol (no es un rol de usuario único como la Líder).

### UC11 — Listado de casos asignados (vista tipo CRM)

**Como** Líder o Usuario comercial, **quiero** ver mi listado completo de clientes asignados, **para** saber qué atender y qué está en manos del bot.

- **Given** un usuario (Líder o Usuario comercial) entra a su listado,
  **When** el sistema lo muestra,
  **Then** lo divide en dos vistas: **Bot** (casos sin contacto humano aún, o en estados como `no_atiende`/`parcial`/`en_proceso` donde el bot sigue respondiendo) y **Manual** (casos donde la conversación ya pasó a esa persona, incluidos los `atencion_manual`).
- **Given** un caso pasa de ser manejado por el bot a ser focalizado/tomado por un humano,
  **When** ocurre esa transición,
  **Then** el caso se mueve de la vista "Bot" a la vista "Manual" de quien lo recibió.

### Cierre de Etapa 6

Sin más casos de uso pendientes — etapa cerrada.

## Etapa 7 — Requerimientos No Funcionales

_(pendiente)_
