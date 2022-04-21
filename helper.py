from typing import Tuple
import pygame


def debug(message: str, surface: pygame.Surface, pos: Tuple[int, int]):
    font = pygame.font.SysFont("Arial", 15)
    text = font.render(f"{message}", True, "black")
    surface.blit(text, pos)
