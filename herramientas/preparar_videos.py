"""Copia los videos del evento a sitio/videos/ con nombres descriptivos y crea una
miniatura (poster) para cada uno en sitio/img/. Los originales no se modifican.
Los videos de WhatsApp ya vienen en H.264, que cualquier navegador reproduce:
no hace falta convertirlos."""
import os
import shutil
import cv2
import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(RAIZ, "archivos")
VIDEOS = os.path.join(RAIZ, "sitio", "videos")
IMG = os.path.join(RAIZ, "sitio", "img")
FV, OV = "fotos y videos", "otras fotos y videos"

# nombre de salida: (ruta relativa a archivos/, posición del fotograma para la miniatura)
LISTA = {
    "01-llegada-agora": (f"{OV}/WhatsApp Video 2026-10-05 at 11.38.29 PM (1).mp4", 0.6),
    "02-bienvenida-publico": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.35 PM.mp4", 0.5),
    "03-bienvenida-escenario": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.34 PM.mp4", 0.5),
    "04-auditorio-lleno": (f"{FV}/WhatsApp Video 2026-10-05 at 11.23.10 PM.mp4", 0.2),
    "05-sig-mundo-inteligente": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.33 PM (2).mp4", 0.35),
    "06-plataforma-arcgis": (f"{FV}/WhatsApp Video 2026-10-05 at 11.23.11 PM (1).mp4", 0.6),
    "07-casos-emergencias": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.32 PM (1).mp4", 0.35),
    "08-casos-movilidad": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.32 PM (2).mp4", 0.35),
    "09-equipo-esri": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.33 PM.mp4", 0.35),
    "10-lemos-inteligencia": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.33 PM (1).mp4", 0.1),
    "11-chivite-presentacion": (f"{FV}/WhatsApp Video 2026-10-05 at 11.23.11 PM.mp4", 0.2),
    "12-chivite-demo-ia": (f"{OV}/WhatsApp Video 2026-10-05 at 11.38.28 PM (1).mp4", 0.6),
    "13-covelli-hola": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.34 PM (2).mp4", 0.35),
    "14-covelli-territorio": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.33 PM (3).mp4", 0.35),
    "15-covelli-aprendemos": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.34 PM (1).mp4", 0.35),
    "16-premio-sag-upme": (f"{FV}/WhatsApp Video 2026-10-05 at 11.24.32 PM.mp4", 0.6),
    "17-satelite-planet": (f"{OV}/WhatsApp Video 2026-10-05 at 11.38.25 PM.mp4", 0.9),
    "18-ecocomputo": (f"{OV}/WhatsApp Video 2026-10-05 at 11.38.27 PM.mp4", 0.35),
    "19-recorrido-dani": (f"{OV}/WhatsApp Video 2026-10-05 at 11.38.30 PM.mp4", 0.6),
}

os.makedirs(VIDEOS, exist_ok=True)
total = 0
for nombre, (rel, pos) in LISTA.items():
    origen = os.path.join(A, rel)
    destino = os.path.join(VIDEOS, nombre + ".mp4")
    if not os.path.exists(destino) or os.path.getsize(destino) != os.path.getsize(origen):
        shutil.copy2(origen, destino)
    total += os.path.getsize(destino)

    cap = cv2.VideoCapture(origen)
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * pos))
    ok, img = cap.read()
    if ok:
        h, w = img.shape[:2]
        s = 480 / max(h, w)
        img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
        cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 60])[1].tofile(os.path.join(IMG, "vp-" + nombre + ".jpg"))
    print(f"{nombre}.mp4")
print(f"{len(LISTA)} videos en sitio/videos/ ({total / 1e6:.0f} MB)")
