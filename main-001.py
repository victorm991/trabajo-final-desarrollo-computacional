import pygame
import sys
import os

pygame.init()

# =====================
# Configuración básica
# =====================
WIDTH, HEIGHT = 1000, 800
TAMANO_BOTON = (350, 150)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Adventure Game")
clock = pygame.time.Clock()
FPS = 60

# ================
# Colores
# ================
NEGRO = (0, 0, 0)
BLANCO = (255,225,255)
ROJO_FALLO = (255,100,100)

# ====================
# Fuentes
# ====================
try:
    fuente_titulo = pygame.font.SysFont("consolas", 40, bold=True)
    fuente_texto = pygame.font.SysFont("consolas", 20)
    fuente_pequena = pygame.font.SysFont("consolas", 16)
except pygame.error:
    print("Advertencia: Fuente consola no encontrada, usando fuente por default")
    fuente_titulo = pygame.font.Font(None, 40)
    fuente_texto = pygame.font.Font(None, 20)
    fuente_pequena = pygame.font.Font(None, 16)

# ====================
# Estado del juego
# ====================
ESTADO_MENU = "MENU"
ESTADO_SELECT_NIVEL = "SELECT_NIVEL"
ESTADO_PLAYGROUND = "PLAYGROUND"
estado_actual = ESTADO_MENU

# =====================
# Cargar imagen de fondo
# =====================
def cargar_imagen(ruta_base, nombre_archivo, tamanio=None, fallback_color=ROJO_FALLO):

    ruta_completa = os.path.join(ruta_base, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta_completa)
        imagen = imagen.convert_alpha()
        if tamanio:
            imagen = pygame.transform.scale(imagen, tamanio)
        return imagen
    
    except Exception as e:
        print(f"Error al sacar la imagen '{ruta_completa}': {e}")
        if tamanio:
            surf_fallback = pygame.Surface(tamanio)
        else:
            surf_fallback = pygame.Surface((200, 50))
        surf_fallback.fill(fallback_color)
        return surf_fallback

# ============
# Rutas base 
# ============
ruta_assets = "assets"
ruta_fondos = os.path.join(ruta_assets, "fondos")
ruta_botones = os.path.join(ruta_assets, "botones")

# -- Fondo ---
fondo_menu = cargar_imagen(ruta_fondos, "pantalla_inicial.png", (WIDTH, HEIGHT), NEGRO)

# --- Imagenes botones
img_boton_start = cargar_imagen(ruta_botones, "IniciarJuego.png", TAMANO_BOTON)
img_boton_start_hover = cargar_imagen(ruta_botones, "IniciarJuegoSelect.png", TAMANO_BOTON)

img_boton_Level1 = cargar_imagen(ruta_botones, "Nive-1.png", TAMANO_BOTON)
img_boton_Level1_hover = cargar_imagen(ruta_botones, "Nivel-1-Select.png", TAMANO_BOTON)

img_boton_Level2 = cargar_imagen(ruta_botones, "Nive-2.png", TAMANO_BOTON)
img_boton_Level2_hover = cargar_imagen(ruta_botones, "Nivel-2-Select.png", TAMANO_BOTON)

img_boton_Level3 = cargar_imagen(ruta_botones, "Nive-3.png", TAMANO_BOTON)
img_boton_Level3_hover = cargar_imagen(ruta_botones, "Nivel-3-Select.png", TAMANO_BOTON)

img_boton_instr = cargar_imagen(ruta_botones, "Instrucciones.png", TAMANO_BOTON)
img_boton_instr_hover = cargar_imagen(ruta_botones, "InstruccionesSelect.png", TAMANO_BOTON)

img_boton_cred = cargar_imagen(ruta_botones, "Creditos.png", TAMANO_BOTON)
img_boton_cred_hover = cargar_imagen(ruta_botones, "CreditosSelect.png", TAMANO_BOTON)

img_boton_salir = cargar_imagen(ruta_botones, "Salir.png", TAMANO_BOTON)
img_boton_salir_hover = cargar_imagen(ruta_botones, "SalirSelect.png", TAMANO_BOTON)

