import pygame
import sys
import os

from config import (
    WIDTH,
    HEIGHT,
    FPS,
    CAPTION,
    NEGRO,
    BLANCO,
    GRIS,
    GRIS_CLARO,
    GRIS_OSCURO,
    ROJO,
    VERDE,
    ROJO_FALLO,
    NARANJA,
    PANEL_BG,
    PANEL_BORDER,
    CODE_BG,
    RUTA_FONDOS,
    RUTA_PERSONAJES,
    RUTA_MUSICA,
    RUTA_ICONO,
)
from entities.sprites import cargar_spritesheet
from entities.player import Player

pygame.init()


# =====================
# Configuración básica
# =====================
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(CAPTION)

# Se encarga de cargar el icono en el titulo de la vetana
try:
    icono_img = pygame.image.load(
        os.path.join("assets", "icono", "python_adventure.png")
    ).convert_alpha()
    pygame.display.set_icon(icono_img)
except Exception as e:
    print(f"No se pudo cargar el icono de la venta: {e}")
clock = pygame.time.Clock()

# =================
# Fuentes
# ================
try:
    fuente_titulo = pygame.font.SysFont("consolas", 40, bold=True)
    fuente_texto = pygame.font.SysFont("consolas", 22)
    fuente_peque = pygame.font.SysFont("consolas", 16)
except pygame.error:
    print("Advertencia: Fuente consola no encontrada, usando fuente por defecto")
    fuente_titulo = pygame.font.Font(None, 40)
    fuente_texto = pygame.font.Font(None, 22)
    fuente_peque = pygame.font.Font(None, 16)

# =====================
# Estados del juego
# =====================
ESTADO_MENU = "MENU"
ESTADO_SELECCION = "SELECCION_PERSONAJE"
ESTADO_PLAYGROUND = "PLAYGROUND"
ESTADO_CREDITOS = "CREDITOS"
estado_actual = ESTADO_MENU

# Niveles
nivel_actual = 1
NUM_NIVELES = 3
nivel_completado = False

# =================
# personajes
# =================
FRAMES_CAMINAR = 6
SCALE_CHAR = 3.0

frames_dude = cargar_spritesheet(
    os.path.join(RUTA_PERSONAJES, "Dude_Monster_Walk.png"),
    FRAMES_CAMINAR,
    scale=SCALE_CHAR,
)
frames_owlet = cargar_spritesheet(
    os.path.join(RUTA_PERSONAJES, "Owlet_Monster_Walk.png"),
    FRAMES_CAMINAR,
    scale=SCALE_CHAR,
)
frames_pink = cargar_spritesheet(
    os.path.join(RUTA_PERSONAJES, "Pink_Monster_Walk.png"),
    FRAMES_CAMINAR,
    scale=SCALE_CHAR,
)

# frame quieto
img_dude_idle = frames_dude[0]
img_owlet_idle = frames_owlet[0]
img_pink_idle = frames_pink[0]

player = Player(frames_dude, speed=4)


# =====================
# Cargar imagen con fallback
# =====================
def cargar_imagen(ruta_base, nombre_archivo, tamanio=None, fallback_color=(30, 30, 30)):
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


def escalar(img, factor):
    w, h = img.get_size()
    return pygame.transform.scale(img, (int(w * factor), int(h * factor)))


# Fondo del menú
fondo_menu = cargar_imagen(RUTA_FONDOS, "pantalla_inicial.png", (WIDTH, HEIGHT), NEGRO)

# =====================
# Música de fondo
# =====================
try:
    ruta_tema = os.path.join(RUTA_MUSICA, "soundTrack.ogg")  # o .mp3
    pygame.mixer.music.load(ruta_tema)
    pygame.mixer.music.set_volume(1.0)  # volumen de 0.0 a 1.0
    pygame.mixer.music.play(-1)  # -1 = loop infinito
except Exception as e:
    print("No se pudo cargar la música:", e)


# =====================
# Personajes selección
# =====================
SCALE_CHAR = 3.0

char1_img = escalar(
    pygame.image.load(
        os.path.join(RUTA_PERSONAJES, "Dude_Monster.png")
    ).convert_alpha(),
    SCALE_CHAR,
)
char2_img = escalar(
    pygame.image.load(
        os.path.join(RUTA_PERSONAJES, "Owlet_Monster.png")
    ).convert_alpha(),
    SCALE_CHAR,
)
char3_img = escalar(
    pygame.image.load(
        os.path.join(RUTA_PERSONAJES, "Pink_Monster.png")
    ).convert_alpha(),
    SCALE_CHAR,
)


