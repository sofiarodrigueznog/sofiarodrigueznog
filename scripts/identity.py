"""Dibuja la cabecera del perfil: el bloque de identidad.

Solo lleva tipografía grande. Todo lo que un SVG achica hasta volver ilegible
en móvil vive en el README como texto de verdad, no aquí.
"""

import json

import theme
from svg import document, esc, fade_in, panel

WIDTH = 768   # el mismo ancho que el panel de actividad: los dos alinean
HEIGHT = 200

ADVANCE = 0.6  # ancho de carácter en una monoespaciada, en ems

# Monograma: una S dibujada en la misma grilla que el calendario de actividad.
# La marca y el gráfico hablan el mismo idioma.
MARK = (
    (1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0),
    (1, 1, 1, 1, 1),
    (0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1),
)
MARK_CELL = 11
MARK_GAP = 3


def _prompt(profile: dict) -> str:
    """Línea de comando con tecleo simulado.

    El tecleo es un recorte que avanza de carácter en carácter: en una
    monoespaciada el paso coincide con el ancho real de la letra.
    """
    size = 13
    step = size * ADVANCE
    prefix = f"{profile['prompt']} % "
    command = profile["command"]
    command_x = theme.PAD + len(prefix) * step
    width = len(command) * step
    steps = ";".join(str(round(index * step, 1)) for index in range(len(command) + 1))

    return (
        f'  <text x="{theme.PAD}" y="44" font-size="{size}" fill="{theme.TEXT_FAINT}">'
        f'{esc(profile["prompt"])} '
        f'<tspan fill="{theme.ACCENT}">%</tspan>\n'
        + fade_in(0.0, 0.4, 0)
        + "  </text>\n"
        "  <defs>\n"
        '    <clipPath id="typing">\n'
        # El recorte nace completo y es `<set>` quien lo cierra: sin SMIL el
        # comando se lee entero en vez de desaparecer tras un recorte de 0px.
        f'      <rect x="{command_x}" y="30" width="{width}" height="20">\n'
        '        <set attributeName="width" to="0" begin="0s"/>\n'
        f'        <animate attributeName="width" values="{steps}" '
        f'calcMode="discrete" begin="0.35s" dur="0.6s" fill="freeze"/>\n'
        "      </rect>\n"
        "    </clipPath>\n"
        "  </defs>\n"
        f'  <text x="{command_x}" y="44" font-size="{size}" fill="{theme.TEXT_DIM}" '
        f'clip-path="url(#typing)">{esc(command)}</text>\n'
        # El cursor parpadea mientras se escribe y luego se retira: nada queda
        # animado de forma permanente.
        f'  <rect x="{command_x + width + 2}" y="33" width="7" height="13" '
        f'fill="{theme.ACCENT}" opacity="0">\n'
        '    <animate attributeName="opacity" values="0;1" begin="0.35s" '
        'dur="0.01s" fill="freeze"/>\n'
        '    <animate attributeName="opacity" values="1;0;1" begin="0.95s" '
        'dur="0.9s" repeatCount="2"/>\n'
        '    <animate attributeName="opacity" values="1;0" begin="2.75s" '
        'dur="0.3s" fill="freeze"/>\n'
        "  </rect>\n"
    )


def _mark() -> str:
    """Monograma en bloques, alineado a la derecha del panel."""
    pitch = MARK_CELL + MARK_GAP
    size = len(MARK) * pitch - MARK_GAP
    left = WIDTH - theme.PAD - size
    top = (HEIGHT - size) / 2

    cells = []
    for row, line in enumerate(MARK):
        for column, filled in enumerate(line):
            color = theme.ACCENT if filled else theme.SURFACE
            opacity = 0.85 if filled else 1
            cells.append(
                f'    <rect x="{left + column * pitch}" y="{top + row * pitch}" '
                f'width="{MARK_CELL}" height="{MARK_CELL}" rx="2" fill="{color}" '
                f'opacity="{opacity}"/>\n'
            )
    return "  <g>\n" + fade_in(1.45, 0.7, 0) + "".join(cells) + "  </g>\n"


def render(profile: dict) -> str:
    """Devuelve el SVG de identidad."""
    focus = " · ".join(profile["focus"])
    body = (
        panel(WIDTH, HEIGHT)
        + _prompt(profile)
        + f'  <text x="{theme.PAD}" y="106" font-size="34" fill="{theme.TEXT}" '
        f'letter-spacing="1.5">{esc(profile["name"].upper())}\n'
        + fade_in(1.0)
        + "  </text>\n"
        + f'  <text x="{theme.PAD}" y="134" font-size="14" fill="{theme.TEXT_DIM}">'
        f'{esc(profile["role"])}\n'
        + fade_in(1.15)
        + "  </text>\n"
        + f'  <text x="{theme.PAD}" y="166" font-size="12.5" '
        f'fill="{theme.TEXT_FAINT}" letter-spacing="0.6">{esc(focus)}\n'
        + fade_in(1.3)
        + "  </text>\n"
        + _mark()
    )
    return document(
        WIDTH,
        HEIGHT,
        f"{profile['name']} — {profile['role']}",
        f"Cabecera del perfil: {profile['name']}, {profile['role']}. "
        f"Áreas de trabajo: {focus}.",
        body,
    )


def load(path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
