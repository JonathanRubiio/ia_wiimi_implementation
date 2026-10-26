---
name: revision-docente-aca
description: Simula la revisión de un docente de posgrado sobre un ACA ya entregado — compara el enunciado, los criterios de aceptación y el documento generado, busca activamente hallazgos de mejora (no solo elogios), asigna una calificación desglosada por criterio con justificación, y deja un informe en entregable-final/critica-docente.md. Usar desde gestion-aca (Fase 11) o directamente cuando el usuario pida "revisar"/"criticar"/"calificar" un ACA ya entregado.
---

# Revisión docente de un ACA ya entregado

Invocada por `gestion-aca` (Fase 11) sobre un documento que ya existe. El objetivo no
es confirmar que "se ve bien" — es adoptar la postura de un evaluador independiente que
no escribió el documento y que busca activamente dónde se pierden puntos, igual que
`code-review` busca defectos reales en vez de repetir que el código "parece correcto".

## Qué leer antes de opinar (en este orden)

1. El enunciado completo (`trabajo/<enunciado>`), incluyendo cualquier "lista de
   control" o checklist literal que traiga — esa lista es la fuente de verdad
   estructural, no una sugerencia.
2. `planificacion/criterios-aceptacion.md` — la rúbrica real pegada por el usuario (y
   cualquier discrepancia que `gestion-aca` haya señalado con la ponderación del
   enunciado).
3. El documento entregable borrador **leído de verdad con la herramienta de lectura**
   (abrir el PDF/docx página por página), no solo el script que lo generó ni el
   `solucion.md` del que salió — el contenido puede divergir de lo previsto por errores
   de generación (tablas que heredan formato incorrecto, texto cortado, página de más
   o de menos).

## Cómo revisar cada criterio de la rúbrica

Para cada criterio de `criterios-aceptacion.md`, responder tres preguntas por separado
— no una impresión general:

1. **¿Qué nivel de la rúbrica alcanza *realmente* el documento** (no el que se
   aspiraba a alcanzar)? Citar la banda de puntaje tal como está redactada y decir en
   qué banda cae, con la evidencia concreta del documento que lo sustenta.
2. **¿Qué evidencia textual/estructural del documento falta o es débil** para la banda
   inmediatamente superior? Ser específico: página, sección, tabla — no "podría
   mejorar la claridad".
3. **¿Es un hallazgo corregible por IA (contenido, formato, estructura) o depende de
   una acción humana del equipo** (aportes individuales reales, ensayo de la
   sustentación oral, confirmación de un dato con el profesor)? Marcar la diferencia
   explícitamente — no se le puede pedir al siguiente paso ("aplicar mejoras") que
   resuelva lo que solo una persona real puede aportar.

## Verificación estructural (antes de la de contenido)

Revisar primero lo objetivamente verificable, porque es lo que más fácil se pasa por
alto al enfocarse en si el razonamiento "suena bien":

- Extensión exacta en páginas si el enunciado la exige (contar las páginas reales del
  documento leído, separando desarrollo de portada/referencias/anexos si el enunciado
  hace esa distinción).
- Cada anexo exigido está completo o explícitamente marcado como pendiente de una
  acción humana (nunca fabricado).
- Formato/norma exigida (ej. APA 7): fuente, interlineado, sangría, portada,
  referencias — y que ese formato no se haya "filtrado" donde no corresponde (ej.
  sangría de primera línea o interlineado doble heredado dentro de tablas, lo que las
  vuelve ilegibles).
- Las tablas son legibles: columnas con ancho proporcional al contenido, no todas del
  mismo ancho por defecto si eso genera texto apretado en una columna y vacío en otra.
- Cualquier cita o referencia académica es real y verificable (DOI o URL que de verdad
  exista) — si hay duda, marcarlo como hallazgo de máxima prioridad, no asumir que está
  bien.

## Reporte: `entregable-final/critica-docente.md`

Estructura fija:

```markdown
# Crítica docente — <Materia> / ACA <N>

- **Fecha de revisión**: <fecha>
- **Documento revisado**: trabajo/<archivo>

## Calificación por criterio

| Criterio | Nivel alcanzado | Evidencia | Qué falta para el máximo |
|---|---|---|---|

**Calificación total estimada**: X / Y puntos.

## Hallazgos (ordenados de mayor a menor impacto en la nota)

1. **[tipo: estructural | contenido | humano-pendiente] — resumen del hallazgo.**
   Evidencia concreta (página/sección). Corrección sugerida.
2. ...

## Veredicto

¿Listo para subir tal cual, o requiere los ajustes de arriba antes de entregar?
```

No incluir hallazgos genéricos de relleno solo para parecer exhaustivo ("podría
profundizar más") — si un criterio ya alcanza el nivel máximo con evidencia sólida,
decirlo y pasar al siguiente. El valor del reporte está en los hallazgos reales, no en
la cantidad de líneas.

## Aplicar mejoras (de vuelta en `gestion-aca`, Fase 12)

Esta skill no corrige el documento — solo lo audita. La corrección y regeneración del
entregable final ocurre en la Fase 12 de `gestion-aca`, tomando cada hallazgo
"corregible por IA" de este reporte uno por uno. Los hallazgos marcados como
"humano-pendiente" se trasladan tal cual al resumen de cierre para el usuario.
