"""Copia optimizada de fotos y fotogramas de video para el sitio (no modifica los originales)."""
import os
import cv2

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(RAIZ, "archivos")
SALIDA = os.path.join(RAIZ, "sitio", "img")
MAX_LADO = 1400
CALIDAD = 72

R_CW, R_CCW, R_180 = cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180
ESPEJO = "espejo"  # selfies guardadas en espejo: se voltean horizontalmente para que el texto se lea bien

# nombre de salida: (ruta relativa a archivos/, rotación o ESPEJO)
FOTOS = {
    "hero-delegacion": ("fyv/WhatsApp Image 2026-10-01 at 5.26.57 PM (1).jpeg", None),
    "dani-planet": ("fotos-best/Diseño sin título (35).png", None),
    "aeropuerto": ("fotos-best/Diseño sin título (36).png", None),
    "delegacion-auditorio": ("fyv/WhatsApp Image 2026-10-01 at 10.26.00 AM.jpeg", None),
    "auditorio-velocity": ("fyv/WhatsApp Image 2026-10-01 at 10.24.51 AM.jpeg", None),
    "auditorio-emergencias": ("fyv/WhatsApp Image 2026-10-01 at 9.37.08 AM.jpeg", None),
    "planeta-stand": ("fyv/WhatsApp Image 2026-10-01 at 6.15.47 PM.jpeg", None),
    "equipo-esri": ("otras fotos y videos/WhatsApp Image 2026-10-05 at 11.38.18 PM.jpeg", None),
    "selfie-escenario": ("fotos y videos/WhatsApp Image 2026-10-05 at 11.23.09 PM.jpeg", ESPEJO),
    "semillero-escenario": ("otras fotos y videos/WhatsApp Image 2026-10-05 at 11.38.14 PM.jpeg", None),
    "escarapela": ("WhatsApp Image 2026-10-05 at 10.59.14 PM.jpeg", None),
    "app-talleres": ("WhatsApp Image 2026-10-04 at 2.57.19 AM.jpeg", None),
    "ecocomputo": ("otras fotos y videos/WhatsApp Image 2026-10-05 at 11.38.26 PM.jpeg", None),
    "refrigerio": ("fyv/WhatsApp Image 2026-10-01 at 10.06.18 AM.jpeg", None),
    # material de partners (sin tarjetas personales)
    "p-intelligis": ("fotos-best/Diseño sin título (28).png", None),
    "p-mpsig": ("fotos-best/Diseño sin título (26).png", None),
    "p-unigis": ("fotos-best/Diseño sin título (34).png", None),
    "p-synspective": ("fotos-best/Diseño sin título (31).png", None),
    "p-here": ("fotos-best/Diseño sin título (32).png", None),
    "p-vantor": ("fotos-best/Diseño sin título (29).png", None),
    "p-dreamgis": ("fotos-best/Diseño sin título (27).png", None),
    "p-ecompass": ("fotos-best/Diseño sin título (33).png", None),
    "p-planet": ("fotos y videos/WhatsApp Image 2026-10-05 at 11.23.09 PM (2).jpeg", None),
}

# nombre de salida: (video relativo a archivos/, posición 0–1)
FOTOGRAMAS = {
    "v-arcgis": ("fotos y videos/WhatsApp Video 2026-10-05 at 11.23.11 PM (1).mp4", 0.6),
    "v-emergencias": ("fotos y videos/WhatsApp Video 2026-10-05 at 11.24.32 PM (1).mp4", 0.35),
    "v-movilidad": ("fotos y videos/WhatsApp Video 2026-10-05 at 11.24.32 PM (2).mp4", 0.35),
    "v-sag": ("fotos y videos/WhatsApp Video 2026-10-05 at 11.24.32 PM.mp4", 0.6),
    "v-chivite-demo": ("otras fotos y videos/WhatsApp Video 2026-10-05 at 11.38.28 PM (1).mp4", 0.6),
    "v-lemos": ("fotos y videos/WhatsApp Video 2026-10-05 at 11.24.33 PM (1).mp4", 0.1),
    "v-covelli": ("fotos y videos/WhatsApp Video 2026-10-05 at 11.24.34 PM (2).mp4", 0.35),
    "v-agora": ("otras fotos y videos/WhatsApp Video 2026-10-05 at 11.38.29 PM (1).mp4", 0.6),
}


def guardar(nombre, img):
    h, w = img.shape[:2]
    s = min(1.0, MAX_LADO / max(h, w))
    if s < 1:
        img = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    ruta = os.path.join(SALIDA, nombre + ".jpg")
    cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, CALIDAD])[1].tofile(ruta)
    print(f"{nombre}.jpg  {img.shape[1]}x{img.shape[0]}  {os.path.getsize(ruta)//1024} KB")


def leer(ruta):
    import numpy as np
    return cv2.imdecode(np.fromfile(ruta, dtype="uint8"), cv2.IMREAD_COLOR)


os.makedirs(SALIDA, exist_ok=True)
for nombre, (rel, rot) in FOTOS.items():
    img = leer(os.path.join(A, rel))
    if rot == ESPEJO:
        img = cv2.flip(img, 1)
    elif rot is not None:
        img = cv2.rotate(img, rot)
    guardar(nombre, img)

for nombre, (rel, pos) in FOTOGRAMAS.items():
    cap = cv2.VideoCapture(os.path.join(A, rel))
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * pos))
    ok, img = cap.read()
    if ok:
        guardar(nombre, img)
