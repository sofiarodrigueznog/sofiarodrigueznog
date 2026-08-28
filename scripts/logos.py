"""Descarga las marcas del stack y las deja cacheadas en el repositorio.

Las siluetas vienen de Simple Icons (CC0), que las publica ya monocromas en un
lienzo de 24×24: exactamente lo que necesita este diseño.

    python3 scripts/logos.py

Se ejecuta a mano, como el retrato. El resultado queda en `data/logos.json` y
se versiona, así que el SVG publicado no pide nada a ningún servidor y el
workflow diario sigue sin depender de la red más que para el calendario.

Una tecnología sin marca disponible —C#, por ejemplo, retirado del catálogo— no
es un error: se dibuja como un token de texto, que en una consola se lee igual
de bien.
"""

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SOURCE = "https://raw.githubusercontent.com/simple-icons/simple-icons/master/icons/{slug}.svg"
USER_AGENT = "sofiarodrigueznog-profile/1.0 (+https://github.com/sofiarodrigueznog)"

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "data" / "profile.json"
CACHE = ROOT / "data" / "logos.json"


def fetch(slug: str) -> str:
    """Devuelve el trazado de una marca, ya normalizado a 24×24."""
    request = urllib.request.Request(
        SOURCE.format(slug=slug), headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        svg = response.read().decode("utf-8")

    inicio = svg.index(' d="', svg.index("<path")) + 4
    return svg[inicio:svg.index('"', inicio)]


def main() -> int:
    profile = json.loads(PROFILE.read_text(encoding="utf-8"))
    slugs = [slug for group in profile["stack"] for slug, _ in group["items"] if slug]

    paths, faltan = {}, []
    for slug in slugs:
        try:
            paths[slug] = fetch(slug)
            print(f"  ✓ {slug}")
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as error:
            faltan.append(slug)
            print(f"  ✗ {slug}: {error}", file=sys.stderr)

    if faltan:
        print(f"error: sin marca para {', '.join(faltan)}. Deja el slug vacío en "
              f"data/profile.json para dibujarlas como texto.", file=sys.stderr)
        return 1

    CACHE.write_text(
        json.dumps({"source": "https://simpleicons.org (CC0)", "paths": paths},
                   ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"· {len(paths)} marcas\n  ✎ {CACHE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
