#!/usr/bin/env python3
"""Regenera portfolio.html a partir de portfolio_template.html: injeta o CSS
compilado do Tailwind (tw/output.css) e embute as imagens de src/images/ como
data URIs no lugar dos placeholders IMG:<nome>."""
import base64
import re
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "portfolio_template.html"
TAILWIND_CSS = HERE / "tw" / "output.css"
IMAGES_DIR = HERE / "images"
OUTPUT = HERE.parent / "index.html"

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def main():
    html = TEMPLATE.read_text(encoding="utf-8")
    tw_css = TAILWIND_CSS.read_text(encoding="utf-8")

    marker = "<!-- TAILWIND -->"
    assert marker in html, "marcador <!-- TAILWIND --> não encontrado no template"
    html = html.replace(marker, f"<style>{tw_css}</style>")

    def repl(m):
        key = m.group(1)
        for ext, mime in MIME.items():
            path = IMAGES_DIR / f"{key}{ext}"
            if path.exists():
                data = base64.b64encode(path.read_bytes()).decode("ascii")
                return f"data:{mime};base64,{data}"
        raise SystemExit(f"imagem não encontrada para o placeholder: {key}")

    html2 = re.sub(r"IMG:([a-zA-Z0-9_]+)", repl, html)
    assert "IMG:" not in html2, "sobrou placeholder sem imagem"

    OUTPUT.write_text(html2, encoding="utf-8")
    print(f"OK — {OUTPUT} ({len(html2)} bytes)")


if __name__ == "__main__":
    main()
