# 8. Modelo Modular y Arquitectura de Comunicación

## Modelo comercial: módulos independientes

El producto se descompone en **módulos vendibles de forma independiente**, en
sub-paquete, o en paquete completo. El cliente arma su propia combinación libremente.

| Módulo | Qué hace |
|---|---|
| **M1 — Bandeja unificada** | Centraliza las conversaciones de redes sociales en un único filtro tipo CRM. |
| **M2 — Agente de respuesta a potenciales clientes** | Clasifica Seguidor/Prospecto y realiza la encuesta de datos obligatorios. |
| **M3 — Agente de bienvenida y categorización de seguidores** | Se activa con el evento "seguir" (no con un mensaje). Engancha con productos vía un menú de opciones y categoriza el interés de cada seguidor. |
| **M4 — Agente de atención a Gerencia** | Responde consultas en lenguaje natural (Telegram/WhatsApp), personalizado por organización. |
| **M5 — Dashboard gerencial** | Tablero web con login y estadísticas. |
| **M6 — Agente de agendamiento y cierre** | Coordina la fecha con el cliente, confirma con la Líder, agenda la reunión, y da seguimiento post-reunión con el equipo comercial. |

El **Panel de Administración / Configuración de la compañía** (ver más abajo) no es un
módulo opcional: es la infraestructura base que viene siempre, independientemente de qué
módulos se hayan comprado.

## Arquitectura de comunicación: solo vía estado en la base de datos compartida

**Regla general para todos los módulos** (no solo M2→M6): los módulos **nunca se llaman
directamente entre sí**. Cada módulo observa cambios de estado en la base de datos
compartida y decide su propio flujo a partir de ese estado.

Ejemplo: M2 marca a un Prospecto con `datos_completos = true`; M6 detecta esa condición
en la base de datos y arranca su propio flujo de agendamiento — sin que M2 lo invoque
directamente.

Esto permite:

- Vender cualquier módulo de forma independiente del resto.
- Que un módulo siga funcionando aunque otro no esté activo o no haya sido comprado,
  siempre que exista en la base de datos el dato que necesita (sin importar quién lo
  puso ahí: otro módulo, carga manual, u otro canal de entrada).
- Que la dependencia entre módulos sea una **dependencia de datos**, nunca una
  dependencia de disponibilidad de otro agente.

Ejemplo aplicado al enlace Instagram → WhatsApp (ver capa 3, sub-flujo M3): cuando una
persona pasa de M3 a escribir por WhatsApp, M2 la recibe como cualquier mensaje entrante
y aplica su regla de identificación ya existente (capa 5): si el teléfono no existía,
la trata como Prospecto nuevo; si ya existía, retoma la conversación/Oportunidad desde
donde quedó. No existe ni se necesita una conexión directa entre M3 y M2.

## Panel de Administración / Configuración de la compañía

- Es una **única estructura base**, igual para todos los clientes del producto. Las
  funciones de los módulos no contratados quedan **deshabilitadas** según el plan o los
  servicios comprados — no se construyen paneles distintos por cliente.
- Cada compañía gestiona ahí su propia plantilla: información base de la empresa,
  mensajes de bienvenida, preguntas de la encuesta, opciones del menú de M3, y la
  conexión de sus redes sociales.
- Esta plantilla es la fuente única de contenido dinámico que alimenta a M2, M3 y los
  demás módulos conversacionales — nunca texto fijo embebido en el sistema.
