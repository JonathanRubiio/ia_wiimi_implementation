# 2. Esquema de Base de Datos (Supabase / PostgreSQL)

> Traduce el modelo de dominio (`requerimientos/04`) y las reglas de negocio
> (`requerimientos/05`) a tablas concretas. Nomenclatura en español, consistente con el
> glosario ya fijado. Un esquema de este tipo se despliega **por cada cliente**
> (infraestructura duplicada, capa 7 de requerimientos).

## Principio de diseño

Cada módulo (M1–M6) lee y escribe directamente sobre estas tablas — **nunca se llaman
entre sí** (capa 8). La forma en que "se enteran" de un cambio es Supabase Realtime
(suscripción a cambios de fila) o un disparo periódico de n8n que consulta el estado.
Por eso casi todas las tablas tienen una columna `estado` explícita: es el contrato
entre módulos.

## Tipos enumerados

```sql
create type rol_usuario as enum ('administrador', 'lider_comercial', 'usuario_comercial', 'gerencia');
create type tipo_canal as enum ('whatsapp', 'instagram', 'facebook', 'telegram');
create type categoria_interes as enum ('empleo', 'producto', 'informacion', 'otro');
create type estado_prospecto as enum ('parcial', 'en_proceso', 'no_atiende', 'atencion_manual', 'sin_acuerdo', 'cliente');
create type estado_oportunidad as enum ('activa', 'cerrada_ganada', 'cerrada_perdida');
create type tipo_mensaje as enum ('texto', 'audio', 'imagen');
create type remitente_mensaje as enum ('contacto', 'agente', 'usuario');
create type vista_conversacion as enum ('bot', 'manual');
create type estado_reunion as enum ('propuesta', 'confirmada', 'realizada', 'cancelada');
create type tipo_agendamiento as enum ('automatico', 'manual');
create type resultado_seguimiento as enum ('cierre', 'sigue_prospecto', 'sin_acuerdo');
create type nivel_modulo as enum ('normal', 'premium');
```

## Tablas

### `organizacion` — fila única por instancia

```sql
create table organizacion (
  id uuid primary key default gen_random_uuid(),
  nombre text not null,
  creado_at timestamptz not null default now()
);
```

### `plantilla_compania` — fuente única de contenido dinámico (Panel de Administración)

```sql
create table plantilla_compania (
  organizacion_id uuid primary key references organizacion(id),
  info_base jsonb not null default '{}',        -- nombre comercial, descripción, etc.
  mensajes_bienvenida jsonb not null default '{}', -- texto de M3 (Normal/Premium)
  preguntas_encuesta jsonb not null default '[]',  -- preguntas que hace M2
  opciones_menu jsonb not null default '[]',       -- ramas de M3 (empleo/producto/info)
  actualizado_at timestamptz not null default now()
);
```

### `niveles_modulo` — feature-gating por plan contratado

```sql
create table niveles_modulo (
  organizacion_id uuid references organizacion(id),
  modulo text not null,            -- 'M1'..'M6'
  activo boolean not null default false,
  nivel nivel_modulo,              -- null si el módulo no tiene variante (ej. M6)
  primary key (organizacion_id, modulo)
);
```

### `usuario` — vinculado a Supabase Auth

```sql
create table usuario (
  id uuid primary key references auth.users(id),
  organizacion_id uuid references organizacion(id),
  nombre text not null,
  rol rol_usuario not null,
  creado_at timestamptz not null default now()
);
```
Regla de negocio: solo puede existir **una** fila con `rol = 'lider_comercial'` activa
por organización (capa 2 — rol único). Se aplica con un índice único parcial:
```sql
create unique index un_lider_comercial on usuario (organizacion_id)
  where rol = 'lider_comercial';
```

### `canal` — redes sociales conectadas

```sql
create table canal (
  id uuid primary key default gen_random_uuid(),
  organizacion_id uuid references organizacion(id),
  tipo tipo_canal not null,
  credenciales jsonb not null,     -- tokens/config del BSP o Graph API
  activo boolean not null default true,
  creado_at timestamptz not null default now()
);
```

### `contacto` — identidad base, nace como candidato a Seguidor

```sql
create table contacto (
  id uuid primary key default gen_random_uuid(),
  telefono text unique,
  correo text unique,
  canal_origen_id uuid references canal(id),
  creado_at timestamptz not null default now(),
  constraint al_menos_un_identificador check (telefono is not null or correo is not null)
);
```
Regla de negocio (capa 5): **teléfono y correo son únicos** — si cualquiera de los dos
ya existe, es el mismo Contacto/Prospecto. El `unique` de Postgres ya lo garantiza; la
lógica de "buscar por cualquiera de los dos antes de insertar" vive en el flujo de n8n.

### `seguidor` — subtipo de Contacto (tabla propia, 1:1)

```sql
create table seguidor (
  contacto_id uuid primary key references contacto(id),
  categoria_interes categoria_interes not null default 'otro',
  creado_at timestamptz not null default now()
);
```

