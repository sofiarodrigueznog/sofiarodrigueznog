"""Dibuja la consola del perfil: retrato ASCII y ficha del sistema.

Recibe el retrato ya convertido (`data/portrait.json`) y el contenido
(`data/profile.json`). No abre imágenes ni consulta la red: solo compone.
"""

import json

import theme
from svg import esc, fade_in, panel

WIDTH = 768          # el mismo ancho que el panel de actividad: los dos alinean
PAD = 24
TITLEBAR = 44

ART_BOX = 376        # ancho reservado al retrato
ADVANCE = 0.6        # avance de un carácter monoespaciado, en ems
LINE = 1.01          # interlineado, en ems
ART_MAX = 320        # alto máximo del retrato

ROW = 14.5           # alto de una fila de la ficha
HEADER = 22          # alto de un encabezado de sección
PANEL_GAP = 10
KEY_COLUMN = 80      # ancho de la columna de etiquetas

TYPE_START = 0.25    # el retrato empieza a imprimirse
TYPE_STEP = 0.045    # retraso entre filas del retrato
CARD_STEP = 0.055    # retraso entre líneas de la ficha


def _titlebar(profile: dict) -> str:
    """Cabecera de la ventana: tres marcas y el prompt."""
    dots = "".join(
        f'  <rect x="{PAD + index * 14}" y="19" width="7" height="7" rx="1.5" '
        f'fill="{color}"/>\n'
        for index, color in enumerate((theme.ACCENT, theme.BORDER, theme.BORDER))
    )
    return (
        dots
        + f'  <text x="{PAD + 56}" y="27" font-size="11" fill="{theme.TEXT_FAINT}">'
        f'{esc(profile["prompt"])} <tspan fill="{theme.ACCENT}">%</tspan> '
        f'{esc(profile["command"])}</text>\n'
        f'  <line x1="0" y1="{TITLEBAR}" x2="{WIDTH}" y2="{TITLEBAR}" '
        f'stroke="{theme.RULE}"/>\n'
    )


def _portrait(art: list, x: float, y: float, size: float) -> str:
    """El retrato se imprime fila por fila, de arriba abajo.

    Cada fila se revela con un recorte que barre de izquierda a derecha, como
    una impresora de texto. El recorte nace abierto y lo cierra un `<set>`:
    sin SMIL el retrato se ve completo en vez de desaparecer.
    """
    advance, line_height = size * ADVANCE, size * LINE
    parts, clips = [], []
    for index, line in enumerate(art):
        if not line.strip():
            continue
        width = len(line) * advance
        top = y + index * line_height
        begin = round(TYPE_START + index * TYPE_STEP, 3)
        clips.append(
            f'    <clipPath id="fila{index}">\n'
            f'      <rect x="{x}" y="{top - size:.1f}" width="{width:.1f}" '
            f'height="{line_height + 2:.1f}">\n'
            f'        <set attributeName="width" to="0" begin="0s"/>\n'
            f'        <animate attributeName="width" from="0" to="{width:.1f}" '
            f'begin="{begin}s" dur="0.32s" fill="freeze"/>\n'
            "      </rect>\n"
            "    </clipPath>\n"
        )
        parts.append(
            f'  <text x="{x}" y="{top:.1f}" font-size="{size:.2f}" '
            f'fill="{theme.TEXT_DIM}" xml:space="preserve" '
            f'clip-path="url(#fila{index})">{esc(line)}</text>\n'
        )
    return "  <defs>\n" + "".join(clips) + "  </defs>\n" + "".join(parts)


def _card(panels: list, x: float, y: float) -> str:
    """Ficha estilo neofetch: secciones con filas de etiqueta y valor."""
    out = []
    cursor = y
    order = 0
    for group in panels:
        delay = round(1.15 + order * CARD_STEP, 3)
        out.append(
            f'  <g>\n{fade_in(delay, 0.45, 4)}'
            f'    <text x="{x}" y="{cursor:.1f}" font-size="10" '
            f'fill="{theme.ACCENT}" letter-spacing="1.4">{esc(group["title"].upper())}</text>\n'
            f'    <line x1="{x + len(group["title"]) * 7.6 + 16}" y1="{cursor - 4:.1f}" '
            f'x2="{WIDTH - PAD}" y2="{cursor - 4:.1f}" stroke="{theme.RULE}"/>\n'
            "  </g>\n"
        )
        order += 1
        cursor += HEADER

        for key, value in group["rows"]:
            delay = round(1.15 + order * CARD_STEP, 3)
            out.append(
                f'  <g>\n{fade_in(delay, 0.45, 4)}'
                f'    <text x="{x}" y="{cursor:.1f}" font-size="11" '
                f'fill="{theme.TEXT_FAINT}">{esc(key)}</text>\n'
                f'    <text x="{x + KEY_COLUMN}" y="{cursor:.1f}" font-size="11" '
                f'fill="{theme.TEXT}">{esc(value)}</text>\n'
                "  </g>\n"
            )
            order += 1
            cursor += ROW
        cursor += PANEL_GAP
    return "".join(out), cursor


def render(profile: dict, portrait: dict) -> str:
    """Devuelve el SVG completo de la consola."""
    art = portrait["art"]
    body_top = TITLEBAR + 26
    card, card_bottom = _card(profile["panels"], PAD + ART_BOX + 24, body_top + 10)
    card_height = card_bottom - body_top

    # El retrato manda: crece hasta llenar el ancho reservado y solo se frena
    # en su alto máximo. Atarlo a la altura de la ficha lo encogía cada vez que
    # se quitaba una fila de texto, que es justo al revés de lo que importa.
    size = min(ART_BOX / (portrait["columns"] * ADVANCE),
               ART_MAX / (len(art) * LINE))
    art_height = len(art) * size * LINE
    art_width = portrait["columns"] * size * ADVANCE

    height = int(body_top + max(art_height, card_height) + 20)
    art_x = PAD + (ART_BOX - art_width) / 2
    art_y = body_top + (max(art_height, card_height) - art_height) / 2 + size

    resumen = " · ".join(
        f"{key}: {value}" for group in profile["panels"] for key, value in group["rows"]
    )
    body = (
        panel(WIDTH, height)
        + _titlebar(profile)
        + _portrait(art, art_x, art_y, size)
        + card
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="title desc" '
        f'font-family="{theme.MONO}">\n'
        f'  <title id="title">{esc(profile["name"])} — consola de perfil</title>\n'
        f'  <desc id="desc">Retrato en ASCII junto a una ficha de sistema. '
        f'{esc(resumen)}.</desc>\n'
        f"{body}"
        "</svg>\n"
    )


def load(path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
