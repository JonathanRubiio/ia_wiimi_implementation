# 2. Actores y Roles

El sistema es **single-tenant por diseño**: cada organización cliente del producto opera
sobre su propia instancia independiente (ver capa 7). Los roles descritos aquí existen
dentro de una misma organización.

Los agentes de IA están organizados en los **módulos comerciales independientes**
descritos en la capa 8 (cada uno vendible por separado, en sub-paquete o completo).

## Personas / contactos externos

| Actor | Descripción |
|---|---|
| **Contacto** | Cualquier persona que escribe por primera vez a una red social conectada. Lo atiende primero el Agente de respuesta a potenciales clientes (M2). |
| **Seguidor** | Contacto clasificado como no-prospecto, o persona que sigue la cuenta sin mostrar interés comercial (vía M3). Tiene una **categoría de interés** (ej. empleo, información, producto). Se guarda categorizado — no se descarta — para remarketing o difusión segmentada futura. |
| **Prospecto** | Contacto clasificado como cliente potencial. Avanza en el funnel: encuesta, agendamiento, reunión, seguimiento. |
| **Cliente** | Prospecto que cerró al menos una Oportunidad de forma ganada. Transformación de ciclo de vida del Prospecto (conserva su historial). |

## Agentes de IA (módulos)

| Actor | Módulo | Descripción |
|---|---|---|
| **Agente de respuesta a potenciales clientes** | M2 | Habla con el Contacto por WhatsApp u otra red social. Lo clasifica (Seguidor/Prospecto) y, si es Prospecto, recolecta los datos obligatorios de la encuesta. |
| **Agente de bienvenida y categorización de seguidores** | M3 | Se activa con el evento "seguir" (no con un mensaje). Ofrece un menú de opciones (productos/servicios) y categoriza el interés de cada seguidor; puede derivar a WhatsApp hacia M2 cuando el interés es comercial. |
| **Agente de agendamiento y cierre** | M6 | Coordina la fecha de reunión con el cliente, la confirma con la Líder, agenda el evento (Calendar/Meet), y da seguimiento post-reunión con el equipo comercial. |
| **Agente de atención a Gerencia** | M4 | Responde en lenguaje natural (Telegram o WhatsApp) consultas estadísticas de Gerencia contra la base compartida. |

## Personas del equipo (internas a la organización)

| Rol | Responsabilidades |
|---|---|
| **Administrador** | Rol técnico, dueño del producto. Da de alta usuarios y controla sus permisos, conecta las redes sociales de la organización, y gestiona el **Panel de Administración/Configuración** (plantilla de la compañía: mensajes, opciones, preguntas de encuesta, parámetros como el plazo máximo de agendamiento). |
| **Líder de área comercial** | Rol único (una persona). Recibe cada Prospecto calificado con su contexto antes de la reunión. Decide si lo atiende ella misma o lo **focaliza** (reasigna la conversación) a un Usuario comercial. Es la única que puede asignar/reasignar casos. Confirma la fecha final de cada reunión según su disponibilidad real. Queda como supervisora de cualquier hilo que reasigne. |
| **Usuario comercial** | Atiende directamente al cliente solo cuando la Líder lo asigna; no interviene en todos los casos. No puede reasignar casos a otros. |
| **Gerencia** | Puede ser más de una persona. No participa en el flujo operativo ni en reuniones. Solo consume estadísticas: dashboard web con login (M5), o consultas en lenguaje natural vía el Agente de atención a Gerencia (M4). |

## Relación entre roles

```
Seguidor de red social ──(evento "seguir")──> M3 ──> Seguidor categorizado
                                                  └──(interés comercial)──> enlaza a WhatsApp
                                                                                  │
Contacto (mensaje) ──(clasifica)──> M2 ──> Seguidor
                                       └──> Prospecto ──(datos completos)──> M6
                                                                                  │
                                                           Líder comercial <──────┘
                                                              │
                                                (atiende ella) │ (focaliza)
                                                              ▼
                                                       Usuario comercial
                                                              │
                                                          Reunión
                                                              │
                                                    M6 (seguimiento post-reunión)
                                                              │
                                                    Resultado → Oportunidad/Cliente
                                                              │
                                                     Gerencia (M5 dashboard / M4 consulta NL)
```

> Nota de arquitectura: cada módulo de este diagrama actúa de forma independiente,
> observando el estado de la base de datos compartida — ninguno llama directamente a
> otro (ver capa 8).