### `prospecto` — subtipo de Contacto (tabla propia, 1:1)

```sql
create table prospecto (
  contacto_id uuid primary key references contacto(id),
  nombre text,
  correo text,
  empresa text,
  estado estado_prospecto not null default 'parcial',
  intentos_reintento int not null default 0,     -- máx. 3 antes de no_atiende
  ultimo_contacto_at timestamptz not null default now(),
  creado_at timestamptz not null default now()
);
```

### `oportunidad` — cada idea/necesidad distinta de un Prospecto

```sql
create table oportunidad (
  id uuid primary key default gen_random_uuid(),
  prospecto_id uuid not null references prospecto(contacto_id),
  necesidad text not null,
  estado estado_oportunidad not null default 'activa',
  creado_at timestamptz not null default now(),
  cerrada_at timestamptz
);
```
Sin límite de Oportunidades activas simultáneas (capa 5) — no hay constraint de
unicidad aquí a propósito.

### `conversacion` — hilo unificado (M1)

```sql
create table conversacion (
  id uuid primary key default gen_random_uuid(),
  contacto_id uuid not null references contacto(id),
  canal_id uuid not null references canal(id),
  propietario_usuario_id uuid references usuario(id),   -- null = lo maneja el bot
  supervisor_usuario_id uuid references usuario(id),    -- la Líder, si reasignó
  vista vista_conversacion not null default 'bot',
  creado_at timestamptz not null default now()
);
```
Varias Oportunidades del mismo Prospecto comparten la misma `conversacion` (capa 4) —
por eso `conversacion` cuelga de `contacto`, no de `oportunidad`.

### `mensaje`

```sql
create table mensaje (
  id uuid primary key default gen_random_uuid(),
  conversacion_id uuid not null references conversacion(id),
  remitente remitente_mensaje not null,
  tipo tipo_mensaje not null,
  contenido_texto text,              -- original, o ya normalizado por Gemini si era audio/imagen
  contenido_media_url text,          -- referencia en Supabase Storage
  creado_at timestamptz not null default now()
);
```

### `reunion` — pertenece a Oportunidad, no a Prospecto

```sql
create table reunion (
  id uuid primary key default gen_random_uuid(),
  oportunidad_id uuid not null references oportunidad(id),
  fecha_hora timestamptz,
  enlace_meet text,
  estado estado_reunion not null default 'propuesta',
  tipo_agendamiento tipo_agendamiento not null default 'automatico',
  creado_at timestamptz not null default now()
);
```

### `resultado_seguimiento` — uno por Reunión realizada

```sql
create table resultado_seguimiento (
  id uuid primary key default gen_random_uuid(),
  reunion_id uuid not null references reunion(id),
  resultado resultado_seguimiento not null,
  comentario text,
  creado_at timestamptz not null default now()
);
```

### `rutina_ejecucion` — control de las 3 rutinas automáticas

```sql
create table rutina_ejecucion (
  id uuid primary key default gen_random_uuid(),
  tipo text not null,                -- 'reintento_abandono' | 'seguimiento_post_reunion' | 'aviso_fallo_agendamiento'
  entidad_tipo text not null,        -- 'prospecto' | 'reunion'
  entidad_id uuid not null,
  proximo_disparo_at timestamptz not null,
  intentos int not null default 0,
  completada boolean not null default false,
  creado_at timestamptz not null default now()
);
create index idx_rutina_pendientes on rutina_ejecucion (proximo_disparo_at) where not completada;
```
n8n consulta esta tabla con su Schedule Trigger (capa técnica) en vez de tener lógica de
cron repartida — así cada rutina (24h, diaria post-reunión, aviso de fallo) es una fila
que se puede auditar e inspeccionar.

### `historial_evento` — bitácora de todo lo que le pasa a un Contacto/Prospecto

```sql
create table historial_evento (
  id uuid primary key default gen_random_uuid(),
  contacto_id uuid not null references contacto(id),
  oportunidad_id uuid references oportunidad(id),   -- null si el evento es a nivel Contacto/Prospecto
  tipo text not null,          -- 'clasificado' | 'datos_completos' | 'oportunidad_creada' |
                                -- 'reunion_agendada' | 'reunion_realizada' | 'resultado_registrado' |
                                -- 'reasignado' | 'estado_cambiado' | 'oportunidad_cerrada' | ...
  actor text not null,          -- 'agente_m2' | 'agente_m6' | 'usuario:<uuid>' | 'sistema'
  detalle jsonb not null default '{}',
  creado_at timestamptz not null default now()
);
create index idx_historial_contacto on historial_evento (contacto_id, creado_at);
```
Esta tabla es la que alimenta la **vista de "avances a detalle"** de un Prospecto
(UC: ver qué ha pasado con él, en orden cronológico) — cada paso relevante del flujo
(capa 3 de requerimientos) escribe una fila aquí, sin importar qué módulo lo generó.
No reemplaza a `mensaje` (que son los mensajes crudos de la conversación) — es la capa
de "qué decisiones/hitos ocurrieron", pensada para lectura humana y para alimentar
métricas, no para reconstruir la conversación palabra por palabra.

