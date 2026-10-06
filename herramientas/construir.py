"""Genera sitio/index.html (un solo archivo, funciona sin internet) a partir de
sitio/index.src.html incrustando las imágenes de sitio/img/ en base64."""
import base64
import os
import re

SITIO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FUENTE = os.path.join(SITIO, "index.src.html")
DESTINO = os.path.join(SITIO, "index.html")


def incrustar(m):
    atributo, ruta = m.group(1), os.path.join(SITIO, m.group(2))
    with open(ruta, "rb") as f:
        datos = base64.b64encode(f.read()).decode("ascii")
    return f'{atributo}="data:image/jpeg;base64,{datos}"'


with open(FUENTE, encoding="utf-8") as f:
    html = f.read()

IMAGEN = r'(src|poster)="(img/[^"]+\.jpg)"'
faltan = [p for _, p in re.findall(IMAGEN, html) if not os.path.exists(os.path.join(SITIO, p))]
faltan += [p for p in re.findall(r'src="(videos/[^"]+\.mp4)"', html) if not os.path.exists(os.path.join(SITIO, p))]
if faltan:
    raise SystemExit("Faltan archivos: " + ", ".join(faltan))

# las imágenes se incrustan; los videos quedan como archivos aparte en sitio/videos/
html = re.sub(IMAGEN, incrustar, html)

# ícono de la pestaña del navegador
with open(os.path.join(SITIO, "favicon.ico"), "rb") as f:
    ico = base64.b64encode(f.read()).decode("ascii")
html = html.replace('href="favicon.ico"', f'href="data:image/x-icon;base64,{ico}"')
with open(DESTINO, "w", encoding="utf-8") as f:
    f.write(html)
print(f"index.html generado: {os.path.getsize(DESTINO) / 1024 / 1024:.1f} MB")
