# 3. Procesos de Negocio

> Los nombres de módulo (M2, M3, M6...) referencian la capa 8 — Modelo Modular y
> Arquitectura.

## Flujo principal — vía mensaje directo (M2 + M6)

1. Un Contacto escribe por una red social (WhatsApp principalmente, en Colombia).
2. **M2** conversa con él y lo clasifica: **Seguidor** (recibe mensaje de cierre) o
   **Prospecto**.
3. Si es Prospecto, **M2** realiza una encuesta corta: nombre, correo, empresa/
   emprendimiento y necesidad (ver capa 5 — campos obligatorios).
4. Cuando el Prospecto queda con datos completos, **M6** detecta esa condición en la
   base de datos (ver capa 8 — nunca una llamada directa de M2 a M6) y le pregunta al
   cliente qué día y hora le sirve; envía esa propuesta, junto con el Resumen del
   cliente, a la Líder comercial.
5. La Líder revisa su disponibilidad real (reuniones ya agendadas) y le indica a M6 qué
   fecha confirmar.
6. M6 confirma la fecha con el cliente y agenda el evento (Calendar/Meet).
7. La Líder decide si atiende el caso ella misma, o lo **focaliza** (reasigna la
   conversación, dentro del mismo inbox) a un Usuario comercial. La Líder queda siempre
   como supervisora del hilo, incluso si lo reasigna.
8. Se realiza la reunión.
9. Un día después, **M6** pregunta al comercial qué pasó (cierre / sigue prospecto /
   sin acuerdo).
10. El resultado se guarda en la base compartida y actualiza el estado de la Oportunidad,
    alimentando las estadísticas de Fase 2 (M5/M4).

## Flujo alterno — vía evento "seguir" (M3)

1. Una persona sigue la cuenta de una red social conectada (hoy implementado en
   Instagram; abierto a otras redes con concepto de "seguidor" si es viable).
2. **M3** envía un mensaje de bienvenida automático con un menú de opciones (los
   productos/servicios configurados en el Panel de Administración de la compañía).
3. Según la opción elegida:
   - **"Quiero trabajar con ustedes" (empleo)** → mensaje + enlace externo a la página
     de oportunidades de empleo. Se registra como **Seguidor** con categoría de interés
     `empleo`. No se convierte en Prospecto.
   - **"Interesado en un producto / trabajar con la compañía" (comercial)** → se enlaza
     a WhatsApp para continuar el flujo comercial. Al escribir ahí, activa **M2**, que
     aplica su regla de identificación ya existente (capa 5): si el teléfono no existía,
     lo trata como Prospecto nuevo; si ya existía, retoma la conversación/Oportunidad
     desde donde quedó.
   - **"Conocer más de la compañía"** → enlace a la página oficial de la empresa. Se
     registra como **Seguidor** con categoría de interés `información`. No se convierte
     en Prospecto.
4. Todas las categorías de interés quedan disponibles para **difusión segmentada** a
   futuro (ej. enviar un mensaje a todos los Seguidores con interés `empleo` cuando se
   abre una vacante en un área específica).

### Campaña a seguidores históricos
Al activar M3, además del disparador automático para cada nuevo seguidor desde ese
momento, se envía (una sola vez) el mismo mensaje de bienvenida a quienes ya seguían la
cuenta antes. Este envío **no es masivo**: se despliega de forma gradual/escalonada,
para no saturar al equipo que debe atender las respuestas.

## Sub-flujo: conversación abandonada

Si el Contacto abandona la encuesta a medias (M2), se guarda como **Prospecto parcial**
con la fase en la que quedó. 24 horas después del último contacto se dispara una rutina
que retoma esa fase. Tras **3 reintentos** sin respuesta, el caso pasa a estado
`no_atiende`.

Si el Prospecto en `no_atiende` vuelve a escribir por su cuenta, el sistema lo reconoce,
reactiva su estado y envía un mensaje predeterminado de reactivación antes de continuar.

## Sub-flujo: falla el agendamiento automático

Si M6 no logra llegar a una fecha viable dentro del plazo configurado (parámetro
ajustable por el Administrador, referencia 7–14 días):

1. Se notifica al grupo donde está la Líder: "no se pudo agendar cita con [cliente],
   realiza el proceso manual".
2. M6 le solicita después la fecha/hora en que quedó la reunión manual, para mantener
   el registro en el sistema.

## Sub-flujo: atención manual directa

La Líder puede tomar un caso de forma manual en cualquier momento (incluso con datos
incompletos). Al hacerlo, el caso pasa a estado `atencion_manual` y el módulo
correspondiente (M2 o M6) deja de actuar sobre él — todo se maneja desde ahí por la
persona.

## Sub-flujo: seguimiento post-reunión

Rutina diaria de M6, al inicio del día. Solo se activa si existe una reunión ya
realizada pendiente de calificar (si no hay ninguna, no se envía nada). Si el comercial
no responde, la rutina insiste diariamente hasta obtener respuesta.

## Sub-flujo: contacto recurrente con nueva necesidad

Si un Prospecto ya existente (identificado por teléfono o correo) escribe sobre una idea
de desarrollo distinta a la anterior, M2 crea una nueva **Oportunidad** bajo el mismo
Prospecto, usando el mismo hilo de conversación de WhatsApp.

## Capacidad transversal requerida

M2 debe poder procesar **texto, audio e imágenes** que envíe el cliente. Ese contenido
no es interpretado para tomar decisiones de flujo (la única decisión que el agente
interpreta es la clasificación Seguidor/Prospecto); solo alimenta, como referencia, el
Resumen de cliente que ve el comercial.
