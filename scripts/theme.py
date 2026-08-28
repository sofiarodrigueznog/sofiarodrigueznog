"""Fuente única de verdad del lenguaje visual.

Ningún otro módulo define un color ni una medida. Si el perfil cambia de
identidad, cambia aquí y en ningún otro sitio.
"""

# --- Color -----------------------------------------------------------------
# Cada SVG pinta su propio panel oscuro: así se ve igual en el modo claro y en
# el oscuro de GitHub, sin duplicar una paleta por tema.

BACKDROP = "#0B0C10"   # fondo del panel, casi negro
SURFACE = "#111319"    # superficie elevada dentro del panel
BORDER = "#22252E"     # borde de 1px, apenas perceptible
RULE = "#191C23"       # separadores internos

TEXT = "#E9EBF1"       # texto principal
TEXT_DIM = "#9AA1B1"   # texto secundario
TEXT_FAINT = "#5A6070"  # etiquetas, unidades, leyendas

ACCENT = "#8B7BFF"     # iris: el único color saturado del sistema
ACCENT_DIM = "#5B4FD6"

# Rampa del heatmap: del vacío al máximo. El nivel 0 es superficie, no color,
# para que los días sin actividad no compitan con los que sí la tienen.
RAMP = ("#171A22", "#2E2A63", "#463C9C", "#6857D4", "#9B8CFF")

# --- Tipografía ------------------------------------------------------------
# Solo familias del sistema: el SVG se sirve como imagen y no puede cargar
# fuentes externas.

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# --- Geometría -------------------------------------------------------------

RADIUS = 10            # radio del panel
PAD = 26               # padding interno del panel
