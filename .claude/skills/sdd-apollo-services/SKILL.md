---
name: sdd-apollo-services
description: Spec-Driven Development adaptado a este proyecto (sin GitLab/MR) — planifica cambios grandes como un contrato revisable (.sdd/<slug>/) con gate de aprobación antes de codear, y audita lo ya construido contra ese mismo estándar. Usar al iniciar cada módulo (M1–M6), ante riesgo arquitectónico, o cuando se pida repasar/mejorar lo ya planteado.
---

# SDD adaptado a este proyecto

Basado en las convenciones abiertas de **OpenSpec** (github.com/Fission-AI/OpenSpec) y el
flujo de aprobación de **Gentle-AI** (github.com/Gentleman-Programming/gentle-ai) — sin
instalar ninguno de los dos, adaptado a: GitHub (no GitLab/MR), un solo desarrollador
(no hay revisor externo — la "aprobación" es del usuario, no de un par), y a los
documentos que ya existen en `requerimientos/` y `diseno-tecnico/`.

## Cuándo usarla

- Al empezar la implementación de un módulo (M1–M6) u otra pieza grande.
- Cuando hay riesgo arquitectónico o incertidumbre genuina sobre el enfoque.
- Cuando el usuario pide explícitamente "repasar/mejorar lo ya planteado" (modo
  auditoría, ver abajo).

No usarla para cambios pequeños o mecánicos — ahí se va directo a un commit normal
(`wiedii-dev:git-workflow`, ya en uso en este proyecto).

## Fase 0 — Recuperar contexto (nunca inventar)

Antes de escribir nada, en este orden:
1. **Engram** (`mem_search`, `mem_context`) — decisiones previas de esta sesión y de
   sesiones pasadas sobre este proyecto.
2. `requerimientos/README.md` y `diseno-tecnico/README.md` — qué ya está cerrado.
3. `notas-recoleccion.md` — historial crudo de cómo se llegó a cada decisión.
4. `git log --oneline -20` — qué se ha hecho en código/documentos hasta ahora.

Si algo no está definido ahí, decirlo explícitamente en el plan — nunca inventar una
convención que no exista.

## Fase 1 — Escribir el contrato (`.sdd/<slug-del-cambio>/`)

Crear como mínimo:

- **`proposal.md`**: título, problema, objetivo, alcance incluido/excluido, enfoque
  propuesto, riesgos principales, supuestos abiertos.
- **`spec.md`**: requisitos funcionales (y no funcionales si aplica), escenarios de uso,
  criterios de aceptación (verificables), restricciones técnicas conocidas.
- **`design.md`** (solo si hay riesgo arquitectónico real): diseño, alternativas
  consideradas, trade-offs.
- **`tasks.md`**: el trabajo partido en unidades revisables.

### Búsqueda activa de alternativas (obligatorio en `design.md`)

Antes de proponer una implementación desde cero, buscar si existe una herramienta o
proyecto **open source** que resuelva lo mismo y ahorre tiempo de desarrollo (esto es
un requisito explícito del usuario, no opcional). Documentar 2–3 candidatos reales
(nombre, repo, licencia, actividad del proyecto) y la razón de elegir uno — o de
construirlo a medida si ninguno encaja. Mismo criterio ya aplicado en
`diseno-tecnico/01-investigacion-tecnologica.md` (ej. por qué Chatwoot no, por qué
Supabase sí) — seguir ese nivel de rigor, no bajarlo.

## Fase 2 — Gate de aprobación (parada absoluta)

Presentar un resumen corto en el chat: objetivo, alcance propuesto, riesgos/preguntas
principales, y confirmar qué artefactos se crearon. Luego **parar** y preguntar
exactamente:

> **¿Apruebas este plan de implementación?**

Esperar confirmación explícita ("sí", "aprobado", o equivalente). El silencio no es
aprobación. Si pide cambios, ajustar los artefactos y volver a preguntar — nunca
empezar a programar antes de un sí explícito.

## Fase 3 — Implementar (tras aprobación)

Seguir el contrato de `spec.md`. Si la realidad diverge de lo planeado, **actualizar el
spec** y señalarlo — no dejar que el contrato quede desactualizado en silencio.
Commits siguiendo `wiedii-dev:git-workflow` (Conventional Commits + emoji), push directo
a `master` (no hay flujo de MR en este repo — es GitHub, un solo desarrollador).

## Fase 4 — Guardar la decisión

Al cerrar el cambio, `mem_save` en Engram con la decisión clave y por qué — para que el
siguiente ciclo de SDD la recupere en la Fase 0 sin tener que repreguntar.

## Modo auditoría — repasar y mejorar lo ya planteado

Cuando se pida explícitamente revisar/mejorar lo ya construido (`requerimientos/`,
`diseno-tecnico/`):

1. Para cada documento, verificar que cubre lo equivalente a `proposal`/`spec`/`design`
   de OpenSpec: ¿el problema y el objetivo quedan claros? ¿hay criterios de aceptación
   verificables? ¿se consideraron alternativas open source antes de decidir construir
   algo a medida?
2. Señalar huecos encontrados de forma concreta (no "podría mejorar" genérico — decir
   exactamente qué falta y en qué documento).
3. Para cada hueco, proponer la mejora directamente (no solo señalarla) y presentarla
   al usuario para su aprobación antes de editar los documentos ya cerrados — un
   documento cerrado no se reabre sin que el usuario lo confirme primero.

## Criterios de salida

Un ciclo de SDD se hizo bien solo si: se recuperó el contexto real (sin inventar) →
existen `proposal.md` + `spec.md` bajo `.sdd/<slug>/` → se buscaron alternativas open
source en `design.md` cuando aplicaba → se presentó el resumen y se preguntó
exactamente la pregunta del gate → se esperó aprobación explícita → la implementación
siguió el spec → la decisión quedó guardada en Engram.
