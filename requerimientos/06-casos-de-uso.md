# 6. Casos de Uso / Historias con Criterios de Aceptación

## UC1 — Clasificación inicial del contacto

**Como** Agente externo, **quiero** clasificar a todo contacto nuevo, **para** separar
Seguidores de Prospectos.

- **Given** un Contacto escribe por primera vez a un Canal conectado,
  **When** el agente conversa con él,
  **Then** lo clasifica como Seguidor o Prospecto y, si es Seguidor, envía un mensaje de
  cierre y lo guarda categorizado (no se descarta).

## UC2 — Encuesta de levantamiento de datos

**Como** Agente externo, **quiero** recolectar los datos obligatorios del Prospecto,
**para** poder agendar la reunión.

- **Given** un Contacto fue clasificado como Prospecto,
  **When** el agente pregunta nombre, correo, empresa/emprendimiento y necesidad,
  **Then** no avanza a agendar hasta tener los 4 datos completos.
- **Given** el Prospecto abandona la encuesta a medias,
  **When** pasan 24h desde el último contacto,
  **Then** se dispara la rutina de reintento retomando la fase en que quedó; tras 3
  reintentos sin respuesta pasa a `no_atiende`.
- **Given** los datos están incompletos pero la Líder decide tomar el caso igual,
  **When** ella lo marca como manual,
  **Then** el caso pasa a `atencion_manual` y el bot deja de actuar sobre él.

## UC3 — Identificación de contacto recurrente

**Como** sistema, **quiero** reconocer a un Prospecto que ya existe, **para** no
duplicar su registro.

- **Given** llega un mensaje de un teléfono o correo ya registrado,
  **When** el sistema lo valida contra los registros existentes,
  **Then** lo asocia al Prospecto existente; si la idea es la misma, retoma la
  Oportunidad abierta; si es una idea nueva, crea una Oportunidad nueva bajo el mismo
  Prospecto.
