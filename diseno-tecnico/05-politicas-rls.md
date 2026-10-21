# 5. Políticas RLS (Row Level Security)

> Pasa a SQL ejecutable las reglas de acceso descritas en prosa en
> `diseno-tecnico/02-esquema-base-datos.md`.

## Aclaración previa — a quién le aplica esto

**RLS solo protege el acceso humano** (M1, M5, Panel Administrativo — la app Next.js
autenticada con Supabase Auth, usando la clave `anon`/`authenticated` del usuario que
inició sesión). Los agentes de n8n (M2, M3, M4, M6) se conectan con la
**`service_role` key**, que **omite RLS por diseño** — necesitan lectura/escritura
amplia para implementar la lógica de negocio. Su control de seguridad no es RLS, es el
set cerrado de funciones por agente ya definido en `diseno-tecnico/04`. Son dos capas
de seguridad distintas, cada una resolviendo un problema distinto (acceso de personas
vs. acceso de agentes automatizados).

## Funciones auxiliares

```sql
create or replace function mi_rol() returns rol_usuario
language sql security definer stable as $$
  select rol from usuario where id = auth.uid();
$$;
```

## Habilitar RLS

```sql
alter table usuario enable row level security;
alter table canal enable row level security;
alter table plantilla_compania enable row level security;
alter table niveles_modulo enable row level security;
alter table parametro_configuracion enable row level security;
alter table contacto enable row level security;
alter table seguidor enable row level security;
alter table prospecto enable row level security;
alter table oportunidad enable row level security;
alter table conversacion enable row level security;
alter table mensaje enable row level security;
alter table reunion enable row level security;
alter table resultado_seguimiento enable row level security;
alter table historial_evento enable row level security;
alter table resumen_cierre enable row level security;
alter table rutina_ejecucion enable row level security;
```

## `usuario` — todos ven el directorio, solo Administrador lo gestiona

```sql
create policy usuario_select_todos on usuario
  for select using (true);

create policy usuario_gestion_admin on usuario
  for insert with check (mi_rol() = 'administrador');

create policy usuario_update_admin on usuario
  for update using (mi_rol() = 'administrador');

create policy usuario_delete_admin on usuario
  for delete using (mi_rol() = 'administrador');
```

## Configuración (`canal`, `plantilla_compania`, `niveles_modulo`, `parametro_configuracion`) — solo Administrador

```sql
create policy admin_todo on canal for all
  using (mi_rol() = 'administrador') with check (mi_rol() = 'administrador');

create policy admin_todo on plantilla_compania for all
  using (mi_rol() = 'administrador') with check (mi_rol() = 'administrador');

create policy admin_todo on niveles_modulo for all
  using (mi_rol() = 'administrador') with check (mi_rol() = 'administrador');

create policy admin_todo on parametro_configuracion for all
  using (mi_rol() = 'administrador') with check (mi_rol() = 'administrador');
```

## `conversacion` — Líder ve todo, Usuario comercial solo lo suyo, Gerencia no entra

```sql
create policy conversacion_select on conversacion
  for select using (
    mi_rol() in ('administrador', 'lider_comercial')
    or (mi_rol() = 'usuario_comercial' and propietario_usuario_id = auth.uid())
  );

-- Reasignar/focalizar (capa 5: solo la Líder puede reasignar) es un UPDATE
create policy conversacion_update_lider on conversacion
  for update using (mi_rol() in ('administrador', 'lider_comercial'));
```
Nota: Gerencia **no tiene policy aquí** — sin policy, el acceso queda denegado por
defecto (consistente con "no participa del flujo operativo").

## `mensaje` — mismo criterio que `conversacion`

```sql
create policy mensaje_select on mensaje
  for select using (
    mi_rol() in ('administrador', 'lider_comercial')
    or exists (
      select 1 from conversacion c
      where c.id = mensaje.conversacion_id and c.propietario_usuario_id = auth.uid()
    )
  );

-- Un humano solo escribe mensajes como remitente 'usuario', en su propia conversación
-- (o cualquiera, si es Líder/Admin)
create policy mensaje_insert_humano on mensaje
  for insert with check (
    remitente = 'usuario' and (
      mi_rol() in ('administrador', 'lider_comercial')
      or exists (
        select 1 from conversacion c
        where c.id = mensaje.conversacion_id and c.propietario_usuario_id = auth.uid()
      )
    )
  );
```

