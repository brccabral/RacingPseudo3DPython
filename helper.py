import pygame


def debug(message: str):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("Arial", 15)
    text = font.render(f"{message}", True, "white")
    screen.blit(text, [10, 10])
