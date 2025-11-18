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

#================
# Colores
#================
NEGRO = (0, 0, 0)
BLANCO = (255,225,255)
ROJO_FALLO = (255,100,100)


# FUENTES
try:
    fuente_titulo = pygame.font.SysFont("consolas", 40, bold=True)
    fuente_texto = pygame.font.SysFont("consolas", 20)
    fuente_pequena = pygame.font.SysFont("consolas", 16)
except pygame.error:
    print("Advertencia: Fuente consola no encontrada, usando fuente por default")
    fuente_titulo = pygame.font_Font(None, 40)
    fuente_texto = pygame.font.Font(None, 20)
    fuente_pequena = pygame.font.Font(None, 16)


# Estado del juego
ESTADO_MENU = "MENU"
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
        print(f"Error al sacar la imagen '{ruta_completa}':{e}")
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
boton_start = cargar_imagen(ruta_botones, "IniciarJuego.png", TAMANO_BOTON)
boton_start_hover = cargar_imagen(ruta_botones, "IniciarJuegoSelect.png", TAMANO_BOTON)
boton_instr = cargar_imagen(ruta_botones, "Instrucciones.png", TAMANO_BOTON)
boton_instr_hover = cargar_imagen(ruta_botones, "InstruccionesSelect.png", TAMANO_BOTON)
boton_cred = cargar_imagen(ruta_botones, "Creditos.png", TAMANO_BOTON)
boton_cred_hover = cargar_imagen(ruta_botones, "CreditosSelect.png", TAMANO_BOTON)
boton_salir = cargar_imagen(ruta_botones, "Salir.png", TAMANO_BOTON)
boton_salir_hover = cargar_imagen(ruta_botones,"SalirSelect.png", TAMANO_BOTON)

# =====================
# Botones
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

boton_start = crear_botones_centrados_menu(boton_start, boton_start_hover, 490, "Iniciar")
boton_instr = crear_botones_centrados_menu(boton_instr, boton_instr_hover, 550, "instrucciones")
boton_cred = crear_botones_centrados_menu(boton_cred, boton_cred_hover, 610, "Créditos")
boton_salir = crear_botones_centrados_menu(boton_salir, boton_salir_hover, 670, "Salir")

botones_menu = [boton_start, boton_instr, boton_cred, boton_salir]

# ====================
# dibujar pantalla
# ====================
def dibujar_pantalla_menu():
    screen.blit(fondo_menu, (0, 0))

    mx, my = pygame.mouse.get_pos()
    for boton in botones_menu:
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
        
        # eventos
        if estado_actual == ESTADO_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for boton in botones_menu:
                    if boton.clic((mx, my)):
                        if boton.texto_accion == "Iniciar":
                            estado_actual = ESTADO_PLAYGROUND
                        elif boton.texto_accion == "instrucciones":
                            print("Mostrar instrucciones")
                        elif boton.texto_accion == "Créditos":
                            print("Mostrar créditos")
                        elif boton.texto_accion == "Salir":
                            running = False
        elif estado_actual == ESTADO_PLAYGROUND:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado_actual = ESTADO_MENU
    
    # dibujar segun el estado
    if estado_actual == ESTADO_MENU:
        dibujar_pantalla_menu()
    elif estado_actual == ESTADO_PLAYGROUND:
        #dibujar_pantalla_playground()
        print("Pantalla de juego")
    
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()