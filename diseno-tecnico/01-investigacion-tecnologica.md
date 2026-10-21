# 1. Investigación Tecnológica — Opciones por Módulo

> Investigación con búsqueda web (octubre 2026), orientada a los módulos M1–M6 definidos
> en `requerimientos/08-modulos-y-arquitectura-comercial.md`. Presenta opciones y una
> recomendación justificada por área — la decisión final es del usuario, módulo por
> módulo. Fuentes al final de cada sección/del documento.

## 1. Canal WhatsApp Business

| Opción | Costo aprox. (2026) | Pros | Contras |
|---|---|---|---|
| **Meta Cloud API directa** | Marketing $0.025/msj, Utility/Auth $0.004/msj (tarifas referencia US; Colombia menor). Desde oct-2026 ya no hay ventana 100% gratis — 1.000 mensajes de servicio gratis/mes/número, luego se cobra. | Sin markup de intermediario, control total programático | Alta/verificación del número vía Meta Business Manager puede ser tediosa sin soporte de un BSP |
| **360dialog (BSP)** | ~€49/número/mes + tarifa de Meta sin markup adicional | Transparente, buena para compliance, self-serve | Sigue siendo tan "manual" como la API directa para lógica custom |
| **Twilio (BSP)** | ~$0.005/mensaje + tarifa Meta | SDKs maduros, útil si luego se suma SMS/voz | Markup más alto; no aporta valor extra en un producto 100% WhatsApp |
| **Gupshup (BSP)** | ~$0.001/mensaje (self-serve) | Más barato a bajo volumen | Enfoque fuerte en mercados asiáticos, menos relevante para Colombia |

**Recomendación:** Meta Cloud API directa, provisionada vía **360dialog** solo para
simplificar el alta/verificación del número, sin perder control programático ni pagar
markup significativo.

## 2. Instagram — evento "seguir" (M3) — ⚠️ riesgo crítico de producto

**Hallazgo:** la Graph API de Meta **no tiene un webhook oficial de "nuevo seguidor"**.
Los webhooks de Instagram solo cubren: comentarios, menciones, insights de historias,
mensajes y `messaging_postbacks` (botones dentro de un mensaje ya existente). No existe
evento "follow".

Lo que se ve en el ejemplo (DM automático al seguir, con botones) corresponde a
**ManyChat "Follow to DM"** (lanzado oct-2025) — la única vía aprobada por Meta para
auto-mensaje al seguir. Limitaciones duras:

- Beta, requiere cuentas con ~1.000+ seguidores y buen engagement.
- Meta permite solo **1 mensaje de este tipo por usuario por semana**.
- Se dispara **una sola vez** por seguidor (si deja de seguir y vuelve a seguir, no se
  repite).

Alternativa sin ManyChat: polling periódico de la lista de seguidores + diff contra la
lista anterior — no es tiempo real, consume rate-limit, frágil a escala. No se
recomienda como vía principal.

**Recomendación:** no prometer "activado al seguir" como garantizado en V1. Dos caminos
— ahora formalizados como los niveles **Normal/Premium de M3** (capa 8 de
requerimientos), no solo como fallback técnico:

1. **Premium — ManyChat Follow-to-DM** como capa de disparo, con backend propio
   recibiendo el evento vía su webhook/API — sujeto a elegibilidad de cada cuenta
   cliente (Meta decide, no hay forma de pagar para saltarse el requisito de ~1.000+
   seguidores y engagement). **Costo: $0** — gratis en todos los planes de ManyChat,
   incluido el plan Free; solo se paga si el cliente además usa ManyChat para otras
   automatizaciones.
2. **Normal — Instant Reply nativo** (si la cuenta no califica para Premium, o el
   cliente compra directamente el nivel Normal): función nativa de Meta Business Suite,
   100% oficial, sin restricción de elegibilidad y **también $0**. Limitación real: es
   un único mensaje de texto (máx. 500 caracteres, solo variable de nombre) — **no
   soporta un menú ramificado con botones** como el nivel Premium. En este nivel la
   lógica de ramas
   (empleo/producto/info) tiene que resolverla el propio M2 conversacionalmente, no
   Meta de forma nativa.

Esto es una limitación de **elegibilidad y de funcionalidad de la plataforma Meta**, no
un costo monetario ni una limitación técnica propia — hay que comunicarlo con claridad
al vender M3.

## 3. Bandeja unificada (M1) — revisado tras validación de Chatwoot

