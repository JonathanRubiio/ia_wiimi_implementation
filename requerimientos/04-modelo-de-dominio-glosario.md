# 4. Modelo de Dominio y Glosario

## Entidades

| Entidad | Descripción |
|---|---|
| **Organización** | La empresa que usa el sistema (una instancia independiente por organización — ver capa 7). |
| **Usuario** | Persona del equipo, con rol Administrador, Líder comercial o Usuario comercial. |
| **Canal / Red Social** | WhatsApp, Instagram, etc., conectado a la Organización. |
| **Contacto** | Persona que escribe por primera vez. Nace como candidato a Seguidor. |
| **Seguidor** | Contacto clasificado como no-prospecto, o persona que siguió la cuenta sin derivar a interés comercial. Entidad propia; se guarda y categoriza, no se descarta. Tiene una **Categoría de interés** (ej. `empleo`, `información`, `producto`). |
| **Prospecto** | Contacto clasificado como cliente potencial. Entidad propia, separada de Seguidor. Guarda los datos generales reutilizables: nombre, correo, empresa. Estados: `parcial`, `en_proceso`, `no_atiende`, `sin_acuerdo`, o transformado en **Cliente**. |
| **Oportunidad** | Cada idea/necesidad de desarrollo distinta que plantea un mismo Prospecto. Un Prospecto puede tener varias Oportunidades, en paralelo o en el tiempo, sin límite. Tiene su propio detalle/necesidad y su propio estado (activa/cerrada). Las Oportunidades cerradas se archivan (dejan de ser visibles en la vista de trabajo, no se eliminan). |
| **Conversación / Hilo** | Unificado, vinculado al Contacto/Prospecto y a un Canal. Tiene un propietario (Líder o Usuario comercial); la Líder queda siempre como supervisora aunque reasigne. Varias Oportunidades del mismo Prospecto comparten el mismo hilo. |
| **Mensaje** | Texto, audio o imagen dentro de una Conversación. |
| **Resumen de Cliente** | Recapitulación de lo preguntado por el agente, entregada al comercial como contexto antes de la reunión. Los datos base (nombre, correo, empresa) viven en el Prospecto; el detalle de necesidad es propio de cada Oportunidad. |
| **Reunión** | Pertenece a una Oportunidad (no directamente al Prospecto). Tiene fecha/hora, enlace Meet, estado (agendada automática / manual / realizada). Una Oportunidad puede tener varias reuniones hasta su cierre. |
| **Resultado de Seguimiento** | Cierre / sigue prospecto / sin acuerdo. Se reporta tras cada Reunión y actualiza el estado de la Oportunidad. |
| **Rutina** | Proceso automático recurrente disparado por tiempo o evento: reintento 24h por abandono, aviso de falla de agendamiento, seguimiento diario post-reunión. |
| **Parámetro de Configuración** | Valores ajustables por el Administrador (ej. días máximos para concretar una reunión). |
| **Categoría de Interés** | Etiqueta asignada a un Seguidor según la opción elegida en el menú de bienvenida de M3 (ej. `empleo`, `información`, `producto`). Habilita difusión segmentada a futuro. |
| **Plantilla de Compañía** | Información base de la organización gestionada desde el Panel de Administración: mensajes de bienvenida, preguntas de encuesta, opciones de menú. Fuente única de contenido dinámico para M2 y M3 — nunca texto fijo embebido. |

## Relaciones clave

- Un **Prospecto** tiene **muchas Oportunidades** (1:N), sin límite de oportunidades activas simultáneas.
- Una **Oportunidad** tiene **muchas Reuniones** (1:N), hasta llegar a un cierre.
- Un **Prospecto** se **transforma en Cliente** cuando al menos una Oportunidad cierra ganada (transformación de ciclo de vida, no una entidad desconectada: conserva historial y datos generales).
- El identificador natural de un Prospecto/Cliente es su **teléfono y/o correo** (ambos únicos en el sistema) — ver capa 5.

## Glosario

| Término | Definición |
|---|---|
| **Seguidor** | Contacto clasificado como no-prospecto; se guarda igual, no se descarta. |
| **Prospecto** | Contacto clasificado como cliente potencial. |
| **Oportunidad** | Cada idea/necesidad de desarrollo distinta que plantea un mismo Prospecto. |
| **Focalizar** | Reasignar la propiedad de una conversación de la Líder a un Usuario comercial (la Líder queda como supervisora). |
| **Rutina** | Proceso automático recurrente disparado por tiempo o evento. |
| **Resumen de Cliente** | Recapitulación de lo preguntado por el agente, entregada al comercial como contexto. |
| **`no_atiende`** | Estado de una Oportunidad/Prospecto tras 3 reintentos fallidos de contacto; reactivable si el cliente vuelve a escribir. |
| **`atencion_manual`** | Estado de un caso que la Líder tomó manualmente; el bot deja de actuar sobre él. |
| **Módulo** | Unidad funcional y comercial independiente (M1–M6, ver capa 8); se vende sola, en sub-paquete o en paquete completo. |
