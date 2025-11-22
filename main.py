import pygame
import sys
import os

pygame.init()

# =====================
# Configuración básica
# =====================
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Adventure Game")
clock = pygame.time.Clock()
FPS = 60

#================
# Colores
#================
NEGRO = (0, 0, 0)
BLANCO = (255, 225, 255)
GRIS = (40, 40, 40)
ROJO = (255, 0, 0)
GRIS_CLARO = (200, 200, 200)
VERDE = (0, 200, 0)
ROJO_FALLO = (255, 100, 100)
NARANJA = (230, 150, 60)
GRIS_OSCURO = (30, 30, 30)

#=================
# Fuentes
# ================
try:
    fuente_titulo = pygame.font.SysFont("consolas", 40, bold=True)
    fuente_texto = pygame.font.SysFont("consolas", 22)
    fuente_peque = pygame.font.SysFont("consolas", 16)
except pygame.error:
    print("Advertencia: Fuente consola no encontrada, usando fuente por default")
    fuente_titulo = pygame.font.Font(None, 40)
    fuente_texto = pygame.font.Font(None, 22)
    fuente_peque = pygame.font.Font(None, 16)

# =====================
# Estados del juego
# =====================
ESTADO_MENU = "MENU"
ESTADO_SELECCION = "SELECCION_PERSONAJE"
ESTADO_PLAYGROUND = "PLAYGROUND"
estado_actual = ESTADO_MENU

# =====================
# Cargar imagen genérica con fallback
# =====================
def cargar_imagen(ruta_base, nombre_archivo, tamanio=None, fallback_color=ROJO_FALLO):
    ruta_completa = os.path.join(ruta_base, nombre_archivo)
    try:
        imagen = pygame.image.load(ruta_completa).convert_alpha()
        if tamanio:
            imagen = pygame.transform.scale(imagen, tamanio)
        return imagen
    except Exception as e:
        print(f"Error al cargar la imagen '{ruta_completa}': {e}")
        if tamanio:
            surf = pygame.Surface(tamanio)
        else:
            surf = pygame.Surface((200, 50))
        surf.fill(fallback_color)
        return surf

# =====================
# Función de escalado proporcional
# =====================
def escalar(img, factor):
    w, h = img.get_size()
    return pygame.transform.scale(img, (int(w * factor), int(h * factor)))

# =============
# Rutas base
# =============
ruta_assets = "assets"
ruta_fondos = os.path.join(ruta_assets, "fondos")

# -- Fondo ---
fondo_menu = cargar_imagen(ruta_fondos, "pantalla_inicial.png", (WIDTH, HEIGHT), NEGRO)

# =====================
# Personajes (selección)
# =====================
ruta_personajes = os.path.join(ruta_assets, "personajes")
SCALE_CHAR = 3.0

char1_img = escalar(pygame.image.load(os.path.join(ruta_personajes, "Dude_Monster.png")).convert_alpha(), SCALE_CHAR)
char2_img = escalar(pygame.image.load(os.path.join(ruta_personajes, "Owlet_Monster.png")).convert_alpha(), SCALE_CHAR)
char3_img = escalar(pygame.image.load(os.path.join(ruta_personajes, "Pink_Monster.png")).convert_alpha(), SCALE_CHAR)

# =====================
# Botones del MENÚ (rectangulares)
# =====================
class BotonMenuRect:
    def __init__(self, x, y, w, h, texto_accion):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto_accion = texto_accion

    def dibujar(self, surface, mouse_pos):
        hover = self.rect.collidepoint(mouse_pos)

        if hover:
            color_fondo = GRIS_OSCURO
            color_borde = NARANJA
        else:
            color_fondo = (50, 50, 50)
            color_borde = (120, 120, 120)

        pygame.draw.rect(surface, color_fondo, self.rect, border_radius=10)
        pygame.draw.rect(surface, color_borde, self.rect, 3, border_radius=10)

        texto = fuente_texto.render(self.texto_accion, True, BLANCO)
        texto_rect = texto.get_rect(center=self.rect.center)
        surface.blit(texto, texto_rect)

    def clic(self, pos):
        return self.rect.collidepoint(pos)