## `contacto`, `seguidor`, `prospecto`, `oportunidad` — lectura amplia, sin datos crudos de chat

Estas tablas no contienen el contenido de la conversación (eso vive en `mensaje`), así
que es seguro que Gerencia también las lea — es justo lo que necesitan las vistas de
métricas (UC9).

```sql
create policy lectura_general on contacto
  for select using (mi_rol() in ('administrador', 'lider_comercial', 'usuario_comercial', 'gerencia'));

create policy lectura_general on seguidor
  for select using (mi_rol() in ('administrador', 'lider_comercial', 'usuario_comercial', 'gerencia'));

create policy lectura_general on prospecto
  for select using (mi_rol() in ('administrador', 'lider_comercial', 'usuario_comercial', 'gerencia'));

create policy lectura_general on oportunidad
  for select using (mi_rol() in ('administrador', 'lider_comercial', 'usuario_comercial', 'gerencia'));
```
Sin policies de `insert`/`update`/`delete` para roles humanos — esas tablas las
escriben los agentes (`service_role`), no la app.

## `reunion`, `resultado_seguimiento`, `historial_evento` — detalle operativo, sin Gerencia

```sql
create policy detalle_operativo on reunion
  for select using (
    mi_rol() in ('administrador', 'lider_comercial')
    or (mi_rol() = 'usuario_comercial' and exists (
      select 1 from oportunidad o
      join prospecto p on p.contacto_id = o.prospecto_id
      join conversacion c on c.contacto_id = p.contacto_id
      where o.id = reunion.oportunidad_id and c.propietario_usuario_id = auth.uid()
    ))
  );

create policy detalle_operativo on resultado_seguimiento
  for select using (
    mi_rol() in ('administrador', 'lider_comercial')
    or (mi_rol() = 'usuario_comercial' and exists (
      select 1 from reunion r
      join oportunidad o on o.id = r.oportunidad_id
      join prospecto p on p.contacto_id = o.prospecto_id
      join conversacion c on c.contacto_id = p.contacto_id
      where r.id = resultado_seguimiento.reunion_id and c.propietario_usuario_id = auth.uid()
    ))
  );

create policy detalle_operativo on historial_evento
  for select using (
    mi_rol() in ('administrador', 'lider_comercial')
    or (mi_rol() = 'usuario_comercial' and exists (
      select 1 from conversacion c
      where c.contacto_id = historial_evento.contacto_id and c.propietario_usuario_id = auth.uid()
    ))
  );
```

## `resumen_cierre` — el único detalle "de cierre" que Gerencia sí ve

```sql
create policy resumen_cierre_select on resumen_cierre
  for select using (mi_rol() in ('administrador', 'lider_comercial', 'gerencia'));
```
Es la pieza diseñada justo para esto (capa 2 del diseño técnico): Gerencia no ve la
conversación cruda, pero sí el resumen narrativo y los factores de por qué se ganó o
perdió cada Oportunidad.

## `rutina_ejecucion` — visibilidad para la Líder, sin más

```sql
create policy rutina_select_lider on rutina_ejecucion
  for select using (mi_rol() in ('administrador', 'lider_comercial'));
```

## Nota sobre las vistas de `diseno-tecnico/02` (`vista_metricas_dashboard`, `vista_factores_cierre`)

Al crearlas, agregar `with (security_invoker = true)` (Postgres 15+, soportado por
Supabase) para que respeten el RLS del usuario que consulta en vez del dueño de la
vista:

```sql
create view vista_metricas_dashboard
  with (security_invoker = true) as
  select ...
```
Sin esto, una vista corre con los privilegios de quien la creó, no de quien la
consulta — podría filtrar datos de más o de menos según cómo se haya desplegado.