# =====================
# Clase boton
# =====================
class crear_boton:
    def __init__(self, img_normal, img_hover, x, y, texto_accion=""):
        self.img_normal = img_normal
        self.img_hover = img_hover
        self.image = img_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.texto_accion = texto_accion
    
    def actualizar(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.image = self.img_hover
        else:
            self.image = self.img_normal
    
    def dibujar_boton_pixel(self, surface):
        surface.blit(self.image, self.rect)

    def clic(self, pos):
        return self.rect.collidepoint(pos)

def crear_botones_centrados_menu(img_normal, img_hover, centro_y, texto_accion=""):
    w = img_normal.get_width()
    h = img_normal.get_height()
    x = WIDTH // 2 - w // 2
    y = centro_y - h // 2
    return crear_boton(img_normal, img_hover, x, y, texto_accion)

# =====================
# Botones menú
# =====================
boton_start = crear_botones_centrados_menu(img_boton_start, img_boton_start_hover, 490, "Iniciar")
boton_instr = crear_botones_centrados_menu(img_boton_instr, img_boton_instr_hover, 550, "instrucciones")
boton_cred = crear_botones_centrados_menu(img_boton_cred, img_boton_cred_hover, 610, "Créditos")
boton_salir = crear_botones_centrados_menu(img_boton_salir, img_boton_salir_hover, 670, "Salir")

botones_menu = [boton_start, boton_instr, boton_cred, boton_salir]

# =====================
# Botones selector nivel
# =====================
boton_nivel1 = crear_botones_centrados_menu(img_boton_Level1, img_boton_Level1_hover, 350, "Nivel1")
boton_nivel2 = crear_botones_centrados_menu(img_boton_Level2, img_boton_Level2_hover, 450, "Nivel2")
boton_nivel3 = crear_botones_centrados_menu(img_boton_Level3, img_boton_Level3_hover, 550, "Nivel3")
boton_atras  = crear_botones_centrados_menu(img_boton_salir, img_boton_salir_hover, 650, "Atras")

botones_selector = [boton_nivel1, boton_nivel2, boton_nivel3, boton_atras]

# ====================
# Dibujar pantallas
# ====================
def dibujar_pantalla_menu():
    screen.blit(fondo_menu, (0, 0))

    mx, my = pygame.mouse.get_pos()
    for boton in botones_menu:
        boton.actualizar((mx, my))
        boton.dibujar_boton_pixel(screen)

def dibujar_selector_nivel():
    screen.blit(fondo_menu, (0, 0))

    mx, my = pygame.mouse.get_pos()
    for boton in botones_selector:
        boton.actualizar((mx, my))
        boton.dibujar_boton_pixel(screen)

# ====================
# loop principal 
# ====================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # eventos MENU
        if estado_actual == ESTADO_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for boton in botones_menu:
                    if boton.clic((mx, my)):
                        if boton.texto_accion == "Iniciar":
                            estado_actual = ESTADO_SELECT_NIVEL
                        elif boton.texto_accion == "instrucciones":
                            print("Mostrar instrucciones")
                        elif boton.texto_accion == "Créditos":
                            print("Mostrar créditos")
                        elif boton.texto_accion == "Salir":
                            running = False

        # eventos SELECTOR DE NIVEL
        elif estado_actual == ESTADO_SELECT_NIVEL:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for boton in botones_selector:
                    if boton.clic((mx, my)):
                        
                        if boton.texto_accion == "Nivel1":
                            print("Cargar nivel 1")
                            estado_actual = ESTADO_PLAYGROUND

                        elif boton.texto_accion == "Nivel2":
                            print("Cargar nivel 2")
                            estado_actual = ESTADO_PLAYGROUND

                        elif boton.texto_accion == "Nivel3":
                            print("Cargar nivel 3")
                            estado_actual = ESTADO_PLAYGROUND

                        elif boton.texto_accion == "Atras":
                            estado_actual = ESTADO_MENU

        # eventos PLAYGROUND
        elif estado_actual == ESTADO_PLAYGROUND:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado_actual = ESTADO_MENU
    
    # =========================
    # Dibujar segun el estado
    # =========================
    if estado_actual == ESTADO_MENU:
        dibujar_pantalla_menu()

    elif estado_actual == ESTADO_SELECT_NIVEL:
        dibujar_selector_nivel()

    elif estado_actual == ESTADO_PLAYGROUND:
        screen.fill((20,20,20))
        texto = fuente_titulo.render("Pantalla de juego (ESC para volver)", True, BLANCO)
        screen.blit(texto, (200, 380))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()

