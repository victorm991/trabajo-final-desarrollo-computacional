import pygame


class Player:

    def __init__(self, idle_image, frames_walk, frames_jump=None, speed: int = 4):
        
        self.idle_image = idle_image
        self.frames_walk = frames_walk
        self.frames_jump = frames_jump or [idle_image]
        self.image = self.frames_walk[0]
        self.rect = self.image.get_rect()

        self.image = self.idle_image
        self.rect = self.image.get_rect()

        # animación
        self.current_frame = 0
        self.anim_timer = 0.0
        self.anim_speed = 0.25  # qué tan rápido cambia de frame

        # Movimiento horizontal
        self.speed = speed
        self.base_y = 0
        self.start_x = 0
        self.target_x = 0

        # Estado general de animación
        self.mode = None      # None, "walk", "jump"
        self.moving = False

        # Saltos
        self.saltos_pendientes = 0
        self.fase_salto = 0
        self.fase_salto_maximo = 30
        self.jump_altura = 40

        self.area_rect = None

    # ---- Configuración -----
    def set_frames(self, idle_image, frames_walk, frames_jump=None):
        """
        Se encarga de cambiar los frames cuando se cambia de personaje.
        """
        old_midbottom = self.rect.midbottom
        self.idle_image = idle_image
        self.frames_walk = frames_walk
        self.image = self.frames_walk[0]
        self.frames_jump = frames_jump or [idle_image]
        self.rect = self.image.get_rect()
        self.rect.midbottom = old_midbottom

    def lugar_en_espacio(self, area_rect, align="left", margin_x=40, margin_bottom=20):
        """
        Coloca al personaje dentro del área visual del nivel.
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
        Inicia animación de caminata hacia la derecha.
        """

        self.area_rect = area_rect
        self.mode = "walk"
        self.moving = True

        # resetear animación
        self.current_frame = 0
        self.anim_timer = 0.0
        self.image = self.frames_walk[self.current_frame]

        pixeles_maximos = (
            area_rect.right - 40 - self.image.get_width() - self.start_x
        )
        distancia = min(pasos * pixels_por_paso, pixeles_maximos)

        self.rect.x = self.start_x
        self.target_x = self.start_x + distancia

    def iniciar_saltar(self, n_saltos, altura_salto=40, fase_salto_maximo=30):
        """
        Inicia animación de saltos.
        """
        self.mode = "jump"
        self.moving = True
        self.saltos_pendientes = n_saltos
        self.fase_salto = 0
        self.jump_altura = altura_salto
        self.fase_salto_maximo = fase_salto_maximo

        self.current_frame = 0
        self.anim_timer = 0.0

    # -------------- Actualiza ---------
    def actualizar(self):
        """
        Actualiza la animación del jugador.
        Devuelve:
            - "walk" cuando termina de caminar
            - "jump" cuando termina de saltar
            - None en cualquier otro caso
        """

        # ==========================
        # MODO CAMINAR
        # ==========================
        if self.mode == "walk":
            if not self.moving:
                return None

            # mover en X hasta el destino
            if self.rect.x < self.target_x:
                self.rect.x += self.speed
                if self.rect.x >= self.target_x:
                    self.rect.x = self.target_x
                    self.moving = False
                    self.mode = None
                    return "walk"
            else:
                # por seguridad: si ya está en o más allá del target
                self.moving = False
                self.mode = None
                return "walk"

            # animar frames de caminata
            if len(self.frames_walk) > 1:
                self.anim_timer += self.anim_speed
                if self.anim_timer >= 1:
                    self.anim_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.frames_walk)
                    self.image = self.frames_walk[self.current_frame]

            return None  # sigue caminando

        # ==========================
        # MODO SALTAR
        # ==========================
        if self.mode == "jump":
            if self.saltos_pendientes <= 0:
                self.rect.y = self.base_y
                self.mode = None
                self.moving = False
                return "jump"

            t = self.fase_salto / self.fase_salto_maximo
            if t < 0.5:
                # sube
                self.rect.y = self.base_y - int(self.jump_altura * (t * 2))
            else:
                # baja
                self.rect.y = self.base_y - int(self.jump_altura * (1 - (t - 0.5) * 2))

            if len(self.frames_jump) > 1:
                self.anim_timer += self.anim_speed
                if self.anim_timer >= 1:
                    self.anim_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.frames_jump)
                    self.image = self.frames_jump[self.current_frame]
            else:
                self.image = self.frames_jump[0]

            self.fase_salto += 1
            if self.fase_salto >= self.fase_salto_maximo:
                self.fase_salto = 0
                self.saltos_pendientes -= 1
                self.rect.y = self.base_y

                if self.saltos_pendientes <= 0:
                    self.mode = None
                    self.moving = False
                    return "jump"

            return None  # sigue saltando

        # ==========================
        # MODO NULO (quieto)
        # ==========================

        self.image = self.idle_image
        return None

    def dibujar(self, surface):
        surface.blit(self.image, self.rect)
