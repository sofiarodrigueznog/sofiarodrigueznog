"""Dibuja el panel de tecnologías: una marca por herramienta.

Las siluetas llegan cacheadas desde `data/logos.json`; este módulo solo las
coloca. Van todas del mismo color a propósito: la paleta del perfil vive de un
único acento, y diecinueve logos con sus colores de marca la harían estallar.
Monocromas siguen siendo reconocibles —es justo la premisa de Simple Icons— y
además se leen igual sobre el modo claro y el oscuro.
"""

import json

import theme
from svg import document, esc, fade_in, panel

WIDTH = 768
PAD = 24

LABEL_COLUMN = 96    # ancho de la etiqueta de grupo
CELL = 56            # separación entre marcas
GLYPH = 22           # lado de la marca
ROW = 50             # separación entre filas
TOP = 78             # primera fila

REVEAL_START = 0.2
REVEAL_STEP = 0.035


def _mark(slug: str, label: str, x: float, y: float, paths: dict) -> str:
    """Una marca, o un token de texto si esa tecnología no tiene silueta."""
    if slug and slug in paths:
        escala = GLYPH / 24
        figura = (
            f'    <g transform="translate({x:.1f} {y:.1f}) scale({escala:.4f})">\n'
            f'      <path d="{paths[slug]}" fill="{theme.TEXT_DIM}"/>\n'
            "    </g>\n"
        )
    else:
        figura = (
            f'    <rect x="{x:.1f}" y="{y:.1f}" width="{GLYPH}" height="{GLYPH}" '
            f'rx="5" fill="none" stroke="{theme.BORDER}"/>\n'
            f'    <text x="{x + GLYPH / 2:.1f}" y="{y + GLYPH / 2 + 3.6:.1f}" '
            f'font-size="10" fill="{theme.TEXT_DIM}" text-anchor="middle">'
            f"{esc(label)}</text>\n"
        )

    return figura + (
        f'    <text x="{x + GLYPH / 2:.1f}" y="{y + GLYPH + 11:.1f}" font-size="7.5" '
        f'fill="{theme.TEXT_FAINT}" text-anchor="middle">{esc(label)}</text>\n'
    )


def render(profile: dict, logos: dict) -> str:
    """Devuelve el SVG del panel de tecnologías."""
    paths = logos["paths"]
    grupos = profile["stack"]
    height = TOP + (len(grupos) - 1) * ROW + GLYPH + 20 + PAD

    cuerpo = [
        panel(WIDTH, height),
        f'  <text x="{PAD}" y="42" font-size="12" fill="{theme.TEXT}" '
        f'letter-spacing="1.6">stack</text>\n',
        f'  <line x1="{PAD}" y1="58" x2="{WIDTH - PAD}" y2="58" '
        f'stroke="{theme.RULE}"/>\n',
    ]

    orden = 0
    for fila, grupo in enumerate(grupos):
        y = TOP + fila * ROW
        cuerpo.append(
            f'  <text x="{PAD}" y="{y + 15}" font-size="11" '
            f'fill="{theme.TEXT_FAINT}">{esc(grupo["title"])}</text>\n'
        )
        for columna, (slug, label) in enumerate(grupo["items"]):
            x = PAD + LABEL_COLUMN + columna * CELL
            retraso = round(REVEAL_START + orden * REVEAL_STEP, 3)
            cuerpo.append(
                f"  <g>\n{fade_in(retraso, 0.4, 5)}"
                + _mark(slug, label, x, y, paths)
                + "  </g>\n"
            )
            orden += 1

    resumen = "; ".join(
        f"{grupo['title']}: " + ", ".join(label for _, label in grupo["items"])
        for grupo in grupos
    )
    return document(
        WIDTH,
        height,
        "Tecnologías",
        f"Marcas de las herramientas que uso. {resumen}.",
        "".join(cuerpo),
    )


def load(path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)
