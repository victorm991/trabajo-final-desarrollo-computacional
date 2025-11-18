import pygame
import sys

pygame.init()

# =====================
# Configuración básica
# =====================
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Adventure Game")
clock = pygame.time.Clock()
FPS = 60

#Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
GRIS = (200, 200, 200)
GRIS_CLARO = (220, 220, 220)
VERDE = (0, 255, 0)

# FUENTES
fuente_titulo = pygame.font.SysFont("consolas", 40, bold=True)
fuente_texto = pygame.font.SysFont("consolas", 20)
fuente_pequeña = pygame.font.SysFont("consolas", 16)

# Estado del juego
ESTADO_MENU = "MENU"
ESTADO_PLAYGROUND = "PLAYGROUND"
estado_actual = ESTADO_MENU

# =====================
# Cargar imagen de fondo
# =====================
try:
    fondo_menu = fondo_menu = pygame.image.load("assets/fondos/pantalla_inicial.png")
    fondo_menu = pygame.transform.scale(fondo_menu, (WIDTH, HEIGHT))
except Exception as e:
    print("Error al cargar la imagen de fondo:", e)
    fondo_menu = pygame.Surface((WIDTH, HEIGHT))
    fondo_menu.fill(NEGRO)

# =======
# imagenes botones
# =============
btn_start_img = pygame.image.load("assets/botones/IniciarJuego.png")
btn_start_hover_img = pygame.image.load("assets/botones/IniciarJuegoSelect.png")
btn_instr_img = pygame.image.load("assets/botones/Instrucciones.png")
btn_instr_hover_img = pygame.image.load("assets/botones/InstruccionesSelect.png")
btn_cred_img = pygame.image.load("assets/botones/Creditos.png")
btn_cred_hover_img = pygame.image.load("assets/botones/CreditosSelect.png")
btn_salir_img = pygame.image.load("assets/botones/Salir.png")
btn_salir_hover_img = pygame.image.load("assets/botones/SalirSelect.png")

btn_start_img = pygame.transform.scale(btn_start_img, (200,180))
btn_start_hover_img = pygame.transform.scale(btn_start_hover_img, (200, 180))
btn_instr_img = pygame.transform.scale(btn_instr_img, (200, 180))
btn_instr_hover_img = pygame.transform.scale(btn_instr_hover_img, (200, 180))
btn_cred_img = pygame.transform.scale(btn_cred_img, (200, 180))
btn_cred_hover_img = pygame.transform.scale(btn_cred_hover_img, (200, 180))
btn_salir_img = pygame.transform.scale(btn_salir_img, (200, 180))
btn_salir_hover_img = pygame.transform.scale(btn_salir_hover_img, (200, 180))


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

botones_menu = [
    crear_boton(btn_start_img, btn_start_hover_img, WIDTH//2 - btn_start_img.get_width() // 2, 300),
    crear_boton(btn_instr_img, btn_instr_hover_img, WIDTH//2 - btn_instr_img.get_width() // 2, 355),
    crear_boton(btn_cred_img, btn_cred_hover_img, WIDTH//2 - btn_cred_img.get_width() // 2, 410),
    crear_boton(btn_salir_img, btn_salir_hover_img, WIDTH//2 - btn_salir_img.get_width() // 2, 465)
]

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
                        texto = boton.texto
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