| Opción | Costo | Fit con el caso de uso |
|---|---|---|
| **Chatwoot (self-hosted)** | Gratis OSS (Rails+Postgres+Redis, Docker). El paywall de jul-2026 aplica solo a **Chatwoot Cloud** (su SaaS); self-hosted sigue con API/webhooks completos bajo MIT. | Soporta WhatsApp/Instagram/FB/Telegram/SMS/email + Agent Bots API. **Pero**: es un monolito Rails que no se puede "tomar en partes" (se consume completo vía su API, no por extracción de código); trae **su propia BD separada** (Postgres+pgvector, + Redis/Sidekiq) — rompe el principio de "una sola BD compartida" de la capa 8; libera versión ~mensual, con rutina de upgrade (imagen + migraciones) que se **multiplica por cada instancia de cliente** en el modelo de infraestructura duplicada. |
| **CRM/inbox propio sobre Supabase** | Solo tiempo de desarrollo (ya se usa Supabase como BD compartida) | Conversación/Mensaje viven en la misma BD que el resto de módulos — sin sincronizar dos bases. La ingesta de webhooks por canal hay que construirla de todas formas para que M2 reciba mensajes, así que el costo incremental real de M1 es solo la UI (lista de conversaciones Bot/Manual + hilo + focalizar), alimentada en vivo con Supabase Realtime, sin servicio ni BD adicional, sin calendario de upgrades de terceros. |

**Recomendación (revisada):** construir M1 a medida sobre Supabase, no usar Chatwoot.
A este volumen (~100 prospectos/mes) es abordable para un solo dev, y evita sumar un
segundo servicio pesado (Rails+Sidekiq+Redis), una segunda BD, y una rutina de
actualización mensual replicada por cada cliente.

**Nota de arquitectura:** M1 y M5 (dashboard) viven en la misma aplicación Next.js, como
**secciones separadas** (no una vista fusionada): "Dashboard" (M5, estadístico, para
Gerencia), "Módulo comercial" (M1, bandeja de conversaciones, para Líder/Usuario
comercial) y "Panel Administrativo" (variables y Plantilla de Compañía, para
Administrador) — ver capa 8 de requerimientos. Mismo login de Supabase Auth, mismos
permisos por rol, un solo frontend y un solo backend por cliente.

## 4. Orquestación de agentes (M2, M3, M4, M6)

| Opción | Fortaleza | Debilidad |
|---|---|---|
| **n8n** | Visual, buena documentación/curva de aprendizaje, fuerte en conectar sistemas + triggers + scheduling, nodos MCP (2026) | Estado persistente entre ejecuciones más limitado (no memoria de primera clase) |
| **LangGraph** | Memoria/estado de primera clase con checkpoints — ideal para un flujo que "pausa días y retoma" como M6 | Requiere código, más esfuerzo de build inicial |

**Recomendación:** empezar con **n8n** (menor fricción para un solo dev, cubre triggers
de WhatsApp/Telegram, cron, lectura/escritura a la BD) y reservar LangGraph si el estado
multi-día de M6 se vuelve difícil de manejar dentro de n8n.

**✅ Confirmado:** n8n para los 4 agentes (M2, M3, M4, M6). El estado que "pausa días"
(ej. M6 esperando la reunión) no depende de la memoria del motor — ya vive en la BD
compartida (`Prospecto`/`Oportunidad.estado`), consistente con el patrón de la capa 8
(los módulos reaccionan a estado en BD, no a memoria propia). Esto hace innecesario
LangGraph para este caso de uso.

## 5. "OpenClaw" (openclaw.ai) — ⚠️ no recomendado

Es un **framework de agente autónomo local y de código abierto** (lanzado nov-2025,
crecimiento viral). Se conecta a WhatsApp/Telegram/Discord y ejecuta comandos de shell,
archivos y tareas multi-paso **sin supervisión por defecto**.

**Riesgos encontrados:**

- Sin allowlist de comandos por defecto — trata `rm -rf` igual que `ls`.
- Filtraciones reportadas de credenciales/API keys en texto plano.
- **CVE-2026-25253**: si el gateway WebSocket queda expuesto a internet, visitar un
  sitio malicioso basta para que un atacante tome control total del agente.
- Autohospedarlo exige hardening serio (Docker aislado, firewall, monitoreo).

**Recomendación: descartar OpenClaw** para M4/M6. Lo necesario (hablar por Telegram,
preguntar algo, escribir en la BD) se logra igual con la **API nativa de Telegram Bot**
+ el motor de orquestación de la sección 4, sin la superficie de ataque de ejecución de
shell/OS completa — crítico porque este producto se despliega repetido en
infraestructura de distintos clientes; una brecha en OpenClaw sería una brecha en el
servidor de cada cliente.

