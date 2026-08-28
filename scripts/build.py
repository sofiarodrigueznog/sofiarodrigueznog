#!/usr/bin/env python3
"""Genera los recursos visuales del perfil.

    python3 scripts/build.py              # descarga la actividad y dibuja todo
    python3 scripts/build.py --offline    # redibuja con los datos ya guardados

Es el único punto de entrada: obtener datos, guardarlos y dibujar son tres
responsabilidades separadas en tres módulos, y este las coordina.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import contributions  # noqa: E402
import heatmap  # noqa: E402
import stack  # noqa: E402
import console  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CALENDAR = ROOT / "data" / "contributions.json"
PROFILE = ROOT / "data" / "profile.json"
PORTRAIT = ROOT / "data" / "portrait.json"
LOGOS = ROOT / "data" / "logos.json"
ASSETS = ROOT / "assets"

USER = "sofiarodrigueznog"


def write(path: Path, content: str) -> None:
    """Escribe solo si el contenido cambió.

    Es lo que evita que el workflow genere un commit diario sin novedad: la
    historia del repositorio refleja actividad real, no la ejecución del cron.
    """
    if path.exists() and path.read_text(encoding="utf-8") == content:
        print(f"  = {path.relative_to(ROOT)}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"  ✎ {path.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--offline",
        action="store_true",
        help="no consulta GitHub: redibuja con data/contributions.json",
    )
    parser.add_argument("--user", default=USER, help="cuenta de GitHub a consultar")
    args = parser.parse_args()

    if args.offline:
        if not CALENDAR.exists():
            print(f"error: no hay datos en {CALENDAR}", file=sys.stderr)
            return 1
        calendar = contributions.load(CALENDAR)
        print(f"· actividad desde caché ({calendar['total']} contribuciones)")
    else:
        try:
            calendar = contributions.collect(args.user)
        except contributions.FetchError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        print(f"· actividad de {args.user}: {calendar['total']} contribuciones")
        contributions.save(calendar, CALENDAR)

    ASSETS.mkdir(exist_ok=True)
    write(ASSETS / "activity.svg", heatmap.render(calendar))
    write(
        ASSETS / "stack.svg",
        stack.render(stack.load(PROFILE), stack.load(LOGOS)),
    )
    write(
        ASSETS / "console.svg",
        console.render(console.load(PROFILE), console.load(PORTRAIT)),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
