# Requerimientos — CRM Comercial Multicanal con IA

Este directorio es la **fuente de verdad del negocio** para el proyecto. Contiene la lógica
funcional completa, agnóstica de lenguaje y framework, levantada en 7 capas. Es el insumo
que alimenta la siguiente fase (diseño técnico + Spec-Driven Development), donde recién
ahí se elige stack y se escribe código.

## Capas

| # | Documento | Contenido |
|---|---|---|
| 1 | [01-vision-y-alcance.md](01-vision-y-alcance.md) | Problema, objetivo, stakeholders, alcance, restricciones |
| 2 | [02-actores-y-roles.md](02-actores-y-roles.md) | Quién interactúa con el sistema y qué puede hacer |
| 3 | [03-procesos-de-negocio.md](03-procesos-de-negocio.md) | Flujos end-to-end del negocio |
| 4 | [04-modelo-de-dominio-glosario.md](04-modelo-de-dominio-glosario.md) | Entidades, relaciones, lenguaje ubicuo |
| 5 | [05-reglas-de-negocio.md](05-reglas-de-negocio.md) | Invariantes, validaciones, parámetros configurables |
| 6 | [06-casos-de-uso.md](06-casos-de-uso.md) | Historias con criterios de aceptación (Given/When/Then) |
| 7 | [07-requerimientos-no-funcionales.md](07-requerimientos-no-funcionales.md) | Volumetría, tiempos de respuesta, datos personales, despliegue, resiliencia |
| 8 | [08-modulos-y-arquitectura-comercial.md](08-modulos-y-arquitectura-comercial.md) | Módulos comerciales independientes (M1–M6), arquitectura de comunicación vía estado en BD compartida, Panel de Administración |

## Estado

Todas las capas están cerradas con la información recolectada hasta la fecha. Quedan dos
puntos explícitamente pendientes de validar en fases posteriores (no bloquean el inicio del
diseño técnico):

- Validar con asesoría legal una Política de Tratamiento de Datos Personales (Habeas Data,
  Colombia) antes del lanzamiento comercial.
- Definir el nombre/alcance real del agente interno de seguimiento (candidato evaluado:
  OpenClaw — openclaw.ai) en la fase de diseño técnico.

## Siguiente paso

Cuando se vaya a construir, cada Caso de Uso de `06-casos-de-uso.md` se convierte en un
spec-contract técnico (bajo el flujo de Spec-Driven Development) donde ahí sí se elige
stack, arquitectura y se implementa bajo TDD.

> El archivo `notas-recoleccion.md` en la raíz del proyecto es el historial de trabajo
> (preguntas y respuestas) que dio origen a estos documentos. Esta carpeta es la versión
> consolidada y definitiva.
