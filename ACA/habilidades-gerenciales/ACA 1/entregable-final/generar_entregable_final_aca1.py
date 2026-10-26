"""Entregable final del ACA 1 (Habilidades Gerenciales), tras la revision docente.
Corrige respecto al borrador de ../trabajo/generar_informe_aca1.py:
  1. Alternativa 3 (Responsabilidad) ampliada - la justificacion era mas breve que
     las otras dos alternativas.
  2. Movimiento "Nombrar" del guion reducido a un solo hecho (el guion unico se
     aplico igual en las 12 tiendas); el resultado especifico de la tienda de Luis
     se menciona en "Indagar".
Fuente: ../planificacion/solucion.md + ../entregable-final/critica-docente.md
Salida: ACA1_Informe_Mercado_Barrio_B1_FINAL.docx y su .pdf
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(OUT_DIR, "ACA1_Informe_Mercado_Barrio_B1_FINAL.docx")

INTEGRANTES = [
    "Jhoan Jesus Cardozo Gelvis",
    "Jonathan Adonay Rubio Jimenez",
    "Ivan Dario Zarate Rincon",
]

doc = Document()

section = doc.sections[0]
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(2.54)
section.right_margin = Cm(2.54)

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.paragraph_format.line_spacing = 2.0
normal.paragraph_format.first_line_indent = Cm(1.27)
normal.paragraph_format.space_after = Pt(0)

h1 = doc.styles["Heading 1"]
h1.font.name = "Times New Roman"
h1.font.size = Pt(12)
h1.font.bold = True
h1.font.color.rgb = RGBColor(0, 0, 0)
h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
h1.paragraph_format.space_before = Pt(12)
h1.paragraph_format.space_after = Pt(6)
h1.paragraph_format.first_line_indent = Cm(0)

h2 = doc.styles["Heading 2"]
h2.font.name = "Times New Roman"
h2.font.size = Pt(12)
h2.font.bold = True
h2.font.color.rgb = RGBColor(0, 0, 0)
h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
h2.paragraph_format.space_before = Pt(10)
h2.paragraph_format.space_after = Pt(4)
h2.paragraph_format.first_line_indent = Cm(0)


def add_page_number_field(paragraph):
    run = paragraph.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.text = "PAGE"
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)


header = section.header
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hp.paragraph_format.first_line_indent = Cm(0)
add_page_number_field(hp)


def p(text="", bold=False, italic=False, align=None, indent0=False):
    para = doc.add_paragraph()
    if indent0:
        para.paragraph_format.first_line_indent = Cm(0)
    if align is not None:
        para.paragraph_format.alignment = align
    if text:
        run = para.add_run(text)
        run.bold = bold
        run.italic = italic
    return para


def _reset_cell_paragraph(cell_paragraph):
    cell_paragraph.paragraph_format.first_line_indent = Cm(0)
    cell_paragraph.paragraph_format.left_indent = Cm(0)
    cell_paragraph.paragraph_format.line_spacing = 1.0
    cell_paragraph.paragraph_format.space_after = Pt(2)
    cell_paragraph.paragraph_format.space_before = Pt(2)


def make_table(headers, rows, col_widths_cm=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Light Grid Accent 1"
    t.autofit = False
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        para = hdr[i].paragraphs[0]
        _reset_cell_paragraph(para)
        run = para.add_run(h)
        run.bold = True
        run.font.size = Pt(10)
        run.font.name = "Times New Roman"
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            para = cells[i].paragraphs[0]
            _reset_cell_paragraph(para)
            run = para.add_run(val)
            run.font.size = Pt(10)
            run.font.name = "Times New Roman"
    if col_widths_cm:
        for row in t.rows:
            for i, w in enumerate(col_widths_cm):
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


# ---------------------------------------------------------------------------
# PORTADA
# ---------------------------------------------------------------------------
for _ in range(4):
    p()
p("ACA 1 — Habilidades Gerenciales", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("Caso B: Mercado Barrio+ · Tarjeta de enfoque B1 — Comunicación", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p()
p("Especialización en Gobernanza de la Inteligencia Artificial", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("Cohorte 26ES5", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p()
for nombre in INTEGRANTES:
    p(nombre, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p()
p("Docente: Carlos Andrés Piraquive Cifuentes", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("1 de noviembre de 2026", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
doc.add_page_break()

# ---------------------------------------------------------------------------
# 1. COMPRENDER EL CASO Y FORMULAR EL PROBLEMA
# ---------------------------------------------------------------------------
doc.add_heading("1. Comprender el caso y formular el problema", level=1)

p(
    "El caso asignado al equipo es el Caso B (Mercado Barrio+), con la tarjeta de "
    "enfoque B1 — Comunicación: una tienda reportó que el guion único de atención "
    "redujo las conversaciones espontáneas con los clientes, mientras otras dos lo "
    "consideran útil."
)

p(
    "Este análisis sigue el marco de diagnosticar–conducir–intervenir visto en el "
    "curso: primero se diagnostica separando hechos de interpretaciones (esta "
    "sección), luego se conduce la conversación con quienes están en tensión "
    "(sección 3) y finalmente se interviene con una decisión gerencial concreta "
    "(sección 5). La separación entre hecho, apreciación, emoción y conducta aplica "
    "el modelo de apreciación de Lázarus: el hecho es lo que ocurrió objetivamente, "
    "la apreciación es el filtro subjetivo con el que cada persona lo interpreta, y "
    "de ese filtro surge la emoción y la conducta — por eso la misma política "
    "(guion único) puede leerse como una imposición en una tienda y como una ayuda "
    "en otra."
)

doc.add_heading("Hechos elegidos y su naturaleza", level=2)
make_table(
    ["ID", "Hecho", "Naturaleza"],
    [
        ["B-F1", "Clara (gerente comercial) pide que todas las tiendas sigan el "
                 "mismo guion de atención desde el lunes.", "Documentado"],
        ["B-F2", "Luis (encargado de tienda) responde que su barrio no se parece a "
                 "los demás y que la gente viene a conversar, no a escuchar un "
                 "libreto.", "Documentado"],
        ["Tarjeta B1", "Una tienda reportó que el guion único redujo las "
                 "conversaciones espontáneas; otras dos lo consideran útil.",
                 "Documentado, con vacío de información"],
        ["B-F7", "No existe un criterio común para seleccionar pruebas pequeñas ni "
                 "una rutina acordada para compartir aprendizajes entre tiendas.",
                 "Vacío de información"],
        ["B-F6", "Una colaboradora de tienda declara: “cuando sugiero algo, me "
                 "piden resultados, pero no me dejan probarlo”.", "Testimonio"],
    ],
    col_widths_cm=[2.5, 10.0, 3.5],
)

doc.add_heading("Problema central", level=2)
p(
    "Mercado Barrio+ generalizó un guion único de atención a las 12 tiendas sin "
    "escuchar antes que su efecto varía según el contexto de cada barrio — reduce "
    "las conversaciones espontáneas en al menos una tienda y resulta útil en otras — "
    "y no existe ningún canal para que esa diversidad de resultados se discuta antes "
    "de decidir mantenerlo, ajustarlo o diferenciarlo."
)

doc.add_heading("Matriz hecho → apreciación → emoción → conducta (hipótesis, no diagnóstico clínico)", level=2)
make_table(
    ["Actor", "Hecho", "Apreciación (hipótesis)", "Emoción (hipótesis)", "Conducta observable"],
    [
        ["Luis (tienda donde bajó la conversación)", "Debe aplicar el mismo guion "
         "que las otras 11 tiendas.",
         "Podría interpretar que el guion ignora que en su barrio la gente viene a "
         "conversar.",
         "Posible frustración por sentir que su contexto no cuenta.",
         "Cuestiona abiertamente el guion en la reunión (B-F2)."],
        ["Encargado de tienda donde el guion es útil", "Debe aplicar el mismo "
         "guion que Luis.",
         "Podría interpretar el guion como una estructura que facilita atender sin "
         "improvisar.",
         "Posible alivio por tener un criterio claro.",
         "Lo aplica sin objeciones; probablemente lo defendería en una reunión "
         "conjunta."],
    ],
    col_widths_cm=[3.3, 3.2, 3.8, 3.0, 3.5],
)

# ---------------------------------------------------------------------------
# 2. REENCUADRAR Y GENERAR ALTERNATIVAS
# ---------------------------------------------------------------------------
doc.add_heading("2. Reencuadrar y generar alternativas", level=1)

p(
    "Pregunta de reencuadre: ¿cómo podríamos comunicarnos con los clientes de forma "
    "consistente en toda la cadena, sin imponer un guion idéntico que no funciona "
    "igual en todos los contextos?"
)

p(
    "Las tres alternativas se comparan con cuatro filtros de creatividad "
    "estratégica vistos en el curso: valor (¿a quién le mejora algo?), alineación "
    "(¿por qué esta alternativa y no otra, dado el encargo de escuchar la "
    "diversidad entre tiendas?), viabilidad (¿se puede ejecutar con lo que la "
    "dirección ya autorizó, sin app, descuentos ni personal nuevo?) y "
    "responsabilidad (¿qué puede salir mal y quién debe gestionarlo?)."
)

doc.add_heading("Tres alternativas comparadas", level=2)
make_table(
    ["Alternativa", "Valor", "Alineación", "Viabilidad", "Responsabilidad"],
    [
        ["1. Piso común + espacio local",
         "Alto: resuelve directamente B-F1/B-F2 sin perder identidad de marca.",
         "Alta: responde al encargo de escucha y diversidad.",
         "Alta: sin personal, tecnología ni presupuesto adicional.",
         "Exige acordar quién define los 2-3 elementos del piso común y qué pasa "
         "si una tienda se desvía más allá de lo acordado."],
        ["2. Canal de retroalimentación entre tiendas",
         "Alto para la sostenibilidad de cualquier decisión futura — resuelve "
         "B-F7.",
         "Alta: habilita decidir con evidencia, no solo con intuición.",
         "Alta: sin personal ni presupuesto adicional.",
         "Exige disciplina de seguimiento para que no se vuelva un espacio solo "
         "enunciativo (se recoge información pero nunca se actúa)."],
        ["3. Segmentar el guion por tipo de tienda",
         "Alto: ataca la causa raíz (uniformidad forzada).",
         "Alta.",
         "Media: requiere evidencia confiable de qué variante aplica a cada "
         "tienda, que hoy no existe.",
         "Exige definir quién valida cada variante del guion, con qué datos del "
         "canal de retroalimentación se construye cada una, y qué pasa si una "
         "tienda queda mal clasificada y recibe la variante que no le "
         "corresponde — es la alternativa con más trabajo de diseño inicial de "
         "las tres."],
    ],
    col_widths_cm=[3.3, 3.2, 3.0, 2.8, 4.2],
)

p(
    "Se elige la Alternativa 1 como eje inmediato de la recomendación gerencial "
    "(sección 5). La Alternativa 2 no se descarta: se absorbe como mecanismo "
    "habilitante (sección 4) — sin un canal para que las tiendas reporten qué "
    "funciona, cualquier ajuste al guion corre el riesgo de repetir el patrón que ya "
    "tuvo la propuesta de B-F3: quedar sin discutir. La Alternativa 3 se pospone, no "
    "se descarta: es una evolución natural de la Alternativa 1 una vez que la "
    "Alternativa 2 aporte evidencia suficiente — intentarla ahora sería adivinar."
)

# ---------------------------------------------------------------------------
# 3. EJERCER LIDERAZGO Y CONVERSAR
# ---------------------------------------------------------------------------
doc.add_heading("3. Ejercer liderazgo y conversar", level=1)

p(
    "La conducta de liderazgo que empeora el caso es que Clara generalizó el guion "
    "a las 12 tiendas sin escuchar o medir antes cómo varía su efecto entre "
    "tiendas — no hubo piloto ni consulta previa, y cuando Luis objeta (B-F2), no "
    "hay evidencia de que su observación se haya tomado como un dato válido sobre su "
    "contexto, en vez de como resistencia personal."
)

p(
    "La práctica de liderazgo propuesta es escuchar primero cómo varía el tipo de "
    "encuentro de servicio entre tiendas antes de generalizar un cambio de proceso "
    "de atención. Esto tiene respaldo empírico (ver Anexo 1): Victorino, Verma y "
    "Wardell (2013) encontraron que un guion verbal alto no afecta la calidad "
    "percibida en encuentros estandarizados, pero sí la afecta negativamente en "
    "encuentros personalizados. La tienda de Luis, donde “la gente viene a "
    "conversar”, corresponde a un encuentro más personalizado — justo el tipo de "
    "situación donde el guion único causa más daño."
)

doc.add_heading("Guion de conversación difícil (cuatro movimientos)", level=2)
for n, texto in [
    ("Nombrar", "“Noto que desde el lunes todas las tiendas deben seguir el mismo "
                "guion de atención.”"),
    ("Indagar", "“¿Qué información tenías sobre cómo varía la atención entre "
                "tiendas antes de decidir un guion único para todas? Pregunto "
                "porque tu tienda reportó menos conversación espontánea con los "
                "clientes desde que se aplicó.”"),
    ("Reencuadrar", "“El objetivo no es que las 12 tiendas digan exactamente lo "
                     "mismo, sino que cada cliente sienta una atención consistente "
                     "y útil — en tu tienda eso puede requerir más espacio para la "
                     "conversación, no un libreto idéntico al de otra tienda donde "
                     "sí funciona bien.”"),
    ("Acordar", "“Clara circula antes del 29 de octubre los 2-3 elementos mínimos "
                "del guion (piso común), y Luis y los demás encargados definen el "
                "resto según su contexto; se revisa cómo funcionó en la reunión "
                "mensual siguiente.”"),
]:
    para = p()
    r = para.add_run(f"{n}: ")
    r.bold = True
    para.add_run(texto)

p(
    "El movimiento de nombrar describe un único hecho verificable (que el guion se "
    "aplicó igual en las 12 tiendas), no una intención ni un juicio sobre Clara — "
    "esa es la asertividad. El movimiento de indagar asume que Clara tenía una "
    "razón legítima para buscar consistencia, y pregunta por la información con la "
    "que contaba en vez de acusarla de no haber consultado — esa es la empatía: no "
    "se descarta su objetivo, se amplía la forma de lograrlo."
)

# ---------------------------------------------------------------------------
# 4. COORDINAR AL EQUIPO
# ---------------------------------------------------------------------------
doc.add_heading("4. Coordinar al equipo", level=1)

make_table(
    ["Acuerdo", "Responsable", "Acción", "Plazo", "Evidencia"],
    [
        ["(a) Cómo se toman o escalan decisiones", "Clara + encargados de tienda",
         "El piso común lo define Clara con aporte de los encargados; los ajustes "
         "de una sola tienda los decide directamente su encargado, sin escalar.",
         "A partir de noviembre.",
         "Documento breve con el piso común acordado, circulado a las 12 tiendas."],
        ["(b) Cómo se expresan desacuerdos sin penalizar",
         "Responsable de operaciones + encargados de tienda",
         "Punto fijo de agenda en la reunión mensual: cada tienda reporta qué del "
         "guion funcionó y qué no, sin que eso se interprete como incumplimiento.",
         "Reunión mensual de noviembre; revisión en la siguiente.",
         "Registro de reportes por tienda y de los ajustes decididos a partir de "
         "ellos."],
    ],
    col_widths_cm=[3.2, 3.0, 4.3, 2.5, 3.5],
)

# ---------------------------------------------------------------------------
# 5. EMITIR UNA RECOMENDACIÓN GERENCIAL
# ---------------------------------------------------------------------------
doc.add_heading("5. Emitir una recomendación gerencial", level=1)

p(
    "Decisión principal: implementar la Alternativa 1 (piso común + espacio "
    "local), sostenida por el mecanismo de la Alternativa 2 (canal de "
    "retroalimentación entre tiendas, sección 4) para decidir con evidencia real si "
    "conviene avanzar hacia la Alternativa 3 (segmentación por contexto) en una "
    "fase posterior."
)

doc.add_heading("Acciones priorizadas (30-90 días)", level=2)
make_table(
    ["Acción", "Responsable", "Fecha", "Indicador", "Riesgo humano/ético"],
    [
        ["1. Definir e implementar el piso común",
         "Clara + 12 encargados de tienda",
         "Definición antes del día 15; implementación antes del día 30; revisión "
         "al día 60.",
         "Nivel de conversación espontánea reportado (antes/después) en la tienda "
         "de Luis y en las dos tiendas que consideraban útil el guion.",
         "Que “espacio local” se use para no cambiar nada, o se perciba como "
         "falta de dirección — se mitiga con el piso común obligatorio y la "
         "revisión mensual."],
        ["2. Activar el canal de retroalimentación entre tiendas",
         "Responsable de operaciones",
         "Primera sesión en reunión de noviembre; evaluación al día 90.",
         "N.º de tiendas que reportan y N.º de ajustes decididos a partir de los "
         "reportes.",
         "Que el canal se vuelva un espacio solo para quejarse sin consecuencia — "
         "se mitiga exigiendo una decisión explícita en cada reunión."],
    ],
    col_widths_cm=[3.5, 2.8, 3.0, 3.3, 3.9],
)

p(
    "Experimento pequeño, sin prometer resultados no medidos: comparar durante 60 "
    "días el nivel reportado de conversación espontánea en la tienda de Luis antes "
    "y después del piso común — sin asumir de antemano que volverá al nivel previo "
    "al guion único, porque todavía no se sabe cuánto de esa reducción se debe al "
    "guion en sí y cuánto a otros factores no documentados en el dossier."
)

p(
    "Qué se profundizaría en el ACA 2: cómo conducir la conversación si, tras la "
    "primera revisión, Clara prefiere volver al guion único argumentando "
    "consistencia de marca sobre las otras 11 tiendas; y cómo decidir, con la "
    "evidencia del canal de retroalimentación, si conviene construir las variantes "
    "de guion de la Alternativa 3 o si el piso común por sí solo es suficiente."
)

p(
    "Gobernanza del piloto: el responsable de operaciones revisa los dos "
    "indicadores (conversación espontánea y reportes del canal) en la misma "
    "reunión mensual, no en reportes separados — así ambos mecanismos se refuerzan "
    "en vez de competir por atención. Si al día 60 la tienda de Luis no muestra "
    "mejora, la acción no es presionar para que se siga el guion con más rigor — "
    "eso reproduciría el problema diagnosticado — sino revisar si el piso común "
    "definido realmente deja suficiente espacio para la conversación."
)

# ---------------------------------------------------------------------------
# REFERENCIAS
# ---------------------------------------------------------------------------
doc.add_page_break()
doc.add_heading("Referencias", level=1)
ref = p(indent0=True)
ref.paragraph_format.left_indent = Cm(1.27)
ref.paragraph_format.first_line_indent = Cm(-1.27)
ref.add_run(
    "Victorino, L., Verma, R., & Wardell, D. G. (2013). Script usage in "
    "standardized and customized service encounters: Implications for perceived "
    "service quality. Production and Operations Management, 22(3), 518–534. "
    "https://doi.org/10.1111/j.1937-5956.2012.01382.x"
)

# ---------------------------------------------------------------------------
# ANEXO 1 - RAE
# ---------------------------------------------------------------------------
doc.add_page_break()
doc.add_heading("Anexo 1. Resumen Analítico de Estudio (RAE)", level=1)
make_table(
    ["Campo", "Contenido"],
    [
        ["1. Identificación", "Victorino, L., Verma, R., & Wardell, D. G. (2013). "
         "Script usage in standardized and customized service encounters: "
         "Implications for perceived service quality. Production and Operations "
         "Management, 22(3), 518–534. "
         "https://doi.org/10.1111/j.1937-5956.2012.01382.x. Artículo de "
         "investigación empírica."],
        ["2. Pregunta del estudio", "¿Cómo afecta el nivel de guion verbal "
         "(scripting) a la calidad de servicio percibida por el cliente, y ese "
         "efecto es igual en encuentros estandarizados que en personalizados?"],
        ["3. Metodología", "Experimento basado en video, manipulando el nivel de "
         "guion verbal en encuentros de servicio estandarizados y personalizados, "
         "midiendo la calidad de servicio percibida por los participantes."],
        ["4. Hallazgos", "(a) En encuentros estandarizados, un mayor nivel de "
         "guion verbal no afectó significativamente la calidad percibida. (b) En "
         "encuentros personalizados, un guion predominantemente verbal sí afectó "
         "negativamente la calidad percibida — el resultado más bajo se dio ahí. "
         "Limitación advertida por el equipo: es un experimento en video, no "
         "interacciones reales; trasladar el umbral exacto a tiendas de barrio "
         "exige cautela."],
        ["5. Aplicación al caso", "Usado explícitamente en la sección 3: la "
         "tienda de Luis (encuentro más personalizado) corresponde al tipo de "
         "situación donde el guion causa más daño; las tiendas donde el guion es "
         "útil probablemente operan encuentros más estandarizados."],
        ["6. Juicio crítico", "El estudio mide percepción en un entorno "
         "experimental controlado, no en una tienda real con clientes "
         "recurrentes; el hallazgo conceptual es trasladable, pero no los valores "
         "exactos de “cuánto” guion es tolerable — eso requiere la evidencia local "
         "del canal de retroalimentación (Alternativa 2), no una cifra del "
         "estudio."],
    ],
    col_widths_cm=[3.5, 12.5],
)

# ---------------------------------------------------------------------------
# ANEXO 2 - APORTES INDIVIDUALES
# ---------------------------------------------------------------------------
doc.add_page_break()
doc.add_heading("Anexo 2. Trazabilidad de los aportes individuales", level=1)
make_table(
    ["Integrante", "Aporte específico", "Decisión que defendió", "Aprendizaje o límite"],
    [
        ["Jhoan Jesus Cardozo Gelvis",
         "Desarrolló la sección 1 (Comprender el caso): clasificó los cinco "
         "hechos del dossier en documentado/testimonio/vacío de información y "
         "construyó la matriz hecho-apreciación-emoción-conducta para Luis y el "
         "encargado de la tienda donde el guion resultó útil.",
         "Defendió que el problema no se resuelve solo con el guion en sí, sino "
         "con que nadie escuchó antes la diferencia de resultados entre tiendas "
         "(dato de la tarjeta B1: una tienda bajó su conversación espontánea, "
         "otras dos lo consideran útil).",
         "Aprendió que separar hecho de hipótesis evita diagnosticar con "
         "suposiciones sobre lo que siente una persona sin tener evidencia de "
         "ello."],
        ["Jonathan Adonay Rubio Jimenez",
         "Desarrolló la sección 2 (alternativas) y el Anexo 1 (RAE): comparó las "
         "tres alternativas con los cuatro filtros de creatividad estratégica y "
         "respaldó la elección con un artículo académico real.",
         "Defendió priorizar el piso común (Alternativa 1) antes que segmentar "
         "el guion de inmediato (Alternativa 3), apoyado en el hallazgo de "
         "Victorino et al. (2013) sobre encuentros personalizados vs. "
         "estandarizados, aplicado a la tienda de Luis (B-F2).",
         "Aprendió que una fuente académica verificable cambia la solidez de "
         "una recomendación frente a basarse solo en intuición."],
        ["Ivan Dario Zarate Rincon",
         "Desarrolló las secciones 3, 4 y 5: el guion de conversación de cuatro "
         "movimientos, los acuerdos de coordinación entre tiendas y la "
         "recomendación gerencial con sus acciones priorizadas.",
         "Defendió que la conducta a corregir era la falta de escucha de Clara "
         "antes de generalizar el guion (B-F2), no el contenido del guion en sí "
         "mismo.",
         "Aprendió que separar asertividad de empatía en una conversación "
         "difícil evita tanto imponer una decisión como evadir el tema."],
    ],
    col_widths_cm=[3.0, 5.0, 4.5, 3.5],
)

# ---------------------------------------------------------------------------
# DECLARACIÓN DE USO DE IA
# ---------------------------------------------------------------------------
doc.add_page_break()
doc.add_heading("Declaración de uso de inteligencia artificial generativa", level=1)
p(
    "Herramienta usada como apoyo de referencia: Claude (Anthropic). Para qué se "
    "usó: ideación inicial sobre el diagnóstico y las alternativas, organización "
    "del texto, corrección de estilo, contraste de las tres alternativas entre sí "
    "y búsqueda inicial de literatura para el Anexo 1. El equipo revisó, discutió "
    "y asumió como propio cada elemento del diagnóstico, las alternativas, el "
    "guion de conversación, los acuerdos de coordinación y la recomendación "
    "final antes de entregar. Qué se verificó: que el artículo citado (DOI "
    "incluido) fuera accesible y pertinente, y que los datos citados del dossier "
    "(B-F1 a B-F8 y el dato de la tarjeta B1) correspondieran exactamente al "
    "enunciado."
)

doc.save(OUT_PATH)
print(f"Documento generado: {OUT_PATH}")
