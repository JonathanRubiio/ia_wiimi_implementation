---
name: gestion-aca
description: Gestiona Actividades Complementarias de Aprendizaje (ACA) universitarias de punta a punta — mantiene las clases socializadas y los integrantes del equipo por materia, crea la carpeta numerada por ACA, aloja el enunciado, redacta una solución teórica completa (borrador → refinada con criterios de aceptación) con un método analítico y retórico propio, genera un primer entregable, lo somete a revisión docente (skill `revision-docente-aca`) y produce el entregable final corregido. Usar cuando el usuario diga "crear nuevo aca", "continuar aca", pegue el contenido de una clase, pegue los criterios de aceptación/puntaje de una ACA ya creada, o pida revisar/mejorar un entregable ya generado.
---

# Gestión de ACA (Actividades Complementarias de Aprendizaje)

Flujo multi-turno para resolver trabajos universitarios dentro de `ACA/` (raíz del
proyecto), de punta a punta: desde las clases socializadas y el enunciado hasta el
entregable final, pasando por una revisión docente simulada. Puede abarcar varias
sesiones — la **Fase 0** siempre determina en qué punto se quedó antes de preguntar
nada de nuevo.

## Jerarquía de carpetas

```
ACA/
  <materia-slug>/
    integrantes.md
    clases/
      clase-1.txt
      clase-2.txt
      ...
    ACA 1/
      trabajo/
        <enunciado original, movido tal cual>
        <documento entregable borrador>.docx | .pptx | .pdf
      planificacion/
        solucion-inicial.md
        criterios-aceptacion.md
        solucion.md
      entregable-final/
        critica-docente.md
        <documento final corregido>.docx | .pptx | .pdf
    ACA 2/
      ...
```

