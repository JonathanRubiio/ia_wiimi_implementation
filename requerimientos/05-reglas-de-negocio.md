# 5. Reglas de Negocio

## Datos obligatorios

Para que el Agente externo avance a agendar una reunión, el Prospecto debe entregar:
**correo, nombre, empresa/emprendimiento y necesidad**. Sin los 4 datos completos, no se
agenda — salvo que la Líder decida tomar el caso manualmente (ver estado
`atencion_manual`).

## Identificación y unicidad

- El **teléfono** (número de WhatsApp) y el **correo** son los identificadores naturales
  de un Prospecto/Cliente, y **ambos son únicos** en el sistema.
- Antes de crear un Prospecto nuevo, el sistema valida si el número o el correo ya
  existen. Si alguno coincide, se trata del mismo Prospecto/Cliente.
- Si el contacto recurrente trae la misma idea de desarrollo, se retoma la Oportunidad
  existente. Si trae una idea distinta, se crea una nueva Oportunidad bajo el mismo
  Prospecto.

## Asignación de casos

Solo la **Líder de área comercial** puede asignar o reasignar un caso a un Usuario
comercial. Un Usuario comercial no puede reasignar un caso a otro.

## Reintentos y estados terminales

- Rutina de abandono: tras **3 intentos** sin respuesta del cliente (reintentos cada
  24h), el caso pasa a estado `no_atiende`.
- `no_atiende` es **reactivable**: si el cliente vuelve a escribir por su cuenta, el
  sistema reactiva su estado y envía un mensaje predeterminado de reactivación antes de
  continuar el flujo normal.

## Oportunidades

No hay límite de Oportunidades activas simultáneas por Prospecto.

## Acceso al dashboard (Fase 2)

Solo **Gerencia** (puede ser más de una persona) tiene acceso, por dos vías:

1. Dashboard web tradicional, con login.
2. Agente conversacional de Gerencia (Telegram/WhatsApp): responde preguntas en lenguaje
   natural contra la base de datos compartida. Puede dar detalle de un caso puntual,
   pero solo a nivel de resumen, no a fondo.

## Parámetros configurables (por el Administrador)

- **Tiempo máximo para concretar/agendar una reunión** con el cliente antes de activar
  el aviso de fallo de agendamiento (referencia: 7–14 días).

## Estados consolidados de Prospecto / Oportunidad

```
parcial → en_proceso → no_atiende (reactivable)
                      → sin_acuerdo
                      → cerrada_ganada → el Prospecto se transforma en Cliente
```

Un caso puede, en cualquier punto, pasar a `atencion_manual` por decisión de la Líder,
momento en el cual el bot deja de actuar sobre él.
