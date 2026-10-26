"""Genera las diapositivas de apoyo para la sustentacion en video del ACA 1
(IA para la Transformacion Digital en Sectores Productivos).
Guion correspondiente: guion-sustentacion-video.md + guion-<nombre>.txt
Salida: ACA1_Presentacion_Apollo_Services.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(OUT_DIR, "ACA1_Presentacion_Apollo_Services.pptx")
FIGURA1 = os.path.join(OUT_DIR, "figura1_arquitectura.png")

AZUL = RGBColor(0x2C, 0x5D, 0x8F)
GRIS = RGBColor(0x40, 0x40, 0x40)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_slide():
    return prs.slides.add_slide(BLANK)


def add_title(slide, text, size=32, top=Inches(0.4), color=AZUL):
    box = slide.shapes.add_textbox(Inches(0.6), top, Inches(12.1), Inches(1.0))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = color
    p.font.name = "Calibri"
    return box


def add_subtitle(slide, text, top=Inches(1.25), size=18, color=GRIS, italic=True):
    box = slide.shapes.add_textbox(Inches(0.6), top, Inches(12.1), Inches(0.6))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.italic = italic
    p.font.color.rgb = color
    p.font.name = "Calibri"
    return box


def add_bullets(slide, items, top=Inches(1.7), left=Inches(0.7), width=Inches(11.9),
                 height=Inches(5.2), size=20, speaker=None):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {item}" if item else ""
        p.font.size = Pt(size)
        p.font.color.rgb = GRIS
        p.font.name = "Calibri"
        p.space_after = Pt(10)
    if speaker:
        add_speaker_tag(slide, speaker)
    return box


def add_speaker_tag(slide, name):
    box = slide.shapes.add_textbox(Inches(0.6), Inches(6.95), Inches(12.0), Inches(0.4))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = f"Presenta: {name}"
    p.font.size = Pt(14)
    p.font.italic = True
    p.font.color.rgb = AZUL
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.RIGHT


# ---------------------------------------------------------------------------
# 1. PORTADA
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "ACA 1 — IA para la Transformación Digital en Sectores Productivos",
          size=30, top=Inches(2.2))
add_subtitle(slide, "Ecosistema de IA empresarial: Apollo Services para Bienestar Integral S.A.S.",
             top=Inches(3.1), size=20, italic=False)
box = slide.shapes.add_textbox(Inches(0.6), Inches(4.2), Inches(12.1), Inches(2.0))
tf = box.text_frame
tf.word_wrap = True
integrantes = [
    "Jonathan Adonay Rubio Jimenez", "Jhoan Jesus Cardozo Gelvis",
    "Daniel Silva Quintero", "Yeimis Urzola Torres", "Ivan Dario Zarate Rincon",
]
for i, nombre in enumerate(integrantes):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = nombre
    p.font.size = Pt(18)
    p.font.color.rgb = GRIS
    p.alignment = PP_ALIGN.CENTER
add_subtitle(slide, "Grupo 3 (G3) · Especialización en Inteligencia Artificial · CUN",
             top=Inches(6.6), size=16)

# ---------------------------------------------------------------------------
# 2. PROBLEMA ORGANIZACIONAL
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "1. Problema organizacional")
add_bullets(slide, [
    "Bienestar Integral S.A.S. — pyme de salud estética (Bogotá y Medellín).",
    "Equipo comercial de 3 personas atiende WhatsApp, Instagram y Facebook por separado.",
    "Sin punto único de gestión de conversaciones.",
    "Contactos sin respuesta a tiempo; sin trazabilidad Seguidor vs. Prospecto.",
    "Citas acordadas de palabra que nunca quedan confirmadas en agenda compartida.",
    "Es un problema de negocio — fuga de oportunidades de venta — no técnico.",
], speaker="Jhoan Jesus Cardozo Gelvis")

# ---------------------------------------------------------------------------
# 3. SECTOR ECONÓMICO
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "2. Sector económico")
add_bullets(slide, [
    "Sector servicios — salud estética (odontología estética, dermatología, nutrición).",
    "Modelo comercial B2C intensivo en redes sociales.",
    "Canal principal de captación: conversacional y digital, no sala de ventas física.",
    "Perfil representativo del segmento objetivo de Apollo Services: equipos "
    "comerciales pequeños (2-5 personas) sin capacidad propia de construir IA.",
], speaker="Jhoan Jesus Cardozo Gelvis")

# ---------------------------------------------------------------------------
# 4. SOLUCIÓN BASADA EN IA
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "3. Solución basada en inteligencia artificial")
add_bullets(slide, [
    "Apollo Services — CRM comercial multicanal con agentes de IA.",
    "Paquete mínimo para este cliente: M1 + M2 + M6 (de 6 módulos independientes).",
    "M1 — Bandeja unificada: centraliza WhatsApp, Instagram y Facebook en un tablero.",
    "M2 — Clasifica Seguidor/Prospecto y recolecta la encuesta (tratamiento, sede, disponibilidad).",
    "M6 — Agenda la cita, confirma con la Líder, usa Google Calendar y da seguimiento post-cita.",
    "No requiere desarrollo nuevo: los 3 módulos ya existen como flujos de n8n reutilizables.",
], speaker="Jonathan Adonay Rubio Jimenez")

# ---------------------------------------------------------------------------
# 5. ARQUITECTURA DEL ECOSISTEMA (con figura)
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "4. Arquitectura del ecosistema de IA", top=Inches(0.3), size=28)
if os.path.exists(FIGURA1):
    slide.shapes.add_picture(FIGURA1, Inches(3.1), Inches(1.0), height=Inches(6.1))
add_speaker_tag(slide, "Jonathan Adonay Rubio Jimenez")

# ---------------------------------------------------------------------------
# 6. TECNOLOGÍAS INVOLUCRADAS
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "5. Tecnologías involucradas")
add_bullets(slide, [
    "Canal: WhatsApp Business, Instagram, Facebook (Meta Cloud/Graph API vía 360dialog).",
    "Motor de automatización: n8n (self-hosted) — orquesta M2 y M6.",
    "IA conversacional: Claude (único motor, tono consistente en todos los canales).",
    "Normalización de medios: Gemini Flash (audio/imagen → texto plano).",
    "Base de datos compartida: Supabase (Postgres + Realtime + Auth + Storage).",
    "Calendario: Google Calendar API (OAuth2) + Meet. Interfaz: App Next.js (M1).",
    "Infraestructura: Docker Compose + Caddy, un stack dedicado por cliente.",
], size=18, speaker="Daniel Silva Quintero")

# ---------------------------------------------------------------------------
# 7. RIESGOS IDENTIFICADOS
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "6. Riesgos identificados")
add_bullets(slide, [
    "Dependencia tecnológica de Meta — WhatsApp ya no es 100% gratuito desde oct-2026.",
    "Saturación del sistema en picos de concurrencia (ej. campañas de descuento).",
    "Errores de la IA (alucinaciones, falsos positivos) — mitigado con confirmación humana.",
    "Privacidad de datos de salud — prioridad: Política de Tratamiento de Datos Personales.",
    "Latencia al normalizar audio/imagen. Manejo manual de secretos (.env por cliente).",
], speaker="Yeimis Urzola Torres")

# ---------------------------------------------------------------------------
# 8. IMPACTO ORGANIZACIONAL
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "7. Impacto organizacional")
add_bullets(slide, [
    "Positivo: visibilidad en tiempo real, reasignación de casos, menos fuga de prospectos.",
    "Positivo: agendamiento ya no depende de confirmación manual en calendario compartido.",
    "A vigilar: el equipo pasa de responder todo a supervisar — riesgo de resistencia inicial.",
    "A vigilar: nueva dependencia tecnológica (Meta, Claude, Google Calendar).",
], speaker="Ivan Dario Zarate Rincon")

# ---------------------------------------------------------------------------
# 9. COSTOS GENERALES ESTIMADOS
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "8. Costos generales estimados")
add_bullets(slide, [
    "Tokens de IA: costo marginal al volumen estimado (~100 casos/mes).",
    "WhatsApp Business: tarifa por conversación tras superar el umbral gratuito mensual.",
    "Infraestructura cloud: un VPS por cliente, costo fijo mensual bajo.",
    "Almacenamiento: incluido en Supabase, crece solo con muchos adjuntos.",
    "Calendario: Google Calendar API sin costo adicional.",
], speaker="Ivan Dario Zarate Rincon")

# ---------------------------------------------------------------------------
# 10. SUPERVISIÓN HUMANA
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "9. Supervisión humana (Human in the Loop)")
add_bullets(slide, [
    "Funciones acotadas y auditables por agente — sin escritura libre en la base de datos.",
    "La Líder comercial revisa y reasigna conversaciones antes del agendamiento definitivo.",
    "Cada cita propuesta por M6 se confirma manualmente antes de quedar en firme.",
    "El resumen_cierre tras cada reunión lo valida el equipo comercial, no se asume como verdad.",
], speaker="Ivan Dario Zarate Rincon")

# ---------------------------------------------------------------------------
# 11. CONCLUSIONES Y CIERRE
# ---------------------------------------------------------------------------
slide = add_slide()
add_title(slide, "Conclusiones")
add_bullets(slide, [
    "El ecosistema no reemplaza al equipo comercial: automatiza lo repetitivo.",
    "Libera al equipo para la relación con el paciente y la decisión final de cada caso.",
    "Arquitectura modular: se puede escalar a más módulos (M3, M4, M5) sin rediseñar nada.",
    "",
    "¡Gracias por su atención!",
], speaker="Ivan Dario Zarate Rincon")

prs.save(OUT_PATH)
print(f"Presentación generada: {OUT_PATH}")