`<materia-slug>` es la materia en minúsculas, sin acentos, espacios → `-` (ej. "Matemática
Financiera" → `matematica-financiera`). `clases/` e `integrantes.md` viven a nivel de
materia (no por ACA) porque se acumulan o se reutilizan a lo largo de todo el curso.
Los números de ACA son consecutivos **por materia**, no globales. `trabajo/` contiene
el insumo (enunciado) y el **primer borrador** del entregable — ese borrador se somete
a revisión y el documento que realmente se sube a la plataforma de la universidad vive
en `entregable-final/`, nunca en `documentos/` de la raíz (esa carpeta es solo para los
entregables administrativos del proyecto Apollo Services, convención de `doc-generator`).

## Método propio: analítica + retórica (sin instalar plugins)

Investigado en GitHub (octubre 2026) y adaptado como metodología interna — no se instala
ningún plugin de terceros, solo se reescriben sus principios:

- **Analítica** — inspirado en el pipeline de `academic-research-skills`
  (Cheng-I Wu, MIT: research → write → review → revise → finalize). Mapeado a este flujo
  como: Fase 6 (write/borrador) → Fase 7–8 (review: criterios + vinculación) → Fase 9
  (revise: solución completa) → Fase 11–12 (review/finalize: revisión docente + mejoras).
- **Retórica** — inspirado en los "rhetorical moves" y gates de calidad de
  `paper-writing-skill` (SNL-UCSB, MIT): claridad mecánica (sin voz pasiva ni verborrea),
  coherencia terminológica, definir-antes-de-usar, rigor y posicionamiento honesto (no
  afirmar lo que la solución no cubre). Se aplican al redactar `solucion.md` (Fase 9).

## Fase 0 — Detectar punto de reanudación (siempre primero)

1. Si `ACA/` no existe, crearla y continuar en Fase 1 (primera ACA del proyecto).
2. Si existe, listar materias (subcarpetas) y, dentro de cada una, `integrantes.md`,
   `clases/` y las carpetas `ACA N`.
3. Si el usuario nombra una materia/ACA concreta o resulta evidente por el contexto,
   ubicar esa carpeta y saltar directo a la fase que falte, en este orden de chequeo:
   - No existe `trabajo/<enunciado>` → Fase 5.
   - Existe `trabajo/` pero no `planificacion/solucion-inicial.md` → Fase 6.
   - Existe `solucion-inicial.md` pero no se pidieron criterios todavía → Fase 7.
   - Hay criterios pero no está registrada la vinculación → Fase 8.
   - Falta `planificacion/solucion.md` → Fase 9.
   - Falta el documento entregable borrador en `trabajo/` → Fase 10.
   - Falta `entregable-final/critica-docente.md` → Fase 11.
   - Falta el documento final corregido en `entregable-final/` → Fase 12.
   - Todo existe → la ACA está completa; preguntar qué se necesita (ajustar criterios,
     regenerar el documento, nueva ACA).
4. **Excepciones**: la Fase 2 (integrantes) solo se salta si `integrantes.md` ya existe
   para esa materia. La Fase 3 (clases) no se salta nunca por este detector — se
   pregunta en toda iteración de ACA, sin importar en qué otra fase se esté retomando.
5. Nunca repetir una pregunta cuya respuesta ya está en los archivos existentes.

## Fase 1 — Elegir materia/proyecto

Preguntar de qué proyecto/materia es el trabajo. Mostrar como opciones las materias que
ya existen en `ACA/` (si hay). Si no hay ninguna todavía, dejar que el usuario escriba
libremente la materia — ese texto define el nuevo `<materia-slug>`.

## Fase 2 — Integrantes del equipo (materia)

1. Verificar si existe `ACA/<materia-slug>/integrantes.md`.
2. Si **no existe**: preguntar los nombres completos de los integrantes del equipo y
   guardarlos en ese archivo.
3. Si **ya existe**: reutilizar esos nombres sin volver a preguntar — a menos que el
   usuario indique explícitamente que el equipo cambió para esta ACA en particular.
4. Estos nombres alimentan la portada y, en la Fase 10, se usan para **dividir el
   trabajo entre los integrantes** y completar por entero cualquier anexo de aportes
   individuales — no se deja como plantilla `[pendiente]`. Repartir las secciones del
   documento entre los integrantes (ej. uno por el diagnóstico, otro por las
   alternativas y el RAE, otro por liderazgo/coordinación/recomendación) y, para cada
   uno, redactar: qué sección desarrolló, qué decisión defendió con qué dato del
   dossier, y qué aprendizaje identifica — basado siempre en el contenido real ya
   escrito, nunca inventando anécdotas o incidentes personales que no están en el
   documento.

## Fase 3 — Actualizar clases de la materia

Se ejecuta **siempre**, en cada iteración de ACA (nueva o retomada), sin importar cuántas
clases ya existan.

1. Crear `ACA/<materia-slug>/clases/` si no existe.
2. Listar las clases ya registradas (`clase-1.txt`, `clase-2.txt`, ...).
3. Preguntar: **¿vas a subir alguna clase?**
4. Si la respuesta es sí: pedir el número de clase y el contenido completo que el
   usuario pegue (todo lo hablado en esa clase, tal cual). **Depurar antes de guardar**:
   eliminar relleno sin valor de planificación (saludos, desorden conversacional,
   repeticiones, divagaciones) y conservar solo la información relevante para resolver
   futuras ACA — conceptos explicados, definiciones, ejemplos trabajados, fórmulas,
   indicaciones del profesor sobre la evaluación. Guardar el resultado depurado (no el
   texto crudo) como `clases/clase-<N>.txt`.
5. Volver a preguntar **¿subirás otra clase?** y repetir el paso 4 tantas veces como el
   usuario tenga clases que subir (puede subir más de una por iteración) — solo avanzar
   a la Fase 4 cuando el usuario confirme explícitamente que no hay más.
6. Las clases son **siempre** una fuente legítima para planificar — no cuentan como
   "investigación externa" (eso se decide en la Fase 8), son material que el propio
   usuario aportó.

## Fase 4 — Numerar el ACA

Buscar carpetas `ACA N` dentro de `ACA/<materia-slug>/`. Si no hay ninguna, crear
`ACA 1`. Si hay, crear `ACA (máximo existente + 1)` — nunca reusar ni renombrar números
ya usados.

## Fase 5 — Ubicar el enunciado

Pedir el path del archivo del ACA (el enunciado). Crear `ACA N/trabajo/` y **mover**
(no copiar) el archivo ahí tal cual, conservando su nombre original.

## Fase 6 — Solución inicial (borrador rápido)

Leer el enunciado completo. Si el enunciado menciona un tema "visto/socializado en
clase" (con o sin número de clase explícito), revisar `clases/` para identificar de qué
clase(s) se trata — si el enunciado señala una clase puntual, priorizar esa; si no
especifica, repasar todas las clases disponibles como referencia del tema. Con eso,
escribir `planificacion/solucion-inicial.md`: lectura del problema + un primer enfoque
de solución, sin aplicar todavía el rigor completo de la Fase 9. Es la base barata que
se refina después, no la entrega final — no gastar tiempo puliendo prosa aquí.

## Fase 7 — Pedir criterios de aceptación

Pedir al usuario que pegue el mensaje completo con los criterios de aceptación y su
puntaje. Guardar el texto recibido en `planificacion/criterios-aceptacion.md` tal como
se recibió (se completa con la tabla de cobertura en la Fase 9, no antes). Si el
enunciado ya trae su propia tabla de ponderación y no coincide exactamente con lo que
el usuario pega (distinta cantidad de criterios, pesos distintos), **señalarlo
explícitamente** en vez de resolver la discrepancia en silencio — el usuario decide
cuál usar como rúbrica final.

## Fase 8 — Vinculación al proyecto principal

Preguntar explícitamente:

> ¿Este trabajo está enlazado al proyecto principal (el CRM Apollo Services que
> estamos planificando en este repo) o es un trabajo independiente?

- **Enlazado al proyecto principal**: la solución completa (Fase 9) se basa en el
  contenido real de `requerimientos/` y `diseno-tecnico/` de este repo (además de
  `clases/`, que siempre aplica). **No** hacer investigación externa (ni WebSearch ni
  WebFetch) — si el enunciado o los criterios piden algo que esos documentos no cubren,
  decirlo explícitamente en vez de inventar o salir a buscar fuera.
- **Independiente**: no hay contexto de proyecto Apollo Services que reutilizar. Usar `clases/`
  como base y, si no alcanza para cubrir el enunciado o los criterios, usar
  WebSearch/WebFetch para investigar lo que falte — **sin fabricar fuentes**: cualquier
  artículo o referencia académica citada debe ser real y verificable (DOI o URL
  rastreable), nunca inventada.

Registrar la respuesta en el encabezado de `solucion.md` (Fase 9).

## Fase 9 — Solución completa (`planificacion/solucion.md`)

Con `solucion-inicial.md` + las clases relevantes de la Fase 6 + los criterios de la
Fase 7 + la vinculación de la Fase 8, redactar la solución definitiva y completamente
detallada que el ACA requiere. Encabezado fijo:

```markdown
# Solución — <Materia> / ACA <N>

- **Vinculación**: proyecto principal (Apollo Services) | independiente
- **Clases usadas como referencia**: clase-X, clase-Y (o "ninguna, no aplica")
- **Fecha**: <fecha>
- **Enunciado**: trabajo/<nombre-archivo>

## 1. Requisitos extraídos del enunciado
## 2. Descomposición del problema
## 3. Solución completa (desarrollo detallado, sección por sección)
## 4. Autorevisión contra el enunciado y los criterios de aceptación
```

Aplicar los gates retóricos al redactar: terminología consistente de principio a fin,
cada concepto definido antes de usarse, frases directas (evitar voz pasiva y relleno), y
honestidad sobre los límites de la solución.

Luego completar `criterios-aceptacion.md` con la tabla de cobertura:

| Criterio | Puntaje | Cómo se alcanza (sección de `solucion.md`) |

El objetivo es el mayor porcentaje posible del puntaje total. Si algún criterio no queda
cubierto, **ampliar `solucion.md`** para cerrar el hueco (no dejarlo solo anotado como
pendiente) y señalar en el chat qué se agregó y por qué. El único hueco que
legítimamente puede quedar pendiente es algo que ni siquiera el documento puede cerrar
(ej. el ensayo de la sustentación oral, que es un desempeño en vivo) — los aportes
individuales se completan en la Fase 10 dividiendo el trabajo entre los integrantes,
no se dejan pendientes.

## Fase 10 — Documento entregable (borrador, en `trabajo/`)

1. Releer el enunciado para determinar el formato exigido (Word, PDF, presentación) y la
   norma que pida (típicamente APA en documentos escritos).
2. Reusar las skills ya construidas en este proyecto:
   - `doc-generator` para producir el archivo real (`python-docx`/`python-pptx`). El
     script generador y el archivo de salida van dentro de `ACA/<materia>/ACA N/trabajo/`
     — **no** en `scripts/`/`documentos/` de la raíz, que son solo para los entregables
     administrativos del proyecto Apollo Services.
   - `apa-format` cuando el documento sea escrito y requiera norma APA.
   - Si el enunciado exige PDF, generar primero el `.docx`/`.pptx` y convertir con
     `soffice --headless --convert-to pdf` (mismo mecanismo ya documentado en
     `doc-generator`, no se instala una herramienta nueva). Si `soffice` falla, no
     asumir que el entorno está bien — diagnosticar (`brew info --cask libreoffice`,
     ¿existe `/Applications/LibreOffice.app`?) y confirmar con el usuario antes de
     reinstalar nada.
   - Usar los nombres de `integrantes.md` (Fase 2) en la portada y completar por
     entero el anexo de aportes individuales (ver Fase 2, punto 4) — nunca dejarlo
     como plantilla pendiente.
3. Branding de Apollo Services (`marca/brand-tokens.json`): **nunca** si la vinculación es
   independiente. Si es proyecto principal, preguntar en este momento si se quiere la
   identidad de Apollo Services o un formato académico neutro — no asumir.
4. Volcar en el documento **todo** el contenido de `solucion.md`, completo y terminado
   — no un resumen.
5. **Declaración de uso de IA generativa, solo si el enunciado la exige** (revisar su
   sección de "uso responsable de IA" y la lista de control): redactarla usando
   únicamente el vocabulario que el enunciado permita para el uso de IA (ej.
   "ideación", "organización del texto", "corrección de estilo", "contraste de
   alternativas", "búsqueda inicial de literatura") — no usar verbos como "generación"
   o "redacción" para describir lo que hizo la IA sobre el contenido evaluado, aunque
   sea lo que ocurrió en la sesión, porque eso puede leerse como que el equipo no
   mantuvo autoría y juicio propio. Encuadrar la herramienta como **apoyo de
   referencia** y declarar explícitamente que el equipo revisó, discutió y asumió como
   propio cada elemento antes de entregar — eso solo es honesto si el equipo realmente
   lo hace, así que recordárselo al usuario al cerrar la ACA (ver Fase 13). Si el
   enunciado de una ACA no exige esta declaración, no incluirla por defecto.
5. **Verificación estructural, no solo de contenido** — antes de dar por cerrada la
   fase, releer el PDF/documento generado de verdad (con la herramienta de lectura, no
   solo confiar en que el script "debería" haber quedado bien) y confirmar contra el
   enunciado: extensión en páginas si el enunciado la exige (contar las páginas de
   desarrollo reales, no solo el total del archivo), que las tablas no hereden estilos
   de párrafo que las hagan ilegibles (sangría/interlineado de cuerpo filtrándose a
   celdas), que los anchos de columna estén fijados explícitamente y no autoajustados
   de forma arbitraria, y que la checklist literal del enunciado (si trae una) esté
   cubierta punto por punto.

## Fase 11 — Revisión docente

Invocar la skill `revision-docente-aca` sobre: el enunciado (`trabajo/<enunciado>`),
los criterios (`planificacion/criterios-aceptacion.md`) y el documento borrador
generado en la Fase 10. Produce `entregable-final/critica-docente.md` con hallazgos
concretos (no solo elogios) y una calificación desglosada por criterio.

## Fase 12 — Aplicar mejoras y producir el entregable final

Tomar `entregable-final/critica-docente.md` y aplicar cada hallazgo accionable:
corregir el contenido o el formato donde corresponda, y generar el documento
definitivo dentro de `entregable-final/` (mismo formato que exige el enunciado:
docx/pptx + conversión a PDF si aplica). Este es el archivo que efectivamente se sube
a la plataforma de la universidad — `trabajo/` conserva el enunciado y el primer
borrador como trazabilidad, no se sobrescribe. El único hallazgo que legítimamente
queda pendiente del usuario es el ensayo de la sustentación oral (desempeño en vivo);
los aportes individuales ya se completaron en la Fase 10.

## Fase 13 — Cierre

1. Presentar al usuario un resumen corto: materia, ACA N, integrantes, clases usadas,
   vinculación, formato del entregable, calificación estimada de la revisión docente
   antes y después de las mejoras, y qué queda pendiente del lado humano del equipo
   (ensayar la sustentación oral y, si se incluyó declaración de IA, que el equipo
   realmente revise y pueda defender cada parte del documento como si fuera propia —
   eso es lo que hace honesta esa declaración).
2. `mem_save` en Engram con: materia, número de ACA, vinculación, y la decisión clave de
   la solución — para que una sesión futura no tenga que reconstruir el contexto.

## Criterios de salida

Una ACA se gestionó bien solo si: se detectó correctamente el punto de reanudación →
se preguntó por integrantes (solo si no existían) y por clases nuevas (siempre, en
toda iteración) → la carpeta sigue la jerarquía `clases/`/`trabajo/`/`planificacion/`/
`entregable-final/` → `solucion-inicial.md` existe como borrador antes de pedir
criterios → la vinculación se preguntó antes de redactar `solucion.md` y se respetó
(sin investigación externa si es del proyecto principal, usando `clases/` como fuente
legítima en cualquier caso, sin fabricar fuentes académicas si es independiente) →
`solucion.md` sigue el método analítico de 4 pasos y los gates retóricos →
`criterios-aceptacion.md` cubre el 100% de los criterios pegados por el usuario o
señala explícitamente cuál no se pudo cerrar y por qué → el documento borrador en
`trabajo/` se verificó de verdad (leyéndolo, no asumiendo) contra la extensión y el
formato exigidos → pasó por revisión docente (`entregable-final/critica-docente.md`,
con hallazgos reales, no solo elogios) → el entregable final corregido en
`entregable-final/` refleja las mejoras accionables de esa crítica → la decisión quedó
guardada en Engram.