**Nota de diseño — el reemplazo sigue siendo un agente autónomo, pero restringido por
herramientas, no solo por texto.** El patrón recomendado (n8n + LLM con
function-calling + Telegram) también toma decisiones guiado por un system prompt
(instrucciones/restricciones en texto) — la diferencia con OpenClaw no es "autonomía
sí/no", es **dónde se aplica la restricción**: en OpenClaw la restricción vive solo en
el texto del prompt mientras la *capacidad* de ejecutar cualquier comando de shell sigue
expuesta (vulnerable a prompt injection); en el patrón recomendado, al agente solo se le
exponen funciones acotadas (`enviar_mensaje_telegram()`, `marcar_resultado_reunion()`,
`escribir_en_bd()`) — no existe una función `ejecutar_shell()` que un mensaje
malicioso pueda invocar. Esto es especialmente relevante para **M2**, que procesa texto/
audio/imagen de clientes (input no confiable): su set de funciones expuestas debe
diseñarse lo más angosto posible desde el inicio.

## 6. Proveedor de LLM

| Proveedor | Precio (por M tokens, in/out) | Audio nativo | Fit |
|---|---|---|---|
| **Claude (Sonnet/Haiku)** | Sonnet $3/$15, Haiku $0.80/$4 | ❌ No soporta audio en la API | Excelente en español y function-calling; bloquea el requisito de M2 de procesar audio sin un paso extra de transcripción |
| **GPT-4o** | $2.50/$10 | ✅ Nativo (texto, audio, imagen) | Cubre M2 en un solo proveedor |
| **Gemini 3.8 Flash** | $0.75/$3.75 | ✅ Nativo | Más barato, también multimodal |

**Recomendación:** para M2/M3 (deben procesar audio/imagen) usar **GPT-4o o Gemini 3.8
Flash**. Para M4 (solo texto) **Claude Haiku o Gemini Flash** son más baratos y sobran
en capacidad. Al volumen declarado (~100 casos/mes, 12–25 mensajes c/u ≈ 1.500–2.500
turnos/mes) el costo de LLM es marginal sin importar cuál se elija — prioriza capacidad
(audio) sobre precio.

**✅ Confirmado — arquitectura final de LLM:** no se reparten turnos de conversación
entre proveedores (evita inconsistencia de tono). En su lugar, dos roles separados:

- **Claude = único motor conversacional**, para M2, M3 y M4 — siempre el mismo "tono"
  del agente, sin importar el tipo de mensaje original del cliente.
- **Gemini Flash = capa de normalización de medios** (no conversacional): cuando llega
  un audio o una imagen, se manda primero a Gemini para convertirlo a texto plano
  (transcripción de audio; descripción/extracción de contenido de imagen). Ese texto es
  lo único que recibe Claude — nunca procesa audio/imagen directamente.
- Esto es coherente con la regla de negocio ya fijada (capa 3): el contenido de
  audio/imagen **no es interpretativo para decisiones, solo alimenta el Resumen de
  Cliente como referencia** — por eso basta con normalizarlo a texto antes de que Claude
  lo vea, sin perder nada relevante para el flujo.
- Ventaja adicional: la integración de Claude queda simple (siempre texto-a-texto), y
  Gemini queda como una única pieza intercambiable de "traducir medios a texto",
  reutilizable para audio e imagen por igual.

## 7. Base de datos compartida

| Opción | Fit con "módulos reaccionan a estado en BD" |
|---|---|
| **PostgreSQL + LISTEN/NOTIFY puro** | Nativo, sin servicios extra, pero cada módulo debe implementar su propio listener |
| **Supabase self-hosted** | Agrega **Realtime (Postgres Changes)** vía websockets — los módulos se suscriben a cambios de tabla sin código de bajo nivel; incluye **Auth** (sirve para login de M5) y **Storage** (sirve para audio/imagen de clientes). Todo en un docker-compose, fácil de plantillar por cliente. |

**Recomendación:** Supabase self-hosted — resuelve BD + tiempo real + auth + storage en
una sola pieza, y es Docker-componible para duplicar por cliente (capa 7 de
requerimientos). Nota técnica: LISTEN/NOTIFY exige modo sesión del pooler (Supavisor),
no modo transacción — definirlo en la plantilla de despliegue desde el inicio.

## 8. Calendario/reuniones (M6)

Confirmado: la API de Google Calendar crea el evento con
`conferenceData.createRequest`, que genera el enlace de Meet automáticamente. Dos
caminos de autenticación:

- **OAuth2 por organización** (la Líder autoriza una sola vez, se guarda el refresh
  token): funciona con cualquier cuenta de Google, Workspace o no.
- **Service Account + Domain-Wide Delegation**: solo funciona si el cliente usa Google
  Workspace con permisos a nivel de dominio.

**Recomendación:** OAuth2 por organización — más compatible, no todos los clientes
tendrán Workspace.