### `resumen_cierre` — por qué se ganó o se perdió una Oportunidad

```sql
create table resumen_cierre (
  oportunidad_id uuid primary key references oportunidad(id),
  resultado estado_oportunidad not null,     -- 'cerrada_ganada' | 'cerrada_perdida'
  factores_clave jsonb not null default '[]', -- tags: ej. ["precio", "tiempo_respuesta", "no_contactado_a_tiempo"]
  resumen_narrativo text not null,            -- recapitulación del proceso completo, generada al cierre
  generado_at timestamptz not null default now()
);
```
Se crea **una sola vez**, en el momento en que `oportunidad.estado` pasa a
`cerrada_ganada` o `cerrada_perdida` (M6, al recibir el resultado final de seguimiento).
Se arma recopilando `historial_evento` + `mensaje` + `resultado_seguimiento` de esa
Oportunidad — el "por qué" queda capturado una sola vez, en frío, para no tener que
reconstruirlo de nuevo cada vez que gerencia o el propio equipo comercial quiera
entender qué marcó la diferencia. Es el dato que después alimenta: reportes de
gerencia (patrones de por qué se gana/pierde), y consultas del Agente de Gerencia (M4)
tipo "¿qué pasó con el cliente X?".

### `parametro_configuracion`

```sql
create table parametro_configuracion (
  organizacion_id uuid references organizacion(id),
  clave text not null,              -- ej. 'plazo_maximo_agendamiento_dias'
  valor text not null,
  primary key (organizacion_id, clave)
);
```

## Índices y constraints clave que materializan reglas de negocio

| Regla (capa 5) | Mecanismo |
|---|---|
| Teléfono y correo únicos | `unique` en `contacto.telefono` y `contacto.correo` |
| Un solo Líder comercial activo | Índice único parcial en `usuario` |
| 3 reintentos antes de `no_atiende` | `prospecto.intentos_reintento`, validado en el flujo de n8n antes de actualizar `estado` |
| Oportunidades sin límite | Sin constraint de unicidad en `oportunidad.prospecto_id` |

## Row Level Security (Supabase)

Con `usuario.rol` como base, las políticas RLS reflejan los permisos ya definidos en
`requerimientos/02`:

- `gerencia`: `select` sobre `vista_metricas_dashboard`, `vista_factores_cierre` y
  `resumen_cierre` (el "por qué" ya resumido) — pero **no** sobre `conversacion`/
  `mensaje` en crudo, consistente con que Gerencia no participa del flujo operativo.
- `usuario_comercial`: `select`/`update` solo sobre `conversacion` (y su `mensaje`,
  `historial_evento`) donde `propietario_usuario_id = auth.uid()` — esto es lo que
  resuelve la "vista a detalle de avances" de sus propios Prospectos.
- `lider_comercial`: `select`/`update` sobre todas las conversaciones, `historial_evento`
  y `resumen_cierre` de la organización (puede reasignar y ver todo el detalle).
- `administrador`: acceso completo a `plantilla_compania`, `niveles_modulo`,
  `parametro_configuracion`, `canal`, `usuario`.

## Vistas para el Dashboard (M5, UC9)

No se agregan columnas denormalizadas — las 5 métricas mínimas de UC9 se calculan con
vistas sobre las tablas ya definidas:

```sql
create view vista_metricas_dashboard as
select
  (select count(*) from contacto) as personas_contactadas,
  (select count(*) from prospecto where estado = 'cliente') as cierres,
  (select count(*) from oportunidad where estado = 'activa') as procesos_abiertos,
  (select count(*) from prospecto
     where estado = 'parcial' and ultimo_contacto_at < now() - interval '24 hours'
  ) as dejaron_de_responder,
  (select count(*) from prospecto where estado = 'no_atiende') as sin_disponibilidad;
```

Y para la sección "por qué se gana/pierde" que habilita `resumen_cierre`:

```sql
create view vista_factores_cierre as
select resultado, jsonb_array_elements_text(factores_clave) as factor, count(*)
from resumen_cierre
group by resultado, factor
order by resultado, count(*) desc;
```

## Pendiente para el siguiente documento técnico

- Definir los canales de Supabase Realtime que escucha cada módulo (ej. M6 escucha
  `prospecto` donde `estado` cambia a `en_proceso` con datos completos).
- Definir quién/qué genera `resumen_cierre.resumen_narrativo` — candidato: un paso de
  n8n que, al cerrar la Oportunidad, le pide a Claude que resuma `historial_evento` +
  `mensaje` + `resultado_seguimiento` de esa Oportunidad en un texto corto.
