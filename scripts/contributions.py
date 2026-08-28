"""Obtiene el calendario real de contribuciones de GitHub.

Fuente: el fragmento HTML que github.com sirve públicamente para el propio
calendario del perfil. No hay servicio de estadísticas de terceros, no hay
token y no hay dependencias fuera de la librería estándar.

Este módulo no sabe nada de SVG: solo devuelve datos.
"""

import json
import re
import urllib.error
import urllib.request

URL = "https://github.com/users/{user}/contributions"
USER_AGENT = "sofiarodrigueznog-profile/1.0 (+https://github.com/sofiarodrigueznog)"

WEEKS = 53
DAYS = 7

# <td ... data-date="2025-10-13" ... data-level="3" ...>, en cualquier orden.
_CELL = re.compile(
    r'<td[^>]*\bid="contribution-day-component-(?P<row>\d+)-(?P<col>\d+)"[^>]*>',
)
_DATE = re.compile(r'data-date="(\d{4}-\d{2}-\d{2})"')
_LEVEL = re.compile(r'data-level="(\d+)"')
_TIP = re.compile(
    r'<tool-tip[^>]*\bfor="(contribution-day-component-\d+-\d+)"[^>]*>(.*?)</tool-tip>',
    re.S,
)
_COUNT = re.compile(r"^\s*([\d,]+)\s+contribution")


class FetchError(RuntimeError):
    """El calendario no se pudo obtener o no se pudo interpretar."""


def fetch(user: str, timeout: int = 20) -> str:
    """Descarga el HTML del calendario."""
    request = urllib.request.Request(
        URL.format(user=user), headers={"User-Agent": USER_AGENT, "Accept": "text/html"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as error:
        raise FetchError(f"no se pudo consultar el calendario de {user}: {error}")


def parse(html: str) -> dict:
    """Convierte el HTML en la grilla de 53 semanas x 7 dias.

    Cada celda trae su fecha, su nivel (0-4, el mismo que usa GitHub) y el
    número real de contribuciones, que vive en el tooltip.
    """
    counts = {}
    for cell_id, tip in _TIP.findall(html):
        match = _COUNT.match(re.sub(r"<[^>]+>", "", tip).strip())
        counts[cell_id] = int(match.group(1).replace(",", "")) if match else 0

    grid = [[None] * WEEKS for _ in range(DAYS)]
    found = 0
    for match in _CELL.finditer(html):
        tag = match.group(0)
        day = _DATE.search(tag)
        level = _LEVEL.search(tag)
        if not day or not level:
            continue
        row, col = int(match.group("row")), int(match.group("col"))
        if not (0 <= row < DAYS and 0 <= col < WEEKS):
            continue
        cell_id = f"contribution-day-component-{row}-{col}"
        grid[row][col] = {
            "date": day.group(1),
            "count": counts.get(cell_id, 0),
            "level": int(level.group(1)),
        }
        found += 1

    if found < WEEKS * DAYS * 0.8:
        raise FetchError(f"calendario incompleto: solo {found} dias reconocidos")

    days = [cell for row in grid for cell in row if cell]
    days.sort(key=lambda cell: cell["date"])
    return {
        "grid": grid,
        "total": sum(cell["count"] for cell in days),
        "busiest": max(cell["count"] for cell in days),
        "active_days": sum(1 for cell in days if cell["count"]),
        "start": days[0]["date"],
        "end": days[-1]["date"],
    }


def load(path) -> dict:
    """Lee el calendario ya guardado en disco."""
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(data: dict, path) -> None:
    """Guarda el calendario de forma estable: mismo dato, mismo archivo.

    Sin marca de tiempo a proposito. Asi el workflow solo genera un commit
    cuando la actividad cambia de verdad, y no uno diario vacio.
    """
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=1, sort_keys=True)
        handle.write("\n")


def collect(user: str) -> dict:
    """Descarga y parsea en un solo paso."""
    return parse(fetch(user))


if __name__ == "__main__":  # comprobación manual rápida
    import sys

    result = collect(sys.argv[1] if len(sys.argv) > 1 else "sofiarodrigueznog")
    print(
        f"{result['total']} contribuciones entre {result['start']} y {result['end']}"
        f" · {result['active_days']} dias activos · maximo {result['busiest']}"
    )
