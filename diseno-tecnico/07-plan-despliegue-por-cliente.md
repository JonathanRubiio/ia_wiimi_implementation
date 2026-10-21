# 7. Plan de Despliegue por Cliente

> Qué significa en concreto "duplicar la infraestructura" (capa 7 de requerimientos:
> no es multi-tenant compartido, cada organización tiene su propia instancia).

## Qué corre por cada cliente

Un solo stack de Docker Compose, con 3 servicios + sus dependencias:

```
infra/docker-compose.yml
├── supabase (Postgres + Realtime + Auth + Storage + Studio)   — docker-compose oficial de Supabase
├── n8n                                                          — motor de orquestación
└── app (Next.js: M1 bandeja, M5 dashboard, Panel Administrativo)
```

**Decisión: todo contenedorizado junto, no repartido entre varios proveedores SaaS**
(ej. Vercel para el app + Supabase Cloud para la BD). Un solo `docker-compose` por
cliente, desplegable en un único servidor (VPS), es más simple de reproducir, versionar
y dar de baja que coordinar cuentas en 3 plataformas distintas por cada cliente nuevo.

## Red y dominios

- Un **reverse proxy con Caddy** (no Traefik) delante de todos los stacks del servidor —
  se eligió Caddy por su configuración mínima (un `Caddyfile` de pocas líneas) y TLS
  automático vía Let's Encrypt, priorizando velocidad de operación para un solo dev.
- Cada cliente recibe subdominios propios: `cliente1.midominio.com` (app),
  `cliente1-n8n.midominio.com` (n8n, acceso solo del Administrador/dueño del producto).
- Varios clientes pueden convivir en un mismo servidor físico mientras el volumen lo
  permita (~100 prospectos/mes por cliente, capa 7) — no hace falta un servidor por
  cliente desde el día uno, solo un **stack Docker aislado** por cliente.

## Variables de entorno y secretos por instancia

| Servicio | Variables clave |
|---|---|
| Supabase | `POSTGRES_PASSWORD`, `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY` (las 3 últimas se generan con el script oficial de Supabase a partir del `JWT_SECRET`, únicas por instancia) |
| n8n | `N8N_ENCRYPTION_KEY`, credenciales de Claude, Gemini, WhatsApp/360dialog, Instagram/Facebook Graph API, Google Calendar OAuth (client id/secret + refresh token por organización), Telegram Bot Token |
| App | `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (apuntando al Supabase de ese cliente) |

**Manejo de secretos**: un archivo `.env.<cliente>` por instancia, generado a partir de
`infra/.env.example`, **nunca commiteado** (gitignored). Dado el volumen actual (pocos
clientes, un solo operador), no se introduce un gestor de secretos externo todavía —
se revisita si el número de clientes crece lo suficiente para que el manejo manual de
archivos `.env` se vuelva un riesgo real.

## Checklist de alta de un cliente nuevo (`infra/alta-cliente-nuevo.md`)

1. Copiar `infra/docker-compose.yml` + `.env.example` → `.env.<cliente>`.
2. Generar `JWT_SECRET`/`ANON_KEY`/`SERVICE_ROLE_KEY` con el script oficial de Supabase.
3. `docker compose --env-file .env.<cliente> up -d`.
4. Aplicar el esquema: correr las migraciones de `supabase/migrations/` (doc 02) contra
   la instancia nueva.
5. Ejecutar `supabase/seed.sql`: crea la fila única de `organizacion`, activa en
   `niveles_modulo` solo los módulos/niveles que ese cliente contrató, y da de alta al
   primer usuario `administrador`.
6. Importar los 5 workflows de `n8n/*.json` (doc 06) a la instancia de n8n del cliente,
   y cargar ahí las credenciales de los canales que contrató (WhatsApp, Instagram,
   Facebook, Telegram, Calendar).
7. Registrar esos mismos canales en la tabla `canal` (vía Panel Administrativo o seed).
8. Configurar el subdominio del cliente en el `Caddyfile` del servidor.
9. **Prueba de humo**: enviar un mensaje de WhatsApp de prueba y confirmar que M2
   responde, clasifica, y el registro aparece en `contacto`/`seguidor` o `prospecto`.

## Qué pasa cuando se actualiza el producto (nueva versión de un workflow, del esquema, o de un prompt)

No hay actualización automática entre clientes — cada stack es independiente. El
proceso es: probar el cambio en una instancia de staging propia, y luego repetir el
mismo cambio (nueva migración de `supabase/migrations/`, nuevo JSON de workflow,
prompt actualizado) manualmente en cada cliente activo. A este volumen (pocos clientes)
es manejable; si el número de clientes crece lo suficiente para que esto se vuelva
pesado, el siguiente paso sería automatizar este rollout (ej. un script que itere sobre
todos los `.env.<cliente>` conocidos) — no se resuelve ahora por no construir algo que
todavía no hace falta.
