"""Genera la Figura 1 (diagrama de arquitectura del ecosistema de IA) del ACA 1.
Salida: figura1_arquitectura.png, insertada luego en el informe Word.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(OUT_DIR, "figura1_arquitectura.png")

fig, ax = plt.subplots(figsize=(10, 7.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 13)
ax.axis("off")

BOX_STYLE = dict(boxstyle="round,pad=0.35", linewidth=1.3)

def box(x, y, w, h, text, fc="#eaf2fb", ec="#2c5d8f", fontsize=9.3, weight="normal"):
    b = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                        boxstyle="round,pad=0.02,rounding_size=0.12",
                        linewidth=1.3, edgecolor=ec, facecolor=fc)
    ax.add_patch(b)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            weight=weight, wrap=True)

def arrow(x1, y1, x2, y2, text=None, text_dx=0.35):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                         linewidth=1.3, color="#2c5d8f")
    ax.add_patch(a)
    if text:
        ax.text((x1 + x2) / 2 + text_dx, (y1 + y2) / 2, text, fontsize=7.6,
                color="#555555", ha="left", va="center", style="italic")

# Nodos (de arriba hacia abajo)
box(5, 12.3, 6.4, 0.8, "Paciente\n(WhatsApp · Instagram · Facebook)", fc="#fdf3e3", ec="#b5802a")
box(5, 11.0, 6.4, 0.8, "API del canal — Meta Cloud API vía 360dialog\n(mismo Graph API para los 3 canales)")
box(5, 9.7, 6.4, 0.8, "n8n — motor de orquestación\n(aloja los agentes M2 y M6)", fc="#eafbe9", ec="#2e7d32")

box(2.3, 8.3, 3.6, 0.9, "Gemini Flash\n(normaliza audio/imagen\na texto plano)", fc="#f3ecfb", ec="#6a3d9a", fontsize=8.6)
box(7.3, 8.3, 3.6, 0.9, "Claude\n(M2 — motor conversacional:\nclasifica Seguidor/Prospecto,\nrecolecta encuesta)", fc="#f3ecfb", ec="#6a3d9a", fontsize=8.3)

box(5, 6.8, 6.6, 1.0,
    "Supabase / PostgreSQL — base de datos compartida\n"
    "M2 escribe `contacto` / `prospecto` (datos_completos = true)",
    fc="#fdeaea", ec="#a33a3a", fontsize=8.6)

box(5, 5.3, 6.6, 0.95,
    "n8n — M6 observa el cambio de estado y coordina:\n"
    "fecha con el paciente → confirmación con la Líder → Google Calendar (OAuth2 + Meet)",
    fc="#eafbe9", ec="#2e7d32", fontsize=8.3)

box(5, 4.0, 6.6, 0.8, "Supabase — registra `Oportunidad` y `resumen_cierre`", fc="#fdeaea", ec="#a33a3a")

box(2.6, 2.6, 4.2, 0.95, "App Next.js — M1\n(bandeja: Líder ve y\nreasigna conversaciones)", fontsize=8.6)
box(7.4, 2.6, 4.2, 0.95, "Vista interna de estado\nde Prospectos / Oportunidades", fontsize=8.6)

box(5, 1.1, 7.4, 0.85,
    "Supervisión humana — Líder comercial y equipo comercial\n"
    "validan clasificación, reasignan casos y confirman cada cita/resultado",
    fc="#fff6d6", ec="#b58b00", fontsize=8.8, weight="bold")

# Flechas verticales principales
arrow(5, 11.9, 5, 11.4)
arrow(5, 10.6, 5, 10.1)
arrow(5, 9.3, 2.3, 8.75, text="si hay audio/imagen")
arrow(5, 9.3, 7.3, 8.75, text="si es texto")
arrow(2.3, 7.85, 5, 7.3, text="texto normalizado")
arrow(7.3, 7.85, 5, 7.3)
arrow(5, 6.3, 5, 5.78)
arrow(5, 4.83, 5, 4.4)
arrow(5, 3.6, 2.6, 3.08)
arrow(5, 3.6, 7.4, 3.08)
arrow(2.6, 2.13, 5, 1.53)
arrow(7.4, 2.13, 5, 1.53)

# Flecha de retorno (respuesta al paciente)
back = FancyArrowPatch((8.6, 9.7), (8.6, 11.8), connectionstyle="arc3,rad=0.25",
                        arrowstyle="-|>", mutation_scale=13, linewidth=1.1,
                        color="#888888", linestyle="--")
ax.add_patch(back)
ax.text(9.0, 10.75, "respuesta\nal paciente", fontsize=7.2, color="#777777", ha="left", style="italic")

ax.text(5, 12.95, "Figura 1. Flujo del ecosistema de IA — Apollo Services para Bienestar Integral S.A.S.",
        ha="center", fontsize=10.5, weight="bold")

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=200, bbox_inches="tight")
print(f"Figura generada: {OUT_PATH}")
