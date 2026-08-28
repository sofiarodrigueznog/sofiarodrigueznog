"""Dibuja el calendario de contribuciones como SVG.

Este módulo no consulta la red: recibe los datos ya resueltos y solo decide
cómo se ven. Es la mitad de presentación de `contributions.py`.
"""

import theme
from svg import document, esc, panel

CELL = 10          # lado de la celda
GAP = 3            # aire entre celdas
PITCH = CELL + GAP
LABEL_COLUMN = 30  # ancho reservado para lun/mié/vie

GRID_X = theme.PAD + LABEL_COLUMN
GRID_Y = 92
WIDTH = GRID_X + 53 * PITCH - GAP + theme.PAD
HEIGHT = 228

MONTHS = ("ene", "feb", "mar", "abr", "may", "jun",
          "jul", "ago", "sep", "oct", "nov", "dic")
WEEKDAYS = {1: "lun", 3: "mié", 5: "vie"}  # la fila 0 es domingo

REVEAL_STEP = 0.018  # retraso entre semanas: el grafico se lee de izq. a der.
REVEAL_START = 0.15


def _month_labels(grid: list) -> str:
    """Marca el mes en la primera semana donde empieza.

    Se salta una etiqueta si quedaría pegada a la anterior: preferible perder
    un mes a que dos nombres se solapen.
    """
    out, previous_month, last_x = [], None, -99
    for column in range(53):
        cell = next((grid[row][column] for row in range(7) if grid[row][column]), None)
        if not cell:
            continue
        month = int(cell["date"][5:7])
        if month == previous_month:
            continue
        previous_month = month
        x = GRID_X + column * PITCH
        if x - last_x < 26:
            continue
        last_x = x
        out.append(
            f'    <text x="{x}" y="84" font-size="10" fill="{theme.TEXT_FAINT}">'
            f"{MONTHS[month - 1]}</text>\n"
        )
    return "".join(out)


def _weekday_labels() -> str:
    return "".join(
        f'    <text x="{theme.PAD}" y="{GRID_Y + row * PITCH + CELL - 1}" '
        f'font-size="9" fill="{theme.TEXT_FAINT}">{name}</text>\n'
        for row, name in WEEKDAYS.items()
    )


def _grid(grid: list) -> str:
    """Una capa por semana: 53 animaciones en vez de 371.

    Agrupar por columna es lo que hace ligero el archivo y a la vez expresa la
    animación: el año se revela semana a semana y se congela.
    """
    columns = []
    for column in range(53):
        cells = []
        for row in range(7):
            cell = grid[row][column]
            if not cell:
                continue
            fill = theme.RAMP[min(cell["level"], len(theme.RAMP) - 1)]
            cells.append(
                f'      <rect x="{GRID_X + column * PITCH}" '
                f'y="{GRID_Y + row * PITCH}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{fill}"/>\n'
            )
        if not cells:
            continue
        begin = round(REVEAL_START + column * REVEAL_STEP, 3)
        columns.append(
            f'    <g>\n'
            f'      <set attributeName="opacity" to="0" begin="0s"/>\n'
            f'      <animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin}s" dur="0.45s" fill="freeze"/>\n'
            + "".join(cells)
            + "    </g>\n"
        )
    return "".join(columns)


def _legend() -> str:
    """Escala de intensidad. Va con texto para no depender solo del color."""
    y = 196
    x = WIDTH - theme.PAD - (len(theme.RAMP) * 12 - 3) - 30
    swatches = "".join(
        f'    <rect x="{x + index * 12}" y="{y}" width="9" height="9" rx="2" '
        f'fill="{color}"/>\n'
        for index, color in enumerate(theme.RAMP)
    )
    return (
        f'    <text x="{x - 6}" y="{y + 8}" font-size="9" fill="{theme.TEXT_FAINT}" '
        f'text-anchor="end">menos</text>\n'
        + swatches
        + f'    <text x="{WIDTH - theme.PAD}" y="{y + 8}" font-size="9" '
        f'fill="{theme.TEXT_FAINT}" text-anchor="end">más</text>\n'
    )


def render(data: dict) -> str:
    """Devuelve el SVG completo del año de actividad."""
    summary = (
        f"{data['total']} contribuciones · {data['active_days']} días activos"
    )
    body = (
        panel(WIDTH, HEIGHT)
        + f'  <text x="{theme.PAD}" y="42" font-size="12" fill="{theme.TEXT}" '
        f'letter-spacing="1.6">actividad</text>\n'
        + f'  <text x="{WIDTH - theme.PAD}" y="42" font-size="11" '
        f'fill="{theme.TEXT_FAINT}" text-anchor="end">{esc(summary)}</text>\n'
        + f'  <line x1="{theme.PAD}" y1="58" x2="{WIDTH - theme.PAD}" y2="58" '
        f'stroke="{theme.RULE}"/>\n'
        + "  <g>\n"
        + _month_labels(data["grid"])
        + _weekday_labels()
        + _grid(data["grid"])
        + f'    <text x="{theme.PAD}" y="204" font-size="9" '
        f'fill="{theme.TEXT_FAINT}">{esc(data["start"])} → {esc(data["end"])}</text>\n'
        + _legend()
        + "  </g>\n"
    )
    return document(
        WIDTH,
        HEIGHT,
        "Actividad de contribuciones en GitHub",
        f"Calendario de 53 semanas entre {data['start']} y {data['end']}: "
        f"{data['total']} contribuciones en {data['active_days']} días activos, "
        f"con un máximo de {data['busiest']} en un solo día.",
        body,
    )
