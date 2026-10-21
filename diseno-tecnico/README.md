# Diseño Técnico — CRM Comercial Multicanal con IA

Este directorio traduce los requerimientos de negocio (`requerimientos/`) en decisiones
técnicas concretas: stack, esquema de base de datos, prompts de agentes, seguridad y
despliegue. Construido sobre el modelo modular ya cerrado en
`requerimientos/08-modulos-y-arquitectura-comercial.md`.

## Documentos

| # | Documento | Contenido |
|---|---|---|
| 1 | [01-investigacion-tecnologica.md](01-investigacion-tecnologica.md) | Stack confirmado por módulo (WhatsApp, Instagram/Facebook, n8n, Claude+Gemini, Supabase, Calendar, Next.js) y barrido de viabilidad de redes adicionales (X, TikTok, LinkedIn, Google Business Messages) |
| 2 | [02-esquema-base-datos.md](02-esquema-base-datos.md) | Esquema completo de Postgres/Supabase: tablas, tipos, constraints, vistas de métricas |
| 3 | [03-triggers-y-flujo-resumen-cierre.md](03-triggers-y-flujo-resumen-cierre.md) | Las 3 clases de disparador por módulo (webhook externo / Realtime interno / cron interno) y el flujo de generación de `resumen_cierre` |
| 4 | [04-system-prompts-agentes.md](04-system-prompts-agentes.md) | System prompts y funciones permitidas de M2, M3, M4 — patrón de restricción por funciones acotadas |
| 5 | [05-politicas-rls.md](05-politicas-rls.md) | Políticas RLS en SQL ejecutable, para el acceso humano (los agentes usan `service_role` y las omiten) |
| 6 | [06-estructura-repositorio.md](06-estructura-repositorio.md) | Organización del monorepo: `supabase/`, `n8n/`, `prompts/`, `app/`, `infra/` |
| 7 | [07-plan-despliegue-por-cliente.md](07-plan-despliegue-por-cliente.md) | Qué significa "duplicar infraestructura": Docker Compose por cliente, Caddy, secretos, checklist de alta |
| 8 | [08-panel-maestro-fase-futura.md](08-panel-maestro-fase-futura.md) | *(fase futura, no implementada)* Monitoreo de salud (Uptime Kuma) y registro de clientes vendidos |

## Estado

Decisiones 1–7 cerradas y confirmadas con el usuario. La 8 queda documentada como
contexto para una fase posterior, disparada cuando exista más de un cliente activo
simultáneamente.

## Siguiente paso

Con esto, el diseño técnico tiene lo necesario para empezar la implementación: crear
el repositorio con la estructura de la capa 6, escribir las migraciones SQL de la
capa 2, y montar el primer workflow de n8n (M2) sobre el esquema ya definido.
