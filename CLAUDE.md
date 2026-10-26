# CRM Comercial Multicanal con IA — Contexto del Proyecto

Proyecto personal de Jonathan: CRM multicanal (WhatsApp, Instagram, Facebook) con
agentes de IA que clasifican contactos, califican prospectos, agendan reuniones y dan
seguimiento comercial. Se vende por módulos independientes (M1–M6), cada cliente con su
propia infraestructura duplicada.

## Dónde está cada cosa (leer en este orden al retomar el proyecto)

1. **`requerimientos/README.md`** — lógica de negocio en 8 capas, agnóstica de stack.
   Todas cerradas y confirmadas con el usuario.
2. **`diseno-tecnico/README.md`** — decisiones técnicas (stack, esquema de BD, prompts
   de agentes, RLS, estructura de repo, despliegue). 1–7 cerradas; la 8 (Panel Maestro)
   es fase futura documentada, no implementada.
3. **`notas-recoleccion.md`** — historial crudo de preguntas/respuestas que originó los
   documentos de arriba. Consultar solo si falta el "por qué" de una decisión.
4. **Engram (memoria persistente)** — `mem_search`/`mem_context` antes de asumir nada;
   las decisiones clave de cada fase se guardan ahí al cerrarla.

## Cómo se trabaja en este proyecto

- **Metodología**: cada fase se validó con el usuario en modo pregunta-respuesta antes
  de escribirse — no se avanza una capa/documento sin su confirmación explícita.
- **Para trabajo nuevo grande** (implementar un módulo, rediseñar algo con riesgo
  arquitectónico, o auditar/mejorar lo ya planteado): usar la skill `sdd-apollo-services` —
  contrato de spec en `.sdd/<slug>/` con gate de aprobación antes de codear.
- **Git**: commits con Conventional Commits **sin emoji** (anula para este proyecto la
  convención por defecto de `wiedii-dev:git-workflow`, que sí usa emoji), push directo
  a `master` en GitHub (`JonathanRubiio/ia_apollo_services_implementation`) — no hay
  flujo de MR, es un solo desarrollador. Nunca commitear/pushear sin confirmación
  explícita en el momento (regla global del usuario, no solo de este proyecto).
- **Documentos administrativos** (pitch, marco teórico, costos): skill `doc-generator`
  (python-docx/pptx/openpyxl ya instalados), aplicando `apa-format` cuando el tipo de
  documento lo requiera.
- **Identidad de marca**: skill `branding` — produce `marca/brand.md` y
  `marca/brand-tokens.json`, fuente única de colores/tipografía que `doc-generator`
  debe leer antes de generar cualquier documento.

## Skills del proyecto (`.claude/skills/`)

| Skill | Para qué |
|---|---|
| `sdd-apollo-services` | Planificar/auditar cambios grandes como contrato revisable, con búsqueda obligatoria de alternativas open source antes de construir algo a medida |
| `apa-format` | Formato APA 7ma edición para documentos académicos/teóricos |
| `doc-generator` | Generar `.docx`/`.pptx`/`.xlsx` reales desde el contenido ya desarrollado |
| `branding` | Paleta de colores, tipografía, tono de voz y brief de logo (sin artwork rasterizado) |

## Convenciones de carpetas aún por crear (las referencian las skills)

- `marca/` — artefactos de la skill `branding`.
- `scripts/` — scripts generadores de `doc-generator` (uno por documento).
- `documentos/` — entregables finales generados (`.docx`/`.pptx`/`.xlsx`), nunca mezclados con `requerimientos/`/`diseno-tecnico/`.
- `.sdd/<slug>/` — contratos de spec de `sdd-apollo-services`, uno por cambio grande.
