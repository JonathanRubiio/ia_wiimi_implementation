# 8. Panel Maestro del Operador — Fase Futura

> **No se implementa todavía.** Se documenta ahora para no perder el contexto de la
> decisión mientras se avanza en otras partes del diseño técnico. Se retoma cuando el
> número de clientes activos lo justifique.

## Problema que resuelve

Cada cliente tiene su propia instancia totalmente aislada (capa 7 de requerimientos:
infraestructura duplicada, no multi-tenant). Eso es correcto para el producto, pero
genera un problema distinto: **el dueño del producto no tiene una vista única de todas
las instancias que vendió** — para saber si alguna está caída, o para llevar el control
de quién es cliente y qué contrató, hoy tendría que revisar cada instancia por separado.

Este panel es **para el operador/dueño del producto**, no para los clientes — es
distinto del Panel Administrativo (capa 8 de requerimientos), que es por cliente y lo
usa el Administrador de cada organización para su propia instancia.

## Decisión tomada (para cuando se implemente)

Dos necesidades separadas, resueltas con herramientas distintas — no un solo desarrollo
a medida:

### 1. Estado de salud y alertas de caída → Uptime Kuma (no construir nada propio)

- Herramienta open source, self-hosted, un único contenedor Docker centralizado (no uno
  por cliente).
- Cada stack de cliente expone un endpoint de salud: n8n ya trae uno nativo (`/healthz`);
  el app Next.js necesitaría un `/api/health` simple (trivial de construir, no existe
  todavía).
- Uptime Kuma hace ping periódico a esas URLs (los subdominios de cada cliente, capa 7,
  ya son públicos detrás de Caddy) y muestra un dashboard visual de arriba/abajo, con
  historial de uptime y alertas (Telegram/email) cuando algo cae.
- Esto complementa, sin reemplazar, la "Resiliencia ante caída del bot" ya definida en
  `requerimientos/07`: aquella notifica al Administrador/Líder **de ese cliente**
  específico; Uptime Kuma notifica **al operador**, de forma centralizada, sobre
  cualquier cliente.

### 2. Registro de cuentas vendidas (quién es cliente, qué contrató) → tabla simple en un Supabase centralizado, sin frontend propio todavía

- Un proyecto de Supabase **separado y centralizado** (distinto del de cada cliente),
  con una tabla básica: cliente, subdominio, fecha de alta, módulos/niveles
  contratados, estado del contrato.
- Se edita directamente desde **Supabase Studio** (su propia UI de administración) —
  sin construir un frontend a medida mientras el número de clientes sea bajo.
- **Condición de escalamiento**: el día que editar filas a mano en Studio se vuelva
  incómodo (varios clientes, necesidad de buscar/filtrar/automatizar), ahí se justifica
  construir una pantalla propia sobre esa misma tabla — no antes, siguiendo el mismo
  criterio de no construir algo que el volumen actual no necesita (ya aplicado en
  `diseno-tecnico/07` para el manejo de secretos y la actualización entre clientes).

## Qué NO se decide todavía

- No se diseña el esquema completo de esa tabla de registro de clientes (se hace
  cuando se implemente esta fase).
- No se decide aún si Uptime Kuma corre en el mismo servidor que algún cliente o en uno
  aparte dedicado solo a monitoreo.
- No se define todavía el endpoint `/api/health` del app Next.js (trivial, pero
  pendiente de construir junto con el resto del app).

## Disparador para retomar esta fase

Cuando exista más de un cliente activo simultáneamente (con un solo cliente, no hay
"flota" que monitorear de forma centralizada — el valor de este panel aparece recién
con 2 o más instancias corriendo en paralelo).