- **Given** un Prospecto en estado `no_atiende` vuelve a escribir por su cuenta,
  **When** el sistema lo detecta,
  **Then** reactiva su estado y envía el mensaje predeterminado de reactivación ("hola,
  qué tal, te estábamos esperando") antes de continuar el flujo.

## UC4 — Agendamiento de reunión (con confirmación de la Líder)

**Como** Agente externo, **quiero** coordinar la reunión entre el cliente y la Líder,
**para** agendarla sin que el cliente tenga que esperar un proceso manual largo.

- **Given** un Prospecto completó la encuesta,
  **When** el agente le pregunta "¿qué día y hora te sirve?",
  **Then** envía esa propuesta a la Líder junto con el Resumen del cliente.
- **Given** la Líder recibe la propuesta de fecha/hora,
  **When** revisa sus reuniones ya existentes (disponibilidad real),
  **Then** le indica al agente qué fecha confirmar (la propuesta del cliente u otra que
  ella defina).
- **Given** la Líder confirmó una fecha,
  **When** el agente se la comunica al cliente,
  **Then** agenda el evento en Calendar/Meet con esa fecha confirmada.
- **Given** no se llega a una fecha viable dentro del plazo configurado,
  **When** se cumple ese plazo,
  **Then** notifica al grupo de la Líder para manejar el agendamiento totalmente
  manual, y luego le solicita fecha/hora para registrar esa reunión en el sistema.

> Nota de diseño: el agendamiento no es 100% autónomo sin intervención humana — la Líder
> siempre confirma la fecha final porque es quien conoce su disponibilidad real frente a
> otras reuniones ya agendadas. Lo autónomo es que el agente inicia, negocia y cierra el
> ciclo con el cliente sin que nadie tenga que abrir el sistema manualmente para
> escribirle.

## UC5 — Asignación y reasignación de casos

**Como** Líder de área comercial, **quiero** decidir quién atiende cada Prospecto,
**para** repartir la carga del equipo.

- **Given** un Prospecto calificado llega a la Líder,
  **When** ella decide focalizarlo a un Usuario comercial,
  **Then** la propiedad de la conversación pasa a ese Usuario comercial y la Líder
  queda como supervisora del hilo.
- **Given** un Usuario comercial intenta reasignar un caso a otro,
  **When** lo intenta,
  **Then** el sistema lo bloquea — solo la Líder puede asignar/reasignar.

## UC6 — Seguimiento post-reunión

**Como** Agente interno de seguimiento, **quiero** preguntar al comercial qué pasó en la
reunión, **para** mantener actualizado el estado de la Oportunidad.

- **Given** una reunión ya se realizó y está pendiente de calificar,
  **When** inicia el día siguiente,
  **Then** el agente pregunta al comercial el resultado (cierre / sigue prospecto / sin
  acuerdo) y actualiza el estado de la Oportunidad.
- **Given** no hay ninguna reunión pendiente de calificar,
  **When** inicia el día,
  **Then** la rutina no envía ningún mensaje.
- **Given** el comercial no responde,
  **When** pasa un día más,
  **Then** la rutina insiste diariamente hasta obtener respuesta.

## UC7 — Conversión a Cliente

**Como** sistema, **quiero** marcar cuándo un Prospecto se convierte en Cliente, **para**
alimentar las estadísticas de cierre.

- **Given** una Oportunidad se marca como cerrada-ganada,
  **When** se registra el resultado,
  **Then** el Prospecto se transforma en Cliente (conserva su historial y datos
  generales).

## UC8 — Consulta en lenguaje natural de Gerencia

**Como** Gerencia, **quiero** preguntar en lenguaje natural por Telegram/WhatsApp,
**para** obtener estadísticas sin entrar a un dashboard.

- **Given** Gerencia pregunta algo como "¿cuántos leads se consiguieron hoy?",
  **When** el agente interpreta la consulta contra la base de datos compartida,
  **Then** responde con el dato agregado; si la pregunta es sobre un caso puntual,
  responde con un resumen (no el detalle completo).

## UC9 — Dashboard web

**Como** Gerencia, **quiero** ver un dashboard con login, **para** revisar estadísticas
de forma visual.

- **Given** Gerencia inicia sesión en el dashboard,
  **When** accede,
  **Then** ve chats respondidos, prospectos ingresados, casos atendidos por comercial y
  conversiones a Cliente.

## UC10 — Administración del sistema

**Como** Administrador, **quiero** gestionar usuarios, canales y parámetros, **para**
mantener operando el sistema.

- **Given** el Administrador necesita dar de alta un usuario o conectar un nuevo canal,
  **When** accede a la configuración,
  **Then** puede crear usuarios con rol (Líder/Usuario comercial), conectar redes
  sociales y ajustar parámetros (ej. plazo máximo de agendamiento).

## UC11 — Listado de casos asignados (vista tipo CRM)

**Como** Líder o Usuario comercial, **quiero** ver mi listado completo de clientes
asignados, **para** saber qué atender y qué está en manos del bot.

- **Given** un usuario (Líder o Usuario comercial) entra a su listado,
  **When** el sistema lo muestra,
  **Then** lo divide en dos vistas: **Bot** (casos sin contacto humano aún, o en
  estados como `no_atiende`/`parcial`/`en_proceso` donde el bot sigue respondiendo) y
  **Manual** (casos donde la conversación ya pasó a esa persona, incluidos los
  `atencion_manual`).
- **Given** un caso pasa de ser manejado por el bot a ser focalizado/tomado por un
  humano,
  **When** ocurre esa transición,
  **Then** el caso se mueve de la vista "Bot" a la vista "Manual" de quien lo recibió.

## UC12 — Bienvenida y categorización al seguir (M3)

**Como** Agente de bienvenida (M3), **quiero** enganchar a quien sigue una red social de
la organización, **para** categorizar su interés y derivar a comercial cuando aplique.

- **Given** una persona sigue una red social conectada,
  **When** M3 detecta el evento "seguir",
  **Then** envía un mensaje de bienvenida con un menú de opciones (productos/servicios
  configurados en la Plantilla de Compañía).
- **Given** la persona elige "quiero trabajar con ustedes" (empleo) o "conocer más",
  **When** M3 procesa la respuesta,
  **Then** envía el mensaje/enlace correspondiente (oportunidades de empleo o página
  oficial) y la registra como Seguidor con su Categoría de Interés — no se convierte en
  Prospecto.
- **Given** la persona elige la opción de interés comercial/producto,
  **When** M3 le entrega el enlace a WhatsApp y ella escribe ahí,
  **Then** M2 recibe el mensaje y aplica su regla de identificación existente (capa 5):
  Prospecto nuevo si el teléfono no existía, o retoma la Oportunidad si ya existía.
- **Given** se activa M3 por primera vez en una organización con seguidores previos,
  **When** se ejecuta la campaña de alcance histórico,
  **Then** el mismo mensaje de bienvenida se envía de forma gradual/escalonada, nunca de
  forma masiva simultánea.

## UC13 — Configuración de la Plantilla de Compañía (Panel de Administración)

**Como** Administrador, **quiero** definir la plantilla de mi compañía, **para** que M2
y M3 usen contenido propio en vez de texto fijo.

- **Given** el Administrador entra al Panel de Administración,
  **When** edita mensajes de bienvenida, preguntas de encuesta u opciones de menú,
  **Then** esos cambios alimentan directamente a M2 y M3 sin requerir cambios en el
  sistema.
- **Given** la organización no ha contratado alguno de los módulos (ej. M3),
  **When** el Administrador entra al Panel,
  **Then** ve la misma estructura base completa, pero con las funciones de ese módulo
  deshabilitadas según su plan.

## UC14 — Difusión segmentada por categoría de interés

**Como** Líder o Administrador, **quiero** enviar un mensaje a los Seguidores de una
Categoría de Interés específica, **para** reactivarlos cuando sea relevante (ej. una
vacante nueva).

- **Given** existen Seguidores categorizados con interés `empleo`,
  **When** se abre una vacante en un área específica,
  **Then** se puede enviar un mensaje de difusión solo a ese segmento, sin afectar a los
  demás Seguidores.
