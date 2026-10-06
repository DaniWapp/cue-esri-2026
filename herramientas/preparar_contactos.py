"""Recorta fotos de personas y logos de empresas (de las propias fotos del evento)
para la pestaña Contactos. Salida: sitio/img/c-*.jpg. Los originales no se modifican."""
import os
import cv2
import numpy as np

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
A = os.path.join(RAIZ, "archivos")
SALIDA = os.path.join(RAIZ, "sitio", "img")
STAND = "fyv/WhatsApp Image 2026-10-01 at 6.15.47 PM.jpeg"
BEST = "fotos-best/Diseño sin título ({}).png"

# nombre: (fuente, recorte en fracciones (x0, y0, x1, y1) del ancho/alto, tipo)
# tipo "foto" = cuadrado para avatar circular; "logo" = se centra sobre fondo claro
RECORTES = {
    "c-sierra":    (STAND, (0.150, 0.348, 0.280, 0.458), "foto"),
    "c-lemos":     (STAND, (0.367, 0.332, 0.487, 0.432), "foto"),
    "c-rector":    (STAND, (0.555, 0.380, 0.660, 0.465), "foto"),
    "c-penaranda": ("fyv/WhatsApp Image 2026-10-01 at 5.26.57 PM (1).jpeg", (0.000, 0.240, 0.097, 0.370), "foto"),
    "c-esri":      ("WhatsApp Image 2026-10-05 at 10.59.14 PM.jpeg", (0.12, 0.225, 0.80, 0.30), "logo"),
    "c-planeta":   (STAND, (0.48, 0.08, 0.74, 0.18), "logo"),
    "c-planet":    (BEST.format(35), (0.29, 0.005, 0.47, 0.06), "logo"),
    "c-procalculo": (BEST.format(35), (0.50, 0.025, 0.62, 0.08), "logo"),
    "c-dreamgis":  (BEST.format(27), (0.17, 0.38, 0.80, 0.56), "logo"),
    "c-ecompass":  (BEST.format(33), (0.15, 0.38, 0.83, 0.59), "logo"),
    "c-intelligis": (BEST.format(28), (0.25, 0.06, 0.71, 0.125), "logo"),
    "c-mpsig":     (BEST.format(26), (0.115, 0.455, 0.30, 0.57), "logo"),
    "c-unigis":    (BEST.format(34), (0.28, 0.31, 0.77, 0.65), "logo"),
    "c-synspective": (BEST.format(31), (0.05, 0.0, 0.34, 0.11), "logo"),
    "c-vantor":    (BEST.format(29), (0.07, 0.045, 0.32, 0.11), "logo"),
    "c-here":      (BEST.format(32), (0.82, 0.15, 0.98, 0.23), "logo"),
}


# fotos y logos aportados por Dani (archivos/fotos contacto/)
FC = "fotos contacto/"
RECORTES.update({
    "c-martha":    (FC + "Martha Lucía Arias.JPG", (0.29, 0.10, 0.68, 0.52), "foto"),
    "c-pedraza":   (FC + "carlos pedraza.jfif", (0.03, 0.06, 0.97, 1.0), "foto"),
    "c-perez":     (FC + "pedro fabian perez.jfif", (0.485, 0.12, 0.845, 0.48), "foto"),
    "c-helena":    (FC + "helena-gutierrez.jpg", (0.345, 0.06, 0.735, 0.53), "foto"),
    "c-natalia":   (FC + "natalia-villamizar.jpg", (0.36, 0.06, 0.71, 0.41), "foto"),
    "c-sabrina":   (FC + "sabrina gonzalez.jfif", (0.35, 0.045, 0.76, 0.455), "foto"),
    "c-covelli":   (FC + "Santiago-Covelli.jpg", (0.29, 0.0, 0.81, 0.40), "foto"),
    "c-unilibre":  (FC + "Escudo_de_la_Universidad_Libre_de_Colombia.svg.webp", (0, 0, 1, 1), "logo"),
    "c-lulo":      (FC + "lulo bank.jfif", (0, 0, 1, 1), "logo"),
})

# conferencistas: rostro tomado de un fotograma de video (ruta, posición 0–1)
FV = "fotos y videos/WhatsApp Video 2026-10-05 at "
VIDEO = {
    "c-chivite": ((FV + "11.23.11 PM.mp4", 0.1), (0.519, 0.20, 0.609, 0.36)),
}


def leer(ruta):
    if isinstance(ruta, tuple):
        cap = cv2.VideoCapture(os.path.join(A, ruta[0]))
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) * ruta[1]))
        return cap.read()[1]
    return cv2.imdecode(np.fromfile(ruta, dtype="uint8"), cv2.IMREAD_COLOR)


def recortar(img, fr):
    h, w = img.shape[:2]
    x0, y0, x1, y1 = fr
    return img[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]


RECORTES.update({k: (v[0], v[1], "foto") for k, v in VIDEO.items()})

for nombre, (fuente, fr, tipo) in RECORTES.items():
    c = recortar(leer(fuente if isinstance(fuente, tuple) else os.path.join(A, fuente)), fr)
    if tipo == "foto":
        lado = min(c.shape[:2])
        y, x = (c.shape[0] - lado) // 2, (c.shape[1] - lado) // 2
        c = cv2.resize(c[y:y + lado, x:x + lado], (160, 160), interpolation=cv2.INTER_AREA)
    else:
        h, w = c.shape[:2]
        s = min(300 / w, 120 / h)
        c = cv2.resize(c, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    cv2.imencode(".jpg", c, [cv2.IMWRITE_JPEG_QUALITY, 80])[1].tofile(os.path.join(SALIDA, nombre + ".jpg"))
    print(nombre, c.shape[1], "x", c.shape[0])
