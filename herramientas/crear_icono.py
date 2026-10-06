"""Crea sitio/favicon.ico: globo azul con meridianos y un punto verde (Cúcuta).
El .ico contiene versiones PNG de 16, 32, 48 y 256 px."""
import os
import struct
import cv2
import numpy as np

SITIO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
S = 1024  # se dibuja grande y se reduce para suavizar bordes
AZUL, BLANCO, VERDE = (193, 121, 0, 255), (255, 255, 255, 255), (55, 139, 61, 255)  # BGRA

img = np.zeros((S, S, 4), np.uint8)
c, r = S // 2, int(S * 0.46)
cv2.circle(img, (c, c), r, AZUL, -1, cv2.LINE_AA)
g = int(S * 0.035)
cv2.circle(img, (c, c), int(r * 0.78), BLANCO, g, cv2.LINE_AA)                       # contorno del globo
cv2.ellipse(img, (c, c), (int(r * 0.34), int(r * 0.78)), 0, 0, 360, BLANCO, g, cv2.LINE_AA)  # meridiano
cv2.line(img, (c - int(r * 0.78), c), (c + int(r * 0.78), c), BLANCO, g, cv2.LINE_AA)   # ecuador
cv2.ellipse(img, (c, c - int(r * 0.42)), (int(r * 0.62), int(r * 0.14)), 0, 0, 180, BLANCO, g, cv2.LINE_AA)
cv2.circle(img, (c + int(r * 0.38), c + int(r * 0.36)), int(r * 0.2), BLANCO, -1, cv2.LINE_AA)  # borde del punto
cv2.circle(img, (c + int(r * 0.38), c + int(r * 0.36)), int(r * 0.14), VERDE, -1, cv2.LINE_AA)

tamanos = [16, 32, 48, 256]
pngs = [cv2.imencode(".png", cv2.resize(img, (t, t), interpolation=cv2.INTER_AREA))[1].tobytes() for t in tamanos]

cabecera = struct.pack("<HHH", 0, 1, len(pngs))
desplazamiento = 6 + 16 * len(pngs)
entradas, datos = b"", b""
for t, png in zip(tamanos, pngs):
    lado = 0 if t == 256 else t
    entradas += struct.pack("<BBBBHHII", lado, lado, 0, 0, 1, 32, len(png), desplazamiento + len(datos))
    datos += png

ruta = os.path.join(SITIO, "favicon.ico")
with open(ruta, "wb") as f:
    f.write(cabecera + entradas + datos)
print(f"favicon.ico creado ({os.path.getsize(ruta)} bytes)")