# Crear botones del menú principal
ANCHO_BTN_MENU = 260
ALTO_BTN_MENU = 55
X_BTN_MENU = WIDTH // 2 - ANCHO_BTN_MENU // 2

boton_start = BotonMenuRect(X_BTN_MENU, 480, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Iniciar")
boton_instr = BotonMenuRect(X_BTN_MENU, 545, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Instrucciones")
boton_cred = BotonMenuRect(X_BTN_MENU, 610, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Créditos")
boton_salir = BotonMenuRect(X_BTN_MENU, 675, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Salir")

botones_menu = [boton_start, boton_instr, boton_cred, boton_salir]

# =====================
# Selección de personaje
# =====================
class OpcionPersonaje:
    def __init__(self, image, nombre, x, y):
        self.image = image
        self.nombre = nombre
        self.rect = self.image.get_rect(center=(x, y))
        self.hit_rect = self.rect.copy()
        self.hit_rect.inflate_ip(-20, -20)

    def dibujar(self, surface, seleccionado=False, hover=False):
        if seleccionado:
            color_borde = NARANJA
        elif hover:
            color_borde = GRIS_CLARO
        else:
            color_borde = (80, 80, 80)

        pygame.draw.rect(surface, color_borde, self.rect.inflate(10, 10), 3, border_radius=8)
        surface.blit(self.image, self.rect)

        texto = fuente_peque.render(self.nombre, True, BLANCO)
        texto_rect = texto.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
        surface.blit(texto, texto_rect)

    def clic(self, pos):
        return self.hit_rect.collidepoint(pos)

char_y = 420
offset_char = 220

personaje_opciones = [
    OpcionPersonaje(char1_img, "Explorador", WIDTH//2 - offset_char, char_y),
    OpcionPersonaje(char2_img, "Hechicera",  WIDTH//2,              char_y),
    OpcionPersonaje(char3_img, "Guardían",   WIDTH//2 + offset_char, char_y),
]

personaje_seleccionado = None

btn_volver_rect = pygame.Rect(100, HEIGHT - 100, 180, 50)
btn_continuar_rect = pygame.Rect(WIDTH - 280, HEIGHT - 100, 180, 50)

# ==========================
# Estado del PLAYGROUND
# ==========================
code_text = ""          # código escrito
log_message = ""        # mensajes en zona de log
log_color = BLANCO

personaje_actual_img = char1_img
player_x = 0
player_y = 0
player_start_x = 0
player_target_x = 0
player_speed = 4
moving = False

PIXELS_PER_STEP = 12

# ==========================
# Layout del PLAYGROUND
# ==========================
LEFT_WIDTH = int(WIDTH * 0.35)
RIGHT_WIDTH = WIDTH - LEFT_WIDTH
INSTR_HEIGHT = int(HEIGHT * 0.4)

RECT_LEFT = pygame.Rect(0, 0, LEFT_WIDTH, HEIGHT)
RECT_INSTR = pygame.Rect(10, 10, LEFT_WIDTH - 20, INSTR_HEIGHT - 20)
CODE_TOP = INSTR_HEIGHT
RECT_CODE = pygame.Rect(10, CODE_TOP + 10, LEFT_WIDTH - 20, HEIGHT - CODE_TOP - 70)

BTN_HEIGHT = 40
RECT_BTN_AREA = pygame.Rect(10, HEIGHT - BTN_HEIGHT - 10, LEFT_WIDTH - 20, BTN_HEIGHT)
ANCHO_BTN = (RECT_BTN_AREA.width - 30) // 2
BTN_REINICIAR = pygame.Rect(RECT_BTN_AREA.x + 5,
                            RECT_BTN_AREA.y + 5,
                            ANCHO_BTN,
                            BTN_HEIGHT - 10)
BTN_EJECUTAR = pygame.Rect(RECT_BTN_AREA.x + 20 + ANCHO_BTN,
                           RECT_BTN_AREA.y + 5,
                           ANCHO_BTN,
                           BTN_HEIGHT - 10)

RECT_RIGHT = pygame.Rect(LEFT_WIDTH, 0, RIGHT_WIDTH, HEIGHT)
VISUAL_HEIGHT = int(HEIGHT * 0.65)
RECT_VISUAL = pygame.Rect(LEFT_WIDTH + 10, 10, RIGHT_WIDTH - 20, VISUAL_HEIGHT - 20)
RECT_LOG = pygame.Rect(LEFT_WIDTH + 10,
                       VISUAL_HEIGHT + 10,
                       RIGHT_WIDTH - 20,
                       HEIGHT - VISUAL_HEIGHT - 20)

# ==========================
# Lógica del nivel 1
# ==========================
def iniciar_nivel_1():
    """Reinicia el estado del primer reto: mover 10 pasos."""
    global code_text, log_message, log_color
    global personaje_actual_img, player_x, player_y, player_start_x, player_target_x, moving

    code_text = ""
    log_message = "Escribe el código y pulsa Ejecutar."
    log_color = BLANCO

    global personaje_seleccionado
    if personaje_seleccionado is not None:
        personaje_actual_img = personaje_opciones[personaje_seleccionado].image
    else:
        personaje_actual_img = char1_img

    player_start_x = RECT_VISUAL.x + 40
    player_x = player_start_x
    player_y = RECT_VISUAL.bottom - personaje_actual_img.get_height() - 20

    moving = False
    player_target_x = player_start_x

def analizar_codigo(texto):
    """
    Analiza el código del jugador.
    Debe ser algo tipo:
        pasos = 10
        mover(pasos)
    o:
        pasos = 10
        mover(10)
    """
    lineas = [l.strip() for l in texto.splitlines() if l.strip() != ""]
    if len(lineas) < 2:
        return False, "Debes escribir dos líneas: la variable y la llamada a mover()."

    # 1) línea de la variable
    linea_var = lineas[0]
    if "=" not in linea_var:
        return False, "Primero define la variable: pasos = 10"

    nombre, valor = linea_var.split("=", 1)
    nombre = nombre.strip()
    valor = valor.strip()

    if nombre != "pasos":
        return False, "La variable debe llamarse exactamente 'pasos'."

    if not valor.isdigit():
        return False, "El valor de 'pasos' debe ser un número entero, ej: pasos = 10."

    pasos_val = int(valor)

    # 2) línea de la función mover
    linea_mover = lineas[1]
    if not linea_mover.startswith("mover(") or not linea_mover.endswith(")"):
        return False, "La segunda línea debe ser: mover(pasos) o mover(10)."

    argumento = linea_mover[len("mover("):-1].strip()

    if argumento == "pasos":
        pasos_finales = pasos_val
    elif argumento.isdigit():
        pasos_finales = int(argumento)
    else:
        return False, "El argumento de mover() debe ser 'pasos' o un número."

    if pasos_finales <= 0:
        return False, "El número de pasos debe ser mayor que 0."

    return True, pasos_finales

def actualizar_movimiento():
    """Actualiza la animación de movimiento del personaje."""
    global player_x, moving, log_message, log_color

    if not moving:
        return

    if player_x < player_target_x:
        player_x += player_speed
        if player_x >= player_target_x:
            player_x = player_target_x
            moving = False
            log_message = "¡Genial! Moviste al personaje correctamente."
            log_color = VERDE
    else:
        moving = False

# ==========================
# Dibujo de pantallas
# ==========================
def dibujar_texto_multilinea(texto, rect, font, color):
    x = rect.x + 8
    y = rect.y + 8
    for linea in (texto.splitlines() or [""]):
        surface = font.render(linea, True, color)
        screen.blit(surface, (x, y))
        y += font.get_linesize()

def dibujar_pantalla_menu():
    screen.blit(fondo_menu, (0, 0))
    mx, my = pygame.mouse.get_pos()
    for boton in botones_menu:
        boton.dibujar(screen, (mx, my))

def dibujar_boton_rect(rect, texto, activo=True):
    color_fondo = GRIS_OSCURO if activo else (60, 60, 60)
    color_borde = NARANJA if activo else (120, 120, 120)
    pygame.draw.rect(screen, color_fondo, rect, border_radius=10)
    pygame.draw.rect(screen, color_borde, rect, 3, border_radius=10)
    txt = fuente_peque.render(texto, True, BLANCO if activo else (180, 180, 180))
    screen.blit(txt, txt.get_rect(center=rect.center))

def dibujar_pantalla_seleccion():
    screen.fill((15, 15, 25))

    titulo = fuente_titulo.render("Elige tu aventurer@", True, NARANJA)
    screen.blit(titulo, titulo.get_rect(center=(WIDTH//2, 60)))

    proposito_lines = [
        "Propósito del juego:",
        "Aprender los conceptos básicos de programación en Python",
        "usando variables, condicionales, ciclos y funciones",
        "para ayudar a tu personaje a superar desafíos 8-bit."
    ]
    y_text = 120
    for linea in proposito_lines:
        t = fuente_peque.render(linea, True, BLANCO)
        screen.blit(t, t.get_rect(center=(WIDTH//2, y_text)))
        y_text += 26

    mx, my = pygame.mouse.get_pos()
    for idx, opcion in enumerate(personaje_opciones):
        hover = opcion.hit_rect.collidepoint((mx, my))
        seleccionado = (personaje_seleccionado == idx)
        opcion.dibujar(screen, seleccionado=seleccionado, hover=hover)

    dibujar_boton_rect(btn_volver_rect, "Volver al menú", activo=True)
    dibujar_boton_rect(btn_continuar_rect, "Continuar", activo=(personaje_seleccionado is not None))

def dibujar_pantalla_playground():
    screen.fill(GRIS)

    # Lado izquierdo
    pygame.draw.rect(screen, GRIS, RECT_LEFT)
    pygame.draw.rect(screen, ROJO, RECT_LEFT, 2)

    # Instrucciones (1)
    pygame.draw.rect(screen, NEGRO, RECT_INSTR)
    pygame.draw.rect(screen, ROJO, RECT_INSTR, 2)

    instrucciones = (
        "Instrucciones del nivel 1:\n\n"
        "Una VARIABLE es como una caja donde guardas un valor.\n"
        "Por ejemplo:\n"
        "    pasos = 10\n\n"
        "Luego puedes usar ese nombre en una función:\n"
        "    mover(pasos)\n\n"
        "Reto: mueve el personaje 10 pasos usando\n"
        "una variable llamada 'pasos' y la función mover()."
    )
    dibujar_texto_multilinea(instrucciones, RECT_INSTR, fuente_peque, BLANCO)

    # Zona de código (2)
    pygame.draw.rect(screen, NEGRO, RECT_CODE)
    pygame.draw.rect(screen, ROJO, RECT_CODE, 2)
    dibujar_texto_multilinea(code_text or "# Escribe tu código aquí", RECT_CODE, fuente_peque, BLANCO)

    # Botones Reiniciar / Ejecutar
    pygame.draw.rect(screen, GRIS_CLARO, RECT_BTN_AREA)
    pygame.draw.rect(screen, ROJO, RECT_BTN_AREA, 2)

    pygame.draw.rect(screen, NEGRO, BTN_REINICIAR)
    pygame.draw.rect(screen, ROJO, BTN_REINICIAR, 2)
    txt_r = fuente_peque.render("Reiniciar", True, BLANCO)
    screen.blit(txt_r, txt_r.get_rect(center=BTN_REINICIAR.center))

    pygame.draw.rect(screen, NEGRO, BTN_EJECUTAR)
    pygame.draw.rect(screen, ROJO, BTN_EJECUTAR, 2)
    txt_e = fuente_peque.render("Ejecutar", True, BLANCO)
    screen.blit(txt_e, txt_e.get_rect(center=BTN_EJECUTAR.center))

    # Lado derecho
    pygame.draw.rect(screen, GRIS, RECT_RIGHT)
    pygame.draw.rect(screen, ROJO, RECT_RIGHT, 2)

    pygame.draw.rect(screen, NEGRO, RECT_VISUAL)
    pygame.draw.rect(screen, ROJO, RECT_VISUAL, 2)

    texto_visual = fuente_peque.render(
        "[ESC] Volver al menú | Visual del juego: mapa + personaje.",
        True, BLANCO
    )
    screen.blit(texto_visual, (RECT_VISUAL.x + 10, RECT_VISUAL.y + 10))

    # Personaje
    screen.blit(personaje_actual_img, (player_x, player_y))

    # Log
    pygame.draw.rect(screen, NEGRO, RECT_LOG)
    pygame.draw.rect(screen, ROJO, RECT_LOG, 2)
    dibujar_texto_multilinea(log_message, RECT_LOG, fuente_peque, log_color)

# ====================
# Loop principal
# ====================
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ----- MENÚ -----
        if estado_actual == ESTADO_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for boton in botones_menu:
                    if boton.clic((mx, my)):
                        if boton.texto_accion == "Iniciar":
                            estado_actual = ESTADO_SELECCION
                        elif boton.texto_accion == "Instrucciones":
                            print("Mostrar instrucciones")
                        elif boton.texto_accion == "Créditos":
                            print("Mostrar créditos")
                        elif boton.texto_accion == "Salir":
                            running = False

        # ----- SELECCIÓN DE PERSONAJE -----
        elif estado_actual == ESTADO_SELECCION:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                for idx, opcion in enumerate(personaje_opciones):
                    if opcion.clic((mx, my)):
                        personaje_seleccionado = idx

                if btn_volver_rect.collidepoint((mx, my)):
                    estado_actual = ESTADO_MENU
                    personaje_seleccionado = None

                if btn_continuar_rect.collidepoint((mx, my)) and personaje_seleccionado is not None:
                    print(f"Personaje seleccionado: {personaje_opciones[personaje_seleccionado].nombre}")
                    iniciar_nivel_1()
                    estado_actual = ESTADO_PLAYGROUND

        # ----- PLAYGROUND -----
        elif estado_actual == ESTADO_PLAYGROUND:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado_actual = ESTADO_MENU
                    personaje_seleccionado = None
                elif event.key == pygame.K_BACKSPACE:
                    code_text = code_text[:-1]
                elif event.key == pygame.K_RETURN:
                    code_text += "\n"
                else:
                    if event.unicode and event.unicode.isprintable():
                        code_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if BTN_REINICIAR.collidepoint((mx, my)):
                    iniciar_nivel_1()

                elif BTN_EJECUTAR.collidepoint((mx, my)):
                    if not moving:
                        ok, res = analizar_codigo(code_text)
                        if not ok:
                            log_message = "Error: " + res
                            log_color = ROJO_FALLO
                        else:
                            pasos = res
                            max_pixels = RECT_VISUAL.right - 40 - personaje_actual_img.get_width() - player_start_x
                            distancia = min(pasos * PIXELS_PER_STEP, max_pixels)
                            player_x = player_start_x
                            player_target_x = player_start_x + distancia
                            moving = True
                            log_message = f"Ejecutando mover({pasos})..."
                            log_color = BLANCO

    # DIBUJO SEGÚN ESTADO
    if estado_actual == ESTADO_MENU:
        dibujar_pantalla_menu()
    elif estado_actual == ESTADO_SELECCION:
        dibujar_pantalla_seleccion()
    elif estado_actual == ESTADO_PLAYGROUND:
        actualizar_movimiento()
        dibujar_pantalla_playground()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