## 9. Dashboard (M5)

| Opción | Fit |
|---|---|
| **Metabase self-hosted** | Gratis OSS, cero frontend, rápido de montar — pensado para BI interno, no para un producto de cara al cliente con login/branding/feature-gating propios |
| **Next.js + librería de gráficos a medida** | Más tiempo de desarrollo, pero control total de marca e integración directa con el sistema de auth y de licenciamiento por módulo |

**Recomendación:** M5 es un módulo que se **vende**, no una herramienta de BI interna —
construirlo a medida (Next.js) integrado al Auth y al feature-gating (capa 7/8 de
requerimientos). Metabase puede servir como v0 rápido si urge mostrar algo cuanto antes.

## 10. Rutinas/cron

Con n8n y Supabase ya en el stack: usar los **Schedule Trigger nodes de n8n** para las 3
rutinas (reintento 24h, seguimiento diario, aviso de fallo de agendamiento) — evita
repartir la lógica de cron entre `pg_cron` y n8n.

---

## Stack definitivo — ✅ confirmado con el usuario

| Pieza | Elección |
|---|---|
| WhatsApp | Meta Cloud API vía 360dialog |
| Instagram M3 | Premium: ManyChat Follow-to-DM, $0 (sujeto a elegibilidad) · Normal: Instant Reply nativo, $0 |
| Módulo comercial M1 | CRM/inbox propio sobre Supabase — sección separada en la misma app que M5, no Chatwoot |
| Orquestación (M2, M3, M4, M6) | n8n (self-hosted) |
| Motor conversacional (M2, M3, M4) | Claude (único, para consistencia de tono) |
| Normalización de medios (audio/imagen → texto) | Gemini Flash, capa previa a Claude, no conversacional |
| M6 seguimiento interno | Telegram Bot API + n8n (no OpenClaw) |
| BD compartida | Supabase self-hosted (Postgres + Realtime + Auth + Storage), un docker-compose por cliente |
| Calendario | Google Calendar API, OAuth2 por organización |
| Dashboard M5 | Next.js a medida + librería de gráficos, sobre Supabase Auth — sección separada del Módulo comercial |
| Rutinas/cron | Schedule Trigger de n8n |

## Riesgos y validaciones pendientes

1. **M3 por "seguir" no tiene webhook oficial** — depende de ManyChat Follow-to-DM
   (beta, ~1.000+ seguidores, 1 msj/semana/usuario, no se repite en re-follow). Validar
   elegibilidad real por cliente antes de prometerlo; tener el plan B listo.
2. **WhatsApp ya no es gratis tras oct-2026** más allá de 1.000 mensajes de
   servicio/mes/número — modelar costo real a mediano plazo.
3. **Claude no soporta audio nativo** — si se usa para algo que reciba audio, se
   necesita un paso de transcripción aparte.
4. **LISTEN/NOTIFY en Supabase self-hosted exige modo sesión del pooler**, no modo
   transacción — definir esto en la plantilla de despliegue por cliente desde el inicio.
5. **OpenClaw tiene un CVE de exposición total** si el gateway queda público —
   descartado para este producto.
6. **Habeas Data (Colombia)**: confirmar que la región de hosting (Supabase/Storage) y
   el proveedor de LLM elegido sean aceptables para datos personales de clientes
   colombianos — pendiente de asesoría legal (ya marcado en requerimientos capa 7).
7. **Tarifas de WhatsApp citadas son de referencia en USD** (mayormente EE.UU.) —
   validar tarifas específicas para Colombia con Meta/360dialog antes de fijar precios
   de venta del producto.

## Fuentes consultadas (búsqueda web, octubre 2026)

Wati, Blueticks, Flowcall, Peppercloud (pricing WhatsApp); d7networks, getkanal, nomadx
(comparativa BSP); Meta for Developers — Webhooks Reference Instagram, foros de
community.make.com y GitHub (confirmación ausencia de webhook de follower); ManyChat
Help Center, Thrive blog (Follow to DM); DigitalOcean, KDnuggets, Contabo, Firecrawl,
Cisco Blogs, arXiv (OpenClaw); Chatwoot.com, OSSAlt, SelfHostIndex (Chatwoot); Peliqan,
ZenML, DigitalApplied (n8n vs LangGraph); IntuitionLabs, Vortenza (pricing LLM);
parsejet.com, MLQ.ai (Claude audio); Supabase docs/blog, sequinstream
(Realtime/LISTEN-NOTIFY); Medium (iceapple-tech-talks), dev.to (Calendar+Meet API);
Sliplane, Mammoth, valiotti (Metabase pricing); Neon docs, freeCodeCamp,
n8nautomation.cloud (pg_cron vs n8n).