# =====================
# Botones del menú
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
        screen.blit(texto, texto.get_rect(center=self.rect.center))

    def clic(self, pos):
        return self.rect.collidepoint(pos)


ANCHO_BTN_MENU = 260
ALTO_BTN_MENU = 55
X_BTN_MENU = WIDTH // 2 - ANCHO_BTN_MENU // 2

boton_start = BotonMenuRect(X_BTN_MENU, 480, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Iniciar")
boton_cred = BotonMenuRect(X_BTN_MENU, 545, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Créditos")
boton_salir = BotonMenuRect(X_BTN_MENU, 610, ANCHO_BTN_MENU, ALTO_BTN_MENU, "Salir")

botones_menu = [boton_start, boton_cred, boton_salir]


# ========================
# Selección de personaje
# ========================
class OpcionPersonaje:
    def __init__(self, frames_walk, nombre, x, y):

        self.frames_walk = frames_walk
        self.image = self.frames_walk[0]
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

        pygame.draw.rect(
            surface, color_borde, self.rect.inflate(10, 10), 3, border_radius=8
        )
        surface.blit(self.image, self.rect)

        texto = fuente_peque.render(self.nombre, True, BLANCO)
        screen.blit(
            texto, texto.get_rect(center=(self.rect.centerx, self.rect.bottom + 20))
        )

    def clic(self, pos):
        return self.hit_rect.collidepoint(pos)


char_y = 420
offset_char = 220

personaje_opciones = [
    OpcionPersonaje(frames_dude, "Explorador", WIDTH // 2 - offset_char, char_y),
    OpcionPersonaje(frames_owlet, "Hechicera", WIDTH // 2, char_y),
    OpcionPersonaje(frames_pink, "Guardían", WIDTH // 2 + offset_char, char_y),
]

personaje_seleccionado = None

btn_volver_rect = pygame.Rect(100, HEIGHT - 100, 180, 50)
btn_continuar_rect = pygame.Rect(WIDTH - 280, HEIGHT - 100, 180, 50)

# ==========================
# Estado del PLAYGROUND
# ==========================
code_text = ""
log_message = ""
log_color = NEGRO

PIXELS_PER_STEP = 12

# Texto que "dice" el personaje (nivel 1)
texto_dicho = ""

# ==========================
# Layout del PLAYGROUND
# ==========================
LEFT_WIDTH = int(WIDTH * 0.35)
RIGHT_WIDTH = WIDTH - LEFT_WIDTH
INSTR_HEIGHT = int(HEIGHT * 0.4)

RECT_LEFT = pygame.Rect(0, 0, LEFT_WIDTH, HEIGHT)
RECT_INSTR = pygame.Rect(10, 50, LEFT_WIDTH - 20, INSTR_HEIGHT - 20)
CODE_TOP = INSTR_HEIGHT
RECT_CODE = pygame.Rect(10, CODE_TOP + 10, LEFT_WIDTH - 20, HEIGHT - CODE_TOP - 70)

BTN_HEIGHT = 40
RECT_BTN_AREA = pygame.Rect(10, HEIGHT - BTN_HEIGHT - 10, LEFT_WIDTH - 20, BTN_HEIGHT)
ANCHO_BTN = (RECT_BTN_AREA.width - 30) // 2
BTN_REINICIAR = pygame.Rect(
    RECT_BTN_AREA.x + 5, RECT_BTN_AREA.y + 5, ANCHO_BTN, BTN_HEIGHT - 10
)
BTN_EJECUTAR = pygame.Rect(
    RECT_BTN_AREA.x + 20 + ANCHO_BTN, RECT_BTN_AREA.y + 5, ANCHO_BTN, BTN_HEIGHT - 10
)

RECT_RIGHT = pygame.Rect(LEFT_WIDTH, 0, RIGHT_WIDTH, HEIGHT)
VISUAL_HEIGHT = int(HEIGHT * 0.65)
RECT_VISUAL = pygame.Rect(LEFT_WIDTH + 10, 10, RIGHT_WIDTH - 20, VISUAL_HEIGHT - 20)
RECT_LOG = pygame.Rect(
    LEFT_WIDTH + 10, VISUAL_HEIGHT + 10, RIGHT_WIDTH - 20, HEIGHT - VISUAL_HEIGHT - 20
)

# Botón "Salir" del playground
BTN_SALIR_PLAYGROUND = pygame.Rect(10, 10, 90, 30)

# ===========
# Mapa visual
# ===========
# Coloca tu imagen aquí: assets/fondos/mapa_nivel1.png
mapa_nivel1 = cargar_imagen(
    RUTA_FONDOS, "fondo_nivel.png", (RECT_VISUAL.width, RECT_VISUAL.height), NEGRO
)


# ==========================
# Lógica niveles
# ==========================
def base_setup_personaje():
    global player, personaje_seleccionado

    if personaje_seleccionado == 0:
        frames = frames_dude
    elif personaje_seleccionado == 1:
        frames = frames_owlet
    elif personaje_seleccionado == 2:
        frames = frames_pink
    else:
        frames = frames_dude

    player.set_frames(frames)
    player.lugar_en_espacio(RECT_VISUAL, align="left")


def iniciar_nivel(n):
    global nivel_actual, code_text, log_message, log_color
    global texto_dicho, nivel_completado

    nivel_actual = n
    nivel_completado = False
    code_text = ""
    texto_dicho = ""
    log_color = NEGRO

    base_setup_personaje()

    if n == 1:
        log_message = "Nivel 1: usa una variable 'pasos' y mover()."
    elif n == 2:
        player.lugar_en_espacio(RECT_VISUAL, align="center")
        log_message = "Nivel 2: usa print() para que el personaje hable."
    elif n == 3:
        player.lugar_en_espacio(RECT_VISUAL, align="center")
        log_message = "Nivel 3: usa un ciclo for y saltar()."


def analizar_nivel1(texto):
    """
    Nivel 1: variables y mover(pasos).
    """
    lineas = [l.strip() for l in texto.splitlines() if l.strip() != ""]
    if len(lineas) < 2:
        return False, "Debes escribir dos líneas: la variable y la llamada a mover()."

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

    linea_mover = lineas[1]
    if not linea_mover.startswith("mover(") or not linea_mover.endswith(")"):
        return False, "La segunda línea debe ser: mover(pasos) o mover(10)."

    argumento = linea_mover[len("mover(") : -1].strip()

    if argumento == "pasos":
        pasos_finales = pasos_val
    elif argumento.isdigit():
        pasos_finales = int(argumento)
    else:
        return False, "El argumento de mover() debe ser 'pasos' o un número."

    if pasos_finales <= 0:
        return False, "El número de pasos debe ser mayor que 0."

    return True, pasos_finales


def analizar_nivel2(texto):
    """
    Nivel 2: print("mensaje").
    """
    lineas = [l.strip() for l in texto.splitlines() if l.strip() != ""]
    if not lineas:
        return False, "Escribe al menos una línea con print()."

    linea = lineas[0]
    if not (linea.startswith("print(") and linea.endswith(")")):
        return False, 'Debes usar: print("tu mensaje")'

    contenido = linea[len("print(") : -1].strip()

    if len(contenido) < 2 or contenido[0] not in "\"'" or contenido[-1] != contenido[0]:
        return False, 'El texto debe ir entre comillas: print("Hola")'

    mensaje = contenido[1:-1]  # quitar comillas
    if len(mensaje) > 200:
        return False, "El mensaje puede tener máximo 200 caracteres."

    return True, mensaje


def analizar_nivel3(texto):
    """
    Nivel 3: ciclo for y saltar().
    Ejemplo esperado (o similar):
        for i in range(3):
            saltar()
    """
    lineas = [l.rstrip() for l in texto.splitlines() if l.strip() != ""]
    if not lineas:
        return False, "Debes usar un ciclo for y la función saltar()."

    tiene_for = False
    tiene_saltar = False
    n_saltos = 0

    for linea in lineas:
        linea_sin_esp = linea.replace(" ", "")
        if linea.strip().startswith("for ") and "range(" in linea and ":" in linea:
            tiene_for = True
            try:
                dentro = linea.split("range(", 1)[1].split(")", 1)[0].strip()
                if not dentro.isdigit():
                    return False, "Usa un número en range(), por ejemplo: range(3)."
                n_saltos = int(dentro)
            except Exception:
                return False, "No pude leer el número de range()."
        if "saltar()" in linea_sin_esp:
            tiene_saltar = True

    if not tiene_for:
        return False, "Te falta el ciclo for con range()."
    if not tiene_saltar:
        return False, "Dentro del ciclo debes llamar a saltar()."
    if n_saltos <= 0:
        return False, "El número de saltos debe ser mayor que 0."

    return True, n_saltos


def actualizar_animacion():
    """
    Mueve al personaje según el modo de animación (caminar o saltar).
    También marca el nivel como completado cuando termina.
    """

    global nivel_completado, log_message, log_color, nivel_actual

    modo_finalizado = player.actualizar()

    if modo_finalizado == "walk" and nivel_actual == 1:
        nivel_completado = True
        log_message = "¡Genial! Moviste al personaje correctamente."
        log_color = VERDE

    if modo_finalizado == "jump" and nivel_actual == 3:
        nivel_completado = True
        log_message = "¡Perfecto! Usaste un ciclo para saltar."
        log_color = VERDE


# ==========================
# Dibujo de pantallas
# ==========================
def dibujar_texto_multilinea(texto, rect, font, color):
    x = rect.x + 8
    y = rect.y + 8
    max_width = rect.width - 16

    for parrafo in texto.splitlines() or [""]:
        palabras = parrafo.split(" ")
        linea = ""
        for palabra in palabras:
            prueba = linea + palabra + " "
            prueba_surf = font.render(prueba, True, color)
            if prueba_surf.get_width() > max_width and linea != "":
                surf = font.render(linea, True, color)
                screen.blit(surf, (x, y))
                y += font.get_linesize()
                linea = palabra + " "
            else:
                linea = prueba
        if linea:
            surf = font.render(linea, True, color)
            screen.blit(surf, (x, y))
            y += font.get_linesize()


def medir_texto_multilinea(texto, max_width, font):
    """
    Calcula el ancho y alto que ocuparía el texto envuelto dentro de max_width.
    Se usa para ajustar el tamaño de la burbuja.
    """
    max_width_interno = max_width - 16
    total_height = 0
    used_width = 0

    for parrafo in texto.splitlines() or [""]:
        palabras = parrafo.split(" ")
        linea = ""
        for palabra in palabras:
            prueba = linea + palabra + " "
            prueba_surf = font.render(prueba, True, (0, 0, 0))
            if prueba_surf.get_width() > max_width_interno and linea != "":
                surf = font.render(linea, True, (0, 0, 0))
                used_width = max(used_width, surf.get_width())
                total_height += font.get_linesize()
                linea = palabra + " "
            else:
                linea = prueba
        if linea:
            surf = font.render(linea, True, (0, 0, 0))
            used_width = max(used_width, surf.get_width())
            total_height += font.get_linesize()

    if used_width == 0:
        used_width = 50
    if total_height == 0:
        total_height = font.get_linesize()

    return used_width, total_height


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
    screen.blit(titulo, titulo.get_rect(center=(WIDTH // 2, 60)))

    proposito_lines = [
        "Python Adventure",
        "",
        "Aprenderás programación en Python paso a paso,",
        "moviendo y ayudando a tu personaje en un mundo 8-bit.",
        "Usaremos variables, print(), ciclos y más.",
    ]
    y_text = 120
    for linea in proposito_lines:
        t = fuente_peque.render(linea, True, BLANCO)
        screen.blit(t, t.get_rect(center=(WIDTH // 2, y_text)))
        y_text += 24

    mx, my = pygame.mouse.get_pos()
    for idx, opcion in enumerate(personaje_opciones):
        hover = opcion.hit_rect.collidepoint((mx, my))
        seleccionado = personaje_seleccionado == idx
        opcion.dibujar(screen, seleccionado=seleccionado, hover=hover)

    dibujar_boton_rect(btn_volver_rect, "Volver al menú", activo=True)
    dibujar_boton_rect(
        btn_continuar_rect, "Continuar", activo=(personaje_seleccionado is not None)
    )


def dibujar_pantalla_playground():
    screen.fill(GRIS)

    # Lado izquierdo
    pygame.draw.rect(screen, PANEL_BG, RECT_LEFT)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_LEFT, 1)

    # Botón Salir
    pygame.draw.rect(screen, GRIS_OSCURO, BTN_SALIR_PLAYGROUND, border_radius=5)
    pygame.draw.rect(screen, PANEL_BORDER, BTN_SALIR_PLAYGROUND, 1, border_radius=5)
    txt_salir = fuente_peque.render("Salir", True, BLANCO)
    screen.blit(txt_salir, txt_salir.get_rect(center=BTN_SALIR_PLAYGROUND.center))

    # Instrucciones
    pygame.draw.rect(screen, CODE_BG, RECT_INSTR)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_INSTR, 1)

    if nivel_actual == 1:
        instrucciones = (
            "Nivel 1: Variables y mover()\n\n"
            "Una VARIABLE es como una caja donde guardas un valor.\n"
            "Ejemplo:\n"
            "    pasos = 10\n\n"
            "Luego puedes usar ese nombre en una función:\n"
            "    mover(pasos)\n\n"
            "Reto: mueve el personaje 10 pasos usando\n"
            "una variable llamada 'pasos' y la función mover()."
        )
    elif nivel_actual == 2:
        instrucciones = (
            "Nivel 2: print()\n\n"
            "La función print() muestra un texto en pantalla.\n"
            "Ejemplo:\n"
            '    print("Hola mundo")\n\n'
            "Reto: escribe un print con el mensaje que quieras\n"
            "(máx 200 caracteres). El personaje lo dirá."
        )
    else:  # nivel 3
        instrucciones = (
            "Nivel 3: ciclos for y saltar()\n\n"
            "Un ciclo for repite instrucciones varias veces.\n"
            "Ejemplo:\n"
            "    for i in range(3):\n"
            "        saltar()\n\n"
            "Reto: usa un ciclo for con range() y llama a saltar()\n"
            "para que el personaje salte varias veces."
        )

    dibujar_texto_multilinea(instrucciones, RECT_INSTR, fuente_peque, NEGRO)

    # Zona de código
    pygame.draw.rect(screen, CODE_BG, RECT_CODE)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_CODE, 1)
    if code_text:
        dibujar_texto_multilinea(code_text, RECT_CODE, fuente_peque, NEGRO)
    else:
        dibujar_texto_multilinea(
            "# Escribe tu código aquí", RECT_CODE, fuente_peque, (150, 150, 150)
        )

    # Botones Reiniciar / Ejecutar / Siguiente
    pygame.draw.rect(screen, PANEL_BG, RECT_BTN_AREA)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_BTN_AREA, 1)

    pygame.draw.rect(screen, GRIS_OSCURO, BTN_REINICIAR, border_radius=5)
    pygame.draw.rect(screen, PANEL_BORDER, BTN_REINICIAR, 1, border_radius=5)
    txt_r = fuente_peque.render("Reiniciar", True, BLANCO)
    screen.blit(txt_r, txt_r.get_rect(center=BTN_REINICIAR.center))

    if nivel_completado and nivel_actual < NUM_NIVELES:
        label_exec = "Siguiente nivel"
    elif nivel_completado and nivel_actual == NUM_NIVELES:
        label_exec = "Completado"
    else:
        label_exec = "Ejecutar"

    pygame.draw.rect(screen, GRIS_OSCURO, BTN_EJECUTAR, border_radius=5)
    pygame.draw.rect(screen, PANEL_BORDER, BTN_EJECUTAR, 1, border_radius=5)
    txt_e = fuente_peque.render(label_exec, True, BLANCO)
    screen.blit(txt_e, txt_e.get_rect(center=BTN_EJECUTAR.center))

    # Lado derecho
    pygame.draw.rect(screen, PANEL_BG, RECT_RIGHT)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_RIGHT, 1)

    # Visual del juego (mapa + personaje)
    pygame.draw.rect(screen, NEGRO, RECT_VISUAL)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_VISUAL, 1)
    # Fondo de mapa
    screen.blit(mapa_nivel1, (RECT_VISUAL.x, RECT_VISUAL.y))

    texto_visual = fuente_peque.render(
        "[ESC] Volver al menú | Visual del juego.", True, BLANCO
    )
    screen.blit(texto_visual, (RECT_VISUAL.x + 10, RECT_VISUAL.y + 10))

    # Personaje
    player.dibujar(screen)

    # Si hay texto dicho (nivel 2), dibujar bocadillo
    if texto_dicho:
        max_bubble_width = RECT_VISUAL.width - 40
        min_bubble_width = 120

        text_w, text_h = medir_texto_multilinea(
            texto_dicho, max_bubble_width, fuente_peque
        )

        bubble_width = max(min_bubble_width, min(max_bubble_width, text_w + 16))
        bubble_height = text_h + 16

        bubble_rect = pygame.Rect(0, 0, bubble_width, bubble_height)
        bubble_rect.midbottom = (player.rect.centerx, player.rect.top - 10)

        if bubble_rect.left < RECT_VISUAL.x + 10:
            bubble_rect.left = RECT_VISUAL.x + 10
        if bubble_rect.right > RECT_VISUAL.right - 10:
            bubble_rect.right = RECT_VISUAL.right - 10
        if bubble_rect.top < RECT_VISUAL.y + 40:
            bubble_rect.top = RECT_VISUAL.y + 40

        pygame.draw.rect(screen, CODE_BG, bubble_rect, border_radius=10)
        pygame.draw.rect(screen, PANEL_BORDER, bubble_rect, 1, border_radius=10)
        dibujar_texto_multilinea(texto_dicho, bubble_rect, fuente_peque, NEGRO)

    # Log
    pygame.draw.rect(screen, CODE_BG, RECT_LOG)
    pygame.draw.rect(screen, PANEL_BORDER, RECT_LOG, 1)
    dibujar_texto_multilinea(log_message, RECT_LOG, fuente_peque, log_color)


def dibujar_pantalla_creditos():
    screen.fill(NEGRO)
    lineas = [
        "PYTHON ADVENTURE",
        "",
        "Creado por:",
        "  - Anderson Gil Arenas",
        "  - Victor Manuel Estrada" "" "",
        "Este proyecto nace con el propósito de enseñar Python",
        "de una forma sencilla y visual a niñas, niños y personas",
        "que están dando sus primeros pasos en programación.",
        "",
        "A través de retos pequeños y un mundo en 8 bits,",
        "buscamos que aprender variables, print(), ciclos y",
        "otras bases de la lógica sea divertido y menos intimidante.",
        "",
        "Presiona ESC para volver al menú.",
    ]
    y = 120
    for linea in lineas:
        txt = fuente_peque.render(linea, True, BLANCO)
        screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))
        y += 26


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
                        elif boton.texto_accion == "Créditos":
                            estado_actual = ESTADO_CREDITOS
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

                if (
                    btn_continuar_rect.collidepoint((mx, my))
                    and personaje_seleccionado is not None
                ):
                    iniciar_nivel(1)
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

                # Botón Salir del playground
                if BTN_SALIR_PLAYGROUND.collidepoint((mx, my)):
                    estado_actual = ESTADO_MENU
                    personaje_seleccionado = None

                elif BTN_REINICIAR.collidepoint((mx, my)):
                    iniciar_nivel(nivel_actual)

                elif BTN_EJECUTAR.collidepoint((mx, my)):
                    if nivel_completado:
                        if nivel_actual < NUM_NIVELES:
                            iniciar_nivel(nivel_actual + 1)
                        else:
                            iniciar_nivel(nivel_actual)
                    else:
                        if nivel_actual == 1:
                            ok, res = analizar_nivel1(code_text)
                            if not ok:
                                log_message = "Error: " + res
                                log_color = ROJO_FALLO
                            else:
                                pasos = res
                                player.iniciar_caminar(
                                    pasos, PIXELS_PER_STEP, RECT_VISUAL
                                )
                                nivel_completado = False
                                log_message = f"Ejecutando mover({pasos})..."
                                log_color = NEGRO

                        elif nivel_actual == 2:
                            ok, mensaje = analizar_nivel2(code_text)
                            if not ok:
                                log_message = "Error: " + mensaje
                                log_color = ROJO_FALLO
                            else:
                                texto_dicho = mensaje
                                nivel_completado = True
                                log_message = "¡Bien! Usaste print() correctamente."
                                log_color = VERDE

                        elif nivel_actual == 3:
                            ok, n_saltos = analizar_nivel3(code_text)
                            if not ok:
                                log_message = f"Error: {n_saltos}"
                                log_color = ROJO_FALLO
                            else:
                                player.iniciar_saltar(n_saltos)
                                log_message = f"Ejecutando saltar() {n_saltos} veces..."
                                log_color = NEGRO
                                nivel_completado = False

        # ----- CRÉDITOS -----
        elif estado_actual == ESTADO_CREDITOS:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                estado_actual = ESTADO_MENU

    # DIBUJO SEGÚN ESTADO
    if estado_actual == ESTADO_MENU:
        dibujar_pantalla_menu()
    elif estado_actual == ESTADO_SELECCION:
        dibujar_pantalla_seleccion()
    elif estado_actual == ESTADO_PLAYGROUND:
        actualizar_animacion()
        dibujar_pantalla_playground()
    elif estado_actual == ESTADO_CREDITOS:
        dibujar_pantalla_creditos()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
