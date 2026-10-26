---
name: branding
description: Define y mantiene la identidad de marca del producto (paleta de colores, tipografía, tono de voz, brief de logo) en marca/brand.md y marca/brand-tokens.json — fuente única de verdad que consume doc-generator para aplicar colores/fuentes a los documentos generados. Usar antes de doc-generator cuando aún no exista marca/, o cuando se pida crear/ajustar la identidad visual del producto.
---

# Identidad de marca

## Límite real de capacidad (decirlo siempre, no prometer de más)

No se puede generar artwork/ilustración rasterizada (un logo ilustrativo complejo como
imagen PNG/JPG). Lo que sí es posible y se entrega con esta skill:

- Una **paleta de colores completa y validada** (no solo "elige un color bonito" — ver
  metodología abajo).
- Un **sistema tipográfico** (familia de fuentes, pesos, jerarquía).
- Un **wordmark o ícono geométrico simple en SVG** (código vectorial real, no una
  imagen generada) — válido para una identidad minimalista, no para un logo
  ilustrativo/mascota.
- Un **brief de logo** completo y específico, listo para pasarle a un diseñador o a una
  herramienta generadora de imágenes (Midjourney, un diseñador freelance, etc.) si se
  quiere algo más elaborado que el SVG.

## Metodología de paleta de colores

Reutilizar la metodología ya validada en la skill `dataviz` de este entorno (fórmula de
color con validador, ver `references/palette.md` de esa skill) en vez de improvisar
colores al ojo — define tonos con contraste accesible (WCAG AA) y una paleta coherente
(color primario, secundario, de acento, neutros, y variantes para modo claro/oscuro).
No reinventar la teoría de color desde cero cuando ya existe una metodología probada en
este mismo entorno.

## Qué preguntar antes de definir la marca (si no está ya decidido)

1. ¿El tono de marca es más corporativo/serio o más cercano/informal? (afecta tipografía
   y tono de voz en `brand.md`).
2. ¿Hay algún color que el usuario ya asocie con el producto o quiera evitar?
3. El nombre comercial del producto es **Apollo Services** — usarlo en todos los
   documentos de marca (el repo de GitHub se llama `ia_apollo_services_implementation`,
   que es solo el identificador interno, no el nombre comercial en sí).

## Artefactos que produce

- **`marca/brand.md`**: paleta con sus usos (primario/secundario/acento/neutros),
  tipografía (encabezados/cuerpo), tono de voz con 3-4 ejemplos de frases "así sí /
  así no", y el brief de logo en texto.
- **`marca/brand-tokens.json`**: los mismos colores/fuentes en formato máquina-legible,
  para que `doc-generator` los lea directo sin tener que parsear el markdown:
  ```json
  {
    "colores": { "primario": "#______", "secundario": "#______", "acento": "#______", "texto": "#______", "fondo": "#______" },
    "tipografia": { "encabezados": "____", "cuerpo": "____" }
  }
  ```
- **`marca/logo.svg`** (si se construye el wordmark/ícono simple): código SVG directo,
  usando los colores de `brand-tokens.json`.

## Aplicación

Una vez que `marca/brand-tokens.json` existe, **no se vuelve a improvisar un color**
en ningún documento generado — `doc-generator` siempre lee este archivo primero.
