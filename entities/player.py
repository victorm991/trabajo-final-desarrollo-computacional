import pygame


class Player:

    def __init__(self, frames_walk, speed: int = 4):

        self.frames_walk = frames_walk
        self.image = self.frames_walk[0]
        self.rect = self.image.get_rect()

        # animación
        self.current_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.25

        # Movimiento
        self.speed = speed
        self.base_y = 0
        self.start_x = 0
        self.target_x = 0

        # Estado general de animacion
        self.mode = None
        self.moving = False

        # saltos
        self.saltos_pendientes = 0
        self.fase_salto = 0
        self.fase_salto_maximo = 30
        self.jump_altura = 40

        self.area_rect = None

    # ---- Configuracion -----
    def set_frames(self, frames_walk):
        """
        Se encarga de cambiar los frames cuando se cambia de personaje.
        """
        old_midbottom = self.rect.midbottom
        self.frames_walk = frames_walk
        self.image = self.frames_walk[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def lugar_en_espacio(self, area_rect, align="left", margin_x=40, margin_bottom=20):
        """
        Se encarga de colocar el personaje dentro del área virtual
        """

        if align == "center":
            self.rect.centerx = area_rect.centerx
        else:
            self.rect.x = area_rect.x + margin_x

        self.rect.y = area_rect.bottom - self.image.get_height() - margin_bottom
        self.start_x = self.rect.x
        self.base_y = self.rect.y

    # ---------- Acciones ---------

    def iniciar_caminar(self, pasos, pixels_por_paso, area_rect):
        """
        Anima la caminada hacia la derecha
        """

        self.area_rect = area_rect
        self.mode = "walk"
        self.moving = True

        # resetear animacion
        self.current_frame = 0
        self.anim_timer = 0.0
        self.image = self.frames_walk[self.current_frame]

        pixeles_maximos = area_rect.right - 40 - self.image.get_width() - self.start_x
        distancia = min(pasos * pixels_por_paso, pixeles_maximos)

        self.rect.x = self.start_x
        self.target_x = self.start_x + distancia

    def iniciar_saltar(self, n_saltos, altura_salto=40, fase_salto_maximo=30):
        """
        Animación de saltos
        """
        self.mode = "jump"
        self.moving = True
        self.saltos_pendientes = n_saltos
        self.fase_salto = 0
        self.altura_salto = altura_salto
        self.fase_salto_maximo = fase_salto_maximo

    # -------------- actualioza
    def actualizar(self):

        if self.mode == "walk":
            if not self.moving:
                return None

        if self.rect.x < self.target_x:
            self.rect.x += self.speed
            if self.rect.x >= self.target_x:
                self.rect.x = self.target_x
                self.moving = False
                self.mode = None
                return "walk"

        else:
            self.moving = False
            self.mode = None
            return "walk"

        if len(self.frames_walk) > 1:
            self.anim_timer += self.anim_speed
            if self.anim_timer >= 1:
                self.anim_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames_walk)
                self.image = self.frames_walk[self.current_frame]
            
            return None

        elif self.mode == "jump":
            if self.saltos_pendientes <= 0:
                self.rect.y = self.base_y
                self.mode = None
                self.moving = False
                return "jump"

            t = self.fase_salto / self.fase_salto_maximo
            if t < 0.5:
                self.rect.y = self.base_y - int(self.jump_altura * (t * 2))
            else:
                self.rect.y = self.base_y - int(self.jump_altura * (t - 0.5) * 2)

            self.fase_salto += 1
            if self.fase_salto >= self.fase_salto_maximo:
                self.fase_salto = 0
                self.saltos_pendientes -= 1
                self.rect.y = self.base_y

                if self.saltos_pendientes <= 0:
                    self.mode = None
                    self.moving = False
                    return "jump"
            return None    
        return None

    def dibujar(self, surface):
        surface.blit(self.image, self.rect)
