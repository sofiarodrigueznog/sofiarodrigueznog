"""Convierte una fotografía en un retrato ASCII.

Es el único script que necesita Pillow y el único que no corre en el workflow:
se ejecuta a mano cuando cambia la foto y deja el resultado en
`data/portrait.json`. Así el dibujo diario no arrastra ninguna dependencia.

    python3 scripts/portrait.py assets/retrato-fuente.jpg

Dos decisiones sostienen la calidad del retrato:

1. El fondo se recorta con un relleno por inundación desde los bordes. Solo se
   propaga por píxeles claros, así que la silueta oscura lo detiene sola y no
   hace falta una librería de segmentación.
2. El contraste se normaliza usando **solo** los píxeles del sujeto. Medido
   sobre la imagen completa, una figura oscura sobre fondo claro cae entera en
   el extremo denso de la rampa y se convierte en una mancha.
"""

import json
import sys
from collections import deque
from pathlib import Path

RAMP = " .:-=+*#%@"  # claro (disperso) → oscuro (denso)

COLUMNS = 72
CROP = (0.22, 0.02, 0.80, 0.56)  # encuadre de busto, en fracciones de la foto
ASPECT = 0.59                    # avance / interlineado de la monoespaciada
BACKGROUND = 95                  # a partir de aquí un píxel del borde es fondo


def _mask(pixels, cols, rows):
    """Marca el fondo: lo claro que se alcanza desde el borde."""
    background = [[False] * cols for _ in range(rows)]
    pending = deque()

    borde = [(x, y) for x in range(cols) for y in (0, rows - 1)]
    borde += [(x, y) for y in range(rows) for x in (0, cols - 1)]
    for x, y in borde:
        if pixels[x, y] >= BACKGROUND and not background[y][x]:
            background[y][x] = True
            pending.append((x, y))

    while pending:
        x, y = pending.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not background[ny][nx]:
                if pixels[nx, ny] >= BACKGROUND:
                    background[ny][nx] = True
                    pending.append((nx, ny))
    return background


def convert(photo: Path, cols: int = COLUMNS, crop=CROP) -> list:
    """Devuelve el retrato como una lista de filas de texto."""
    from PIL import Image  # local: el resto del proyecto no depende de Pillow

    image = Image.open(photo).convert("RGB")
    width, height = image.size
    image = image.crop((int(crop[0] * width), int(crop[1] * height),
                        int(crop[2] * width), int(crop[3] * height)))

    crop_w, crop_h = image.size
    rows = int(cols * (crop_h / crop_w) * ASPECT)
    grey = image.resize((cols, rows), Image.LANCZOS).convert("L")
    pixels = grey.load()

    background = _mask(pixels, cols, rows)

    subject = sorted(pixels[x, y] for y in range(rows) for x in range(cols)
                     if not background[y][x])
    if not subject:
        raise SystemExit("la máscara dejó el retrato vacío: revisa el encuadre")
    low = subject[len(subject) * 2 // 100]
    high = subject[len(subject) * 98 // 100]
    span = max(1, high - low)

    art = []
    for y in range(rows):
        line = ""
        for x in range(cols):
            if background[y][x]:
                line += " "
                continue
            value = min(1.0, max(0.0, (pixels[x, y] - low) / span))
            line += RAMP[int((1 - value) * (len(RAMP) - 1))]
        art.append(line)

    return _trim(art)


def _trim(art: list) -> list:
    """Recorta el dibujo a su propia tinta.

    El encuadre siempre deja aire alrededor del sujeto. Si ese aire viaja
    dentro del dato, quien dibuje después centra un rectángulo vacío en vez de
    un retrato, y no hay forma de calcular el cuerpo de letra correcto.
    """
    while art and not art[0].strip():
        art.pop(0)
    while art and not art[-1].strip():
        art.pop()
    if not art:
        return art

    izquierda = min(len(line) - len(line.lstrip()) for line in art if line.strip())
    return [line[izquierda:].rstrip() for line in art]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    photo = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "assets" / "retrato-fuente.jpg"
    if not photo.exists():
        print(f"error: no encuentro la foto en {photo}", file=sys.stderr)
        return 1

    art = convert(photo)
    destino = root / "data" / "portrait.json"
    destino.write_text(
        json.dumps({"columns": max(len(line) for line in art),
                    "rows": len(art), "art": art},
                   ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    cubierto = sum(len(line.strip()) for line in art)
    print(f"· retrato {max(len(l) for l in art)}×{len(art)} · {cubierto} caracteres con tinta")
    print(f"  ✎ {destino.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
