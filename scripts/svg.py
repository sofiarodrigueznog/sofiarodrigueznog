"""Piezas compartidas por todos los SVG del perfil.

Solo lo que de verdad se repite: escapado, el marco del panel y el documento.
Cada renderizador escribe su propio contenido.
"""

import theme


def esc(text: str) -> str:
    """Escapa texto para incrustarlo en XML."""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def document(width: int, height: int, title: str, desc: str, body: str) -> str:
    """Envuelve el contenido en un SVG accesible y autocontenido.

    `role="img"` mas `<title>`/`<desc>` dan a los lectores de pantalla el mismo
    contenido que ve el resto: el SVG no depende de su alt text.
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-labelledby="title desc" font-family="{theme.MONO}">\n'
        f"  <title id=\"title\">{esc(title)}</title>\n"
        f"  <desc id=\"desc\">{esc(desc)}</desc>\n"
        f"{body}"
        "</svg>\n"
    )


def panel(width: int, height: int) -> str:
    """Marco del sistema: fondo propio mas un borde de 1px.

    El +0.5 alinea el trazo a la grilla de pixeles para que no se vea difuso.
    """
    return (
        f'  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" '
        f'rx="{theme.RADIUS}" fill="{theme.BACKDROP}" stroke="{theme.BORDER}"/>\n'
    )


def fade_in(delay: float, duration: float = 0.5, shift: int = 6) -> str:
    """Aparición: opacidad mas un desplazamiento vertical mínimo.

    El elemento es visible en su estado base y es `<set>` quien lo esconde para
    que la animación empiece. Así, un renderizador que ignore SMIL —una
    miniatura, una vista previa— muestra el contenido completo en vez de un
    rectángulo vacío: la animación mejora la lectura, nunca es requisito.

    `fill="freeze"` congela el estado final: ocurre una vez y queda estática.
    """
    return (
        '    <set attributeName="opacity" to="0" begin="0s"/>\n'
        f'    <animate attributeName="opacity" from="0" to="1" begin="{delay}s" '
        f'dur="{duration}s" fill="freeze"/>\n'
        f'    <animateTransform attributeName="transform" type="translate" '
        f'from="0 {shift}" to="0 0" begin="{delay}s" dur="{duration}s" '
        f'calcMode="spline" keySplines="0.16 1 0.3 1" fill="freeze"/>\n'
    )
