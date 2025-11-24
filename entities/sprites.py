import pygame
import os


def cargar_spritesheet(ruta_imagen, num_frames, scale=1.0):

    sheet = pygame.image.load(ruta_imagen).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()

    frame_width = sheet_width // num_frames
    frame_height = sheet_height

    frames = []

    for i in range(num_frames):
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame_surface.blit(
            sheet, (0, 0), pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        )
        if scale != 1.0:
            frame_surface = pygame.transform.scale(
                frame_surface, (int(frame_width * scale), int(frame_height * scale))
            )
            frames.append(frame_surface)
    return frames
