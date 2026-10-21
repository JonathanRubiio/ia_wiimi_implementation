# 6. Estructura del Repositorio

## Decisión: monorepo, no un repo por módulo

Los 6 módulos (M1–M6) se venden por separado (capa 8 de requerimientos), pero **el
código vive en un solo repositorio**. Razones:

- Todos comparten el mismo esquema de base de datos (`diseno-tecnico/02`) — separarlos
  en repos distintos obligaría a sincronizar un esquema compartido entre varios repos,
  sin beneficio real para un solo desarrollador.
- El empaquetado comercial (qué módulo está activo/Normal/Premium) ya es una decisión de
  **feature-gating en runtime** (tabla `niveles_modulo`), no de separación de código
  fuente — un módulo "no vendido" simplemente no se activa, no hace falta que viva en
  otro repositorio.
- Un monorepo es más simple de desplegar junto (un solo `docker-compose` por cliente,
  capa 7) y de versionar (un solo commit puede tocar el esquema de BD y el workflow de
  n8n que depende de él, de forma atómica).

## Estructura propuesta

```
proyecto IA/
├── requerimientos/              # ya existe — specs de negocio (capas 1–8)
├── diseno-tecnico/               # ya existe — decisiones técnicas (este conjunto de docs)
├── supabase/
│   ├── migrations/               # SQL versionado (Supabase CLI): 0001_init.sql, 0002_rls.sql...
│   ├── seed.sql                   # datos iniciales: niveles_modulo, parametro_configuracion por defecto
│   └── config.toml                # config del Supabase CLI
├── n8n/
│   ├── m2-clasificacion-encuesta.json
│   ├── m3-bienvenida-seguidores.json
│   ├── m4-consulta-gerencia.json
│   ├── m6-agendamiento-cierre.json
│   ├── rutinas-cron.json
│   └── README.md                  # convención de export/import, cómo probar un workflow local
├── prompts/
│   ├── m2.md
│   ├── m3.md
│   └── m4.md
├── app/                            # Next.js — M1 (bandeja), M5 (dashboard), Panel Administrativo
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/login/
│   │   │   ├── comercial/          # M1 — vista Bot/Manual, UC11
│   │   │   ├── dashboard/          # M5 — estadísticas, UC9
│   │   │   └── admin/              # Panel Administrativo — Plantilla de Compañía
│   │   ├── components/
│   │   └── lib/supabase/           # cliente Supabase + tipos generados (`supabase gen types`)
│   └── package.json
├── infra/
│   ├── docker-compose.yml          # Supabase self-hosted + n8n + app, parametrizado por cliente
│   ├── .env.example
│   └── alta-cliente-nuevo.md       # checklist para desplegar una instancia nueva (detalle en #4)
├── notas-recoleccion.md            # ya existe
└── README.md                        # nuevo — índice general de todo el repo
```

## Por qué `prompts/` está separado de `diseno-tecnico/04`

`diseno-tecnico/04-system-prompts-agentes.md` es la **documentación explicada** (el
"por qué" de cada regla del prompt, pensada para que una persona la lea y entienda la
decisión). `prompts/*.md` son los **archivos planos que de verdad se inyectan** en el
nodo de n8n que llama a Claude — sin comentarios ni justificación, solo el texto final.
Mantenerlos separados evita que cambiar el prompt en producción implique editar (o
desordenar) el documento narrativo, y viceversa. Cuando se actualice uno, el otro se
revisa para mantenerlos coherentes — no se generan automáticamente el uno del otro.

## Por qué los workflows de n8n se versionan como JSON exportado

n8n permite exportar cualquier workflow a JSON (vía UI o API) e importarlo en otra
instancia. Guardarlos en `n8n/*.json` dentro del repo significa que **desplegar un
cliente nuevo es importar los mismos 5 archivos**, no reconstruir los flujos a mano
cada vez — y cualquier cambio a un flujo pasa por el mismo control de versiones que el
resto del código.

## Qué falta (se resuelve en el siguiente documento, #4)

El contenido real de `infra/docker-compose.yml`, `.env.example` y el checklist de
`alta-cliente-nuevo.md` — qué significa concretamente "duplicar la infraestructura"
cuando entra un cliente nuevo.
