"""Genera el informe del ACA 1 (IA para la Transformacion Digital en Sectores
Productivos) en Word, formato APA 7.
Caso: Bienestar Integral S.A.S. (salud estetica) resuelto con Apollo Services
(M1 + M2 + M6).
Fuente de contenido: ../planificacion/solucion.md
Salida: ACA1_Informe_Apollo_Services.docx (y su conversion a PDF via soffice)
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(OUT_DIR, "ACA1_Informe_Apollo_Services.docx")
FIGURA1 = os.path.join(OUT_DIR, "figura1_arquitectura.png")

INTEGRANTES = [
    "Jhoan Jesus Cardozo Gelvis",
    "Jonathan Adonay Rubio Jimenez",
    "Daniel Silva Quintero",
    "Yeimis Urzola Torres",
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


def add_figure(path, caption, width_in=6.3):
    pic_p = doc.add_paragraph()
    pic_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic_p.paragraph_format.first_line_indent = Cm(0)
    run = pic_p.add_run()
    run.add_picture(path, width=Inches(width_in))
    cap = p(caption, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
    cap.paragraph_format.space_after = Pt(10)


# ---------------------------------------------------------------------------
# PORTADA
# ---------------------------------------------------------------------------
for _ in range(4):
    p()
p("ACA 1 — IA para la Transformación Digital en Sectores Productivos",
  bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("Ecosistema de IA empresarial: Apollo Services para Bienestar Integral S.A.S.",
  align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p()
p("Especialización en Inteligencia Artificial", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("Corporación Unificada Nacional de Educación Superior — CUN", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("Grupo 3 (G3)", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p()
for nombre in INTEGRANTES:
    p(nombre, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p()
p("Docente: Jainer Andrés Ballesteros Rincón", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
p("1 de noviembre de 2026", align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
doc.add_page_break()

# ---------------------------------------------------------------------------
# 1. PROBLEMA ORGANIZACIONAL
# ---------------------------------------------------------------------------
doc.add_heading("1. Problema organizacional", level=1)

p(
    "Bienestar Integral S.A.S. es una pyme del sector salud estética, con sedes en "
    "Bogotá y Medellín, cuyo equipo comercial (tres personas) atiende consultas de "
    "pacientes potenciales por tres canales simultáneos: WhatsApp Business, "
    "Instagram y Facebook. Cada integrante del equipo revisa manualmente cada red "
    "por separado, sin un punto único de gestión de las conversaciones."
)
p(
    "Esto produce tres efectos medibles: (a) contactos que escriben y no reciben "
    "respuesta a tiempo porque ningún canal tiene prioridad visible sobre otro; "
    "(b) ausencia de trazabilidad sobre quién es un simple Seguidor y quién es un "
    "Prospecto con intención real de agendar un tratamiento; y (c) citas que se "
    "acuerdan de palabra por chat pero nunca quedan formalmente confirmadas en una "
    "agenda compartida, por lo que se pierden sin que nadie lo note a tiempo. El "
    "problema es de negocio —fuga de oportunidades de venta— y no un problema "
    "técnico de ninguna de las plataformas usadas individualmente."
)

# ---------------------------------------------------------------------------
# 2. SECTOR ECONÓMICO
# ---------------------------------------------------------------------------
doc.add_heading("2. Sector económico", level=1)

p(
    "Bienestar Integral S.A.S. pertenece al sector servicios, específicamente salud "
    "estética (odontología estética, dermatología y nutrición), con un modelo "
    "comercial B2C intensivo en redes sociales: su canal principal de captación y "
    "conversión de pacientes es conversacional y digital, no una sala de ventas "
    "física. Este perfil —equipo comercial pequeño (2 a 5 personas) dependiente de "
    "redes sociales para vender, sin capacidad propia de construir infraestructura "
    "de IA— es representativo del segmento objetivo al que se dirige Apollo "
    "Services."
)

# ---------------------------------------------------------------------------
# 3. SOLUCIÓN BASADA EN INTELIGENCIA ARTIFICIAL
# ---------------------------------------------------------------------------
doc.add_heading("3. Solución basada en inteligencia artificial", level=1)

p(
    "La solución es Apollo Services, un CRM comercial multicanal con agentes de "
    "IA, desplegado para Bienestar Integral S.A.S. con tres de sus seis módulos "
    "comerciales independientes: M1 (bandeja unificada), M2 (agente de respuesta a "
    "potenciales clientes) y M6 (agente de agendamiento y cierre)."
)
p(
    "M1 centraliza en un único tablero, tipo CRM, las conversaciones de los tres "
    "canales, reemplazando la revisión manual canal por canal. M2 atiende todo "
    "contacto entrante, lo clasifica como Seguidor o Prospecto y recolecta los "
    "datos obligatorios de la encuesta (tratamiento de interés, sede preferida, "
    "disponibilidad) antes de escalar a agendamiento. M6, una vez el Prospecto "
    "tiene los datos completos, coordina la fecha de la cita con el paciente, la "
    "confirma con la Líder comercial, la agenda en Google Calendar (con enlace de "
    "Meet si la primera valoración es virtual) y hace seguimiento posterior con el "
    "equipo comercial para registrar el resultado."
)
p(
    "No se requiere construir software nuevo desde cero: los tres módulos ya "
    "existen como flujos reutilizables de n8n sobre una base de datos compartida "
    "(Supabase), por lo que el esfuerzo de puesta en marcha para este cliente es de "
    "configuración —plantilla de la compañía, credenciales de sus canales, "
    "preguntas de la encuesta— y no de desarrollo de producto nuevo."
)

# ---------------------------------------------------------------------------
# 4. ARQUITECTURA DEL ECOSISTEMA DE IA
# ---------------------------------------------------------------------------
doc.add_heading("4. Arquitectura del ecosistema de IA", level=1)

p(
    "La Figura 1 representa el flujo completo del sistema, desde que el paciente "
    "escribe por cualquiera de los tres canales hasta que recibe una respuesta."
)
add_figure(FIGURA1, "Figura 1. Flujo del ecosistema de IA — Apollo Services para Bienestar Integral S.A.S.")

p(
    "El mensaje entrante llega por WhatsApp, Instagram o Facebook a través de la "
    "misma API (Meta Cloud API, provisionada vía 360dialog), que lo entrega como "
    "webhook a n8n, el motor que orquesta a los agentes M2 y M6. Si el mensaje trae "
    "audio o imagen, pasa primero por Gemini Flash, que lo normaliza a texto plano; "
    "si ya es texto, va directo a Claude. Claude es el único motor conversacional "
    "del sistema (para mantener un tono consistente sin importar el canal de "
    "origen): clasifica al contacto y, si corresponde, recoge los datos de la "
    "encuesta, que M2 escribe en Supabase marcando `datos_completos = true`."
)
p(
    "El principio de diseño clave —ya cerrado en el proyecto— es que los módulos "
    "nunca se llaman directamente entre sí: M6 no es invocado por M2, sino que "
    "observa ese cambio de estado en la base de datos compartida y arranca su "
    "propio flujo de agendamiento de forma autónoma. Esto permite vender M1, M2 o "
    "M6 de forma independiente, y que cada uno siga funcionando aunque otro módulo "
    "no haya sido contratado, siempre que el dato que necesita exista en la base de "
    "datos, sin importar quién lo puso ahí."
)
p(
    "Tras agendar, M6 registra la Oportunidad y, después de la cita, el "
    "resumen_cierre. Toda esta información se visualiza en tiempo real en la app "
    "Next.js (sección M1, bandeja de conversaciones), donde la Líder comercial "
    "ejerce la supervisión humana descrita en la sección 9."
)

# ---------------------------------------------------------------------------
# 5. TECNOLOGÍAS INVOLUCRADAS
# ---------------------------------------------------------------------------
doc.add_heading("5. Tecnologías involucradas", level=1)

p("La Tabla 1 detalla cada componente del ecosistema junto con la tecnología que lo soporta.")
p("Tabla 1", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
make_table(
    ["Componente", "Tecnología", "Rol en el ecosistema"],
    [
        ["Canal de comunicación", "WhatsApp Business, Instagram, Facebook (Meta Cloud/Graph API)",
         "Punto de entrada y salida de la conversación con el paciente"],
        ["API / puente", "Meta Cloud API vía 360dialog",
         "Transporta el mensaje entrante al motor de automatización y la respuesta de vuelta"],
        ["Motor de automatización", "n8n (self-hosted)",
         "Orquesta los flujos de M2 y M6; triggers por webhook y por cron"],
        ["Modelo de IA conversacional", "Claude (Sonnet/Haiku)",
         "Único motor de M2; mantiene un tono consistente en todos los canales"],
        ["Modelo de IA — normalización de medios", "Gemini Flash",
         "Convierte audio/imagen a texto plano antes de que Claude lo procese"],
        ["Base de datos compartida", "Supabase self-hosted (Postgres + Realtime + Auth + Storage)",
         "Única fuente de verdad del estado; los módulos reaccionan a sus cambios, no se llaman entre sí"],
        ["Calendario", "Google Calendar API (OAuth2 por organización) + Meet",
         "Agenda la cita y genera el enlace de videollamada automáticamente"],
        ["Interfaz / dashboard", "App Next.js (sección M1)",
         "Bandeja de conversaciones donde la Líder comercial supervisa y reasigna casos"],
        ["Infraestructura cloud", "Docker Compose + reverse proxy Caddy, un stack por cliente",
         "Despliegue dedicado para Bienestar Integral S.A.S., sin compartir base de datos con otros clientes"],
    ],
    col_widths_cm=[3.6, 5.4, 7.0],
)

# ---------------------------------------------------------------------------
# 6. RIESGOS IDENTIFICADOS
# ---------------------------------------------------------------------------
doc.add_heading("6. Riesgos identificados", level=1)

p(
    "La Tabla 2 clasifica los riesgos asociados a la implementación de este "
    "ecosistema de IA por tipo (técnico, operativo u organizacional) y describe su "
    "impacto concreto dentro del sistema diseñado para Bienestar Integral S.A.S."
)
p("Tabla 2", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent0=True)
make_table(
    ["Riesgo", "Tipo", "Impacto dentro del sistema diseñado"],
    [
        ["Dependencia tecnológica de Meta", "Técnico / operativo",
         "WhatsApp dejó de ser 100% gratuito desde oct-2026 (1.000 mensajes de "
         "servicio gratis/mes/número); el costo por conversación crece con el "
         "volumen de pacientes, fuera del control del diseño del producto."],
        ["Saturación del sistema", "Técnico",
         "El stack está dimensionado para ~100 prospectos/mes por cliente; un pico "
         "de concurrencia (ej. campaña de descuentos) puede exceder lo que el VPS "
         "asignado soporta si no se redimensiona a tiempo."],
        ["Errores de la IA (alucinaciones, falsos positivos)", "Operativo",
         "M2 puede clasificar mal a un paciente o malinterpretar un dato de la "
         "encuesta; mitigado porque ninguna decisión final de agendamiento se toma "
         "sin confirmación humana (sección 9)."],
        ["Privacidad de datos personales", "Organizacional / legal",
         "Bienestar Integral S.A.S. maneja datos de salud de pacientes; el "
         "proyecto tiene pendiente, a nivel general, una Política de Tratamiento "
         "de Datos Personales (Habeas Data, Colombia) antes del lanzamiento "
         "comercial — más sensible aún en un cliente del sector salud."],
        ["Latencia en la respuesta", "Técnico",
         "Si llega una imagen (ej. foto de un diagnóstico previo) y Gemini Flash "
         "tarda en normalizarla, el paciente puede percibir el chatbot como lento."],
        ["Manejo manual de secretos", "Operativo",
         "Las credenciales de los canales de este cliente se gestionan en un "
         "archivo .env manual, no en un gestor de secretos — aceptable al volumen "
         "actual, pero es un riesgo que crece si Apollo Services suma más "
         "clientes simultáneos."],
    ],
    col_widths_cm=[3.4, 2.6, 10.0],
)

# ---------------------------------------------------------------------------
# 7. IMPACTO ORGANIZACIONAL
# ---------------------------------------------------------------------------
doc.add_heading("7. Impacto organizacional", level=1)

p(
    "Impacto positivo: el equipo comercial deja de revisar tres redes por "
    "separado; la Líder comercial gana visibilidad en tiempo real de cuántos "
    "contactos están sin responder y puede reasignar casos desde un único "
    "tablero. El agendamiento deja de depender de que alguien recuerde confirmar "
    "manualmente en un calendario compartido, lo que ataca directamente la fuga de "
    "prospectos descrita en la sección 1."
)
p(
    "Impacto negativo o a vigilar: el rol del equipo comercial cambia —de "
    "responder todo manualmente pasa a supervisar y confirmar lo que la IA ya "
    "adelantó— lo que puede generar resistencia inicial si no se comunica que el "
    "sistema no reemplaza al equipo, sino que filtra el trabajo repetitivo. "
    "También aparece una dependencia tecnológica nueva: si Apollo Services o "
    "alguno de sus proveedores (Meta, Claude, Google Calendar) presenta una caída, "
    "el proceso comercial de la organización se ve directamente afectado, algo que "
    "antes no ocurría cuando el proceso era enteramente manual."
)

# ---------------------------------------------------------------------------
# 8. COSTOS GENERALES ESTIMADOS
# ---------------------------------------------------------------------------
doc.add_heading("8. Costos generales estimados", level=1)

p(
    "No se presentan valores exactos de facturación, sino la identificación "
    "conceptual de los elementos de costo reales del stack:"
)
for texto in [
    "Consumo de tokens de los modelos de IA: al volumen estimado para este "
    "cliente (≈100 casos/mes, 12–25 mensajes por caso, ≈1.500–2.500 turnos/mes) el "
    "costo de LLM es marginal, sin importar si se usa Claude Sonnet/Haiku o "
    "Gemini Flash para la normalización.",
    "Costo por conversación de WhatsApp Business: 1.000 mensajes de servicio "
    "gratis/mes/número desde oct-2026, y tarifa por conversación después de ese "
    "umbral (referencia aproximada 0.004–0.025 USD/mensaje según tipo).",
    "Infraestructura cloud: un VPS por cliente corriendo Supabase + n8n + app, "
    "costo fijo mensual bajo, independiente del volumen dentro del rango "
    "dimensionado.",
    "Almacenamiento: incluido en el mismo Supabase self-hosted (Storage); solo "
    "crece si se almacenan muchos adjuntos de audio o imagen de los pacientes.",
    "Calendario: Google Calendar API no tiene costo adicional para este volumen "
    "de uso.",
]:
    bp = p(indent0=True)
    bp.paragraph_format.left_indent = Cm(0.9)
    r = bp.add_run("• ")
    bp.add_run(texto)

# ---------------------------------------------------------------------------
# 9. SUPERVISIÓN HUMANA (HUMAN IN THE LOOP)
# ---------------------------------------------------------------------------
doc.add_heading("9. Supervisión humana (Human in the Loop)", level=1)

p(
    "La supervisión humana tiene dos capas, consistentes con cómo ya está "
    "construido el producto. Primero, una restricción por funciones acotadas: "
    "M2 solo puede invocar funciones específicas y auditables "
    "(clasificar_contacto, registrar_dato_encuesta), y M6 solo puede agendar_cita, "
    "confirmar_con_lider y marcar_resultado_reunion — ninguno tiene una función de "
    "escritura libre en la base de datos ni de ejecución de comandos."
)
p(
    "Segundo, un punto de intervención humana explícito: la Líder comercial "
    "revisa y reasigna conversaciones desde la bandeja (M1) antes de que lleguen a "
    "agendamiento definitivo, y confirma manualmente cada cita que M6 propone "
    "antes de que quede en firme en el calendario. Tras cada reunión, el "
    "resumen_cierre generado por el agente de seguimiento es validado por el "
    "equipo comercial, no se asume como verdad definitiva — esto es lo que evita "
    "que un falso positivo de clasificación (sección 6) termine en una cita mal "
    "agendada sin que nadie la revise."
)

# ---------------------------------------------------------------------------
# CONCLUSIONES
# ---------------------------------------------------------------------------
doc.add_heading("Conclusiones", level=1)

p(
    "El ecosistema de IA propuesto no reemplaza al equipo comercial de Bienestar "
    "Integral S.A.S.: automatiza la parte repetitiva y propensa a error humano "
    "—clasificación inicial, recolección de datos, coordinación de fecha— y libera "
    "al equipo para enfocarse en lo que la IA no puede hacer, que es la relación "
    "con el paciente y la decisión final sobre cada caso."
)
p(
    "La arquitectura modular de Apollo Services —módulos independientes que "
    "reaccionan a estado compartido en base de datos, sin llamarse entre sí— "
    "permite que esta organización empiece con el paquete mínimo (M1+M2+M6) y "
    "escale a más módulos (M3, M4, M5) sin necesidad de rediseñar lo ya "
    "construido, a medida que el volumen de pacientes o la complejidad del "
    "negocio lo justifique."
)

p(
    "Enlace del video de sustentación: [PENDIENTE — agregar aquí el enlace "
    "público antes de la entrega final, según lo exige el enunciado]."
)

# ---------------------------------------------------------------------------
# ANEXO. TRAZABILIDAD DE LOS APORTES INDIVIDUALES
# ---------------------------------------------------------------------------
doc.add_page_break()
doc.add_heading("Anexo. Trazabilidad de los aportes individuales", level=1)
make_table(
    ["Integrante", "Aporte específico", "Decisión que defendió", "Aprendizaje o límite"],
    [
        ["Jhoan Jesus Cardozo Gelvis",
         "Desarrolló las secciones 1 y 2 (problema organizacional y sector "
         "económico): delimitó el caso de Bienestar Integral S.A.S. a partir del "
         "problema de negocio ya documentado del proyecto (fuga de prospectos por "
         "gestión multicanal dispersa).",
         "Defendió formular el problema desde una perspectiva organizacional —"
         "pérdida de ingresos— y no técnica, para que la solución propuesta en la "
         "sección 3 respondiera a una necesidad real del negocio.",
         "Aprendió a diferenciar un problema de negocio de un problema técnico "
         "antes de proponer cualquier solución de IA."],
        ["Jonathan Adonay Rubio Jimenez",
         "Desarrolló las secciones 3 y 4 (solución de IA y arquitectura del "
         "ecosistema), incluyendo el diseño de la Figura 1 a partir del stack ya "
         "confirmado del proyecto Apollo Services.",
         "Defendió usar el paquete mínimo M1+M2+M6 en vez de los seis módulos "
         "completos, por ser suficiente para resolver el problema delimitado sin "
         "sobredimensionar el proyecto.",
         "Aprendió que una arquitectura donde los módulos nunca se llaman entre "
         "sí, sino que reaccionan a estado compartido, permite vender e "
         "implementar cada módulo de forma independiente."],
        ["Daniel Silva Quintero",
         "Desarrolló la sección 5 (tecnologías involucradas) y la Tabla 1, "
         "relacionando cada componente de la arquitectura con la tecnología real "
         "que lo soporta.",
         "Defendió mantener a Claude como único motor conversacional y usar "
         "Gemini Flash solo como capa de normalización de medios, para no perder "
         "consistencia de tono entre canales.",
         "Aprendió que separar el modelo conversacional del modelo que procesa "
         "medios reduce dependencia de que un solo proveedor cubra todas las "
         "capacidades necesarias."],
        ["Yeimis Urzola Torres",
         "Desarrolló la sección 6 (riesgos identificados) y la Tabla 2, "
         "clasificando cada riesgo como técnico, operativo u organizacional.",
         "Defendió incluir el riesgo de privacidad de datos de salud como punto "
         "crítico propio de este cliente, más sensible que el riesgo genérico ya "
         "documentado para el proyecto en general.",
         "Aprendió que el mismo riesgo documentado a nivel de producto (Habeas "
         "Data) puede tener distinto nivel de criticidad según el sector del "
         "cliente final."],
        ["Ivan Dario Zarate Rincon",
         "Desarrolló las secciones 7, 8 y 9 (impacto organizacional, costos "
         "estimados y supervisión humana) y las conclusiones del informe.",
         "Defendió que ningún agente del ecosistema debe tener una función de "
         "escritura libre en la base de datos, sino funciones acotadas y "
         "auditables, como garantía de que la supervisión humana sea real y no "
         "solo declarativa.",
         "Aprendió que la supervisión humana efectiva se diseña restringiendo "
         "qué puede hacer un agente, no solo revisando después lo que ya hizo."],
    ],
    col_widths_cm=[3.0, 4.4, 4.0, 4.6],
)

doc.save(OUT_PATH)
print(f"Documento generado: {OUT_PATH}")
