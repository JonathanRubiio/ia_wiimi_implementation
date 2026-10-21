# 3. Mapeo de Triggers por Módulo y Flujo de `resumen_cierre`

## Las 3 clases de disparador (ningún módulo llama a otro directamente — capa 8)

| Clase | Qué es | Quién lo usa |
|---|---|---|
| **A. Webhook externo** | Evento que llega de una plataforma (Meta, Telegram) a un nodo Webhook de n8n. Es la puerta de entrada — aquí es donde un módulo **escribe** estado por primera vez. | M2, M3 (mensajes/eventos de clientes), M4 (pregunta de Gerencia), acciones de UI de M1 (la Líder reasigna) |
| **B. Realtime interno (Supabase Postgres Changes)** | Un módulo se suscribe a `INSERT`/`UPDATE` de una tabla propia del sistema y reacciona cuando otro módulo cambió ese estado — sin llamarlo directamente. | M6 (reacciona a M2), M1 y M5 (actualizan su UI en vivo), generación de `resumen_cierre` |
| **C. Cron interno (`rutina_ejecucion`)** | n8n consulta periódicamente filas vencidas (`proximo_disparo_at <= now()`), no depende de ningún evento. | Las 3 rutinas ya definidas: reintento 24h, seguimiento diario post-reunión, aviso de fallo de agendamiento |

## Mapeo módulo por módulo

| Módulo | Disparador | Condición | Acción |
|---|---|---|---|
| **M2** | A — webhook WhatsApp/Instagram/Facebook | mensaje entrante de un Contacto | Clasifica, escribe `contacto`/`seguidor`/`prospecto`, acumula respuestas de la encuesta en `prospecto` |
| **M2 → cierra la encuesta** | — | al completar los 4 datos obligatorios | `UPDATE prospecto SET estado = 'en_proceso'` + `INSERT INTO oportunidad` (con la necesidad) |
| **M6** | B — Realtime en `oportunidad` | `INSERT` (nueva Oportunidad) | Arranca la negociación de fecha con el cliente |
| **M6** | B — Realtime en `reunion` | `UPDATE` → `estado = 'confirmada'` (la Líder ya indicó la fecha) | Crea el evento en Google Calendar/Meet, `UPDATE reunion SET enlace_meet, estado = 'realizada'` tras la reunión |
| **M6** | C — cron en `rutina_ejecucion` (`tipo = 'aviso_fallo_agendamiento'`) | vencido el plazo configurado sin fecha confirmada | Notifica al grupo de la Líder; pide fecha manual |
| **M6** | C — cron en `rutina_ejecucion` (`tipo = 'seguimiento_post_reunion'`) | reunión `realizada` sin `resultado_seguimiento` | Pregunta al comercial por Telegram qué pasó |
| **M3** | A — webhook ManyChat (Premium) o Instant Reply (Normal) | evento "seguir" o primer mensaje | Menú de bienvenida; si rama "producto", redirige a WhatsApp (entra como webhook de M2) |
| **M4** | A — webhook Telegram/WhatsApp de Gerencia | pregunta en lenguaje natural | Consulta `vista_metricas_dashboard` / `resumen_cierre` / `historial_evento` (solo lectura) |
| **M1 (bandeja)** | B — Realtime en `mensaje` | `INSERT` | Actualiza la lista de conversaciones en vivo |
| **M1 (bandeja)** | B — Realtime en `conversacion` | `UPDATE` → cambia `vista` o `propietario_usuario_id` | Mueve la tarjeta entre las vistas Bot/Manual (UC11) |
| **M5 (dashboard)** | B — Realtime en `contacto`/`prospecto`/`oportunidad`/`resumen_cierre` | cualquier `INSERT`/`UPDATE` relevante | Vuelve a ejecutar (debounced) las vistas de métricas — Realtime no transmite sobre vistas SQL directamente, solo sobre tablas base |
| **Generador de `resumen_cierre`** | B — Realtime en `resultado_seguimiento` | `INSERT` con `resultado IN ('cierre','sin_acuerdo')` | Ver flujo completo abajo |
| **C — todas las rutinas** | cron de n8n | consulta `rutina_ejecucion` cada N minutos | Dispara la rutina vencida, incrementa `intentos`, marca `completada` cuando corresponde |

## Flujo de generación de `resumen_cierre`

Disparado cuando llega un `resultado_seguimiento` que **cierra** la Oportunidad (no
cuando es `sigue_prospecto`, que la deja abierta):

1. **Trigger (Realtime B)**: `INSERT` en `resultado_seguimiento` donde
   `resultado IN ('cierre', 'sin_acuerdo')`.
2. **Actualizar estado**: n8n hace
   `UPDATE oportunidad SET estado = 'cerrada_ganada'|'cerrada_perdida', cerrada_at = now()`
   según corresponda.
3. **Promoción a Cliente** (solo si `cierre`): si es la primera Oportunidad ganada de
   ese Prospecto, `UPDATE prospecto SET estado = 'cliente'`.
4. **Recopilar contexto**: n8n junta en un solo payload:
   - todas las filas de `historial_evento` de esa `oportunidad_id`,
   - los `mensaje` de la `conversacion` del Contacto (acotados al rango de fechas de
     esa Oportunidad),
   - el/los `resultado_seguimiento` y comentarios del comercial,
   - los datos de la(s) `reunion` asociadas.
5. **Llamada a Claude** (motor conversacional único, capa 1 de diseño técnico) con un
   prompt de resumen — no es una conversación, es una sola llamada de "resumir y
   extraer factores":
   > "Con este historial de un proceso comercial, responde en JSON:
   > `{ "resumen_narrativo": "...", "factores_clave": ["...", "..."] }`.
   > El resumen debe explicar en 3–5 líneas qué pasó de principio a fin. Los factores
   > clave son las razones concretas (precio, tiempo de respuesta, falta de
   > seguimiento, ajuste de producto, etc.) que explican el resultado."
6. **Guardar**: `INSERT INTO resumen_cierre (oportunidad_id, resultado, factores_clave, resumen_narrativo)`.
7. **Registrar el hito**: `INSERT INTO historial_evento (..., tipo = 'oportunidad_cerrada', ...)`.

Este resumen queda disponible de inmediato para: el Dashboard de Gerencia
(`vista_factores_cierre`), el Agente de Gerencia M4 (consulta de casos puntuales), y
cualquier análisis futuro de por qué se gana o se pierde (mencionado como necesidad
explícita por el usuario).
