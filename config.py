import os

# ==================
# Ventana y FPS
# ==================
WIDTH = 1400
HEIGHT = 950
FPS = 60
CAPTION = "Python Adventure Game"

# ==================
# Colores
# =================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (40, 40, 40)
GRIS_CLARO = (200, 200, 200)
GRIS_OSCURO = (30, 30, 30)
ROJO = (255, 0, 0)
VERDE = (0, 200, 0)
ROJO_FALLO = (255, 100, 100)
NARANJA = (230, 150, 60)

# Colores para el panel del playground
PANEL_BG = (245, 245, 245)
PANEL_BORDER = (170, 170, 170)
CODE_BG = BLANCO

# Rutas de assets
RUTA_ASSETS = "assets"
RUTA_FONDOS = os.path.join(RUTA_ASSETS, "fondos")
RUTA_PERSONAJES = os.path.join(RUTA_ASSETS, "personajes")
RUTA_MUSICA = os.path.join(RUTA_ASSETS, "musica")
RUTA_ICONO = os.path.join(RUTA_ASSETS, "icono")
