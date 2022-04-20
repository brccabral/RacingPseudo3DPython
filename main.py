import time
import pygame
import sys

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768


def drawQuad(
    surface: pygame.Surface,
    color: pygame.Color,
    x1: int,
    y1: int,
    w1: int,
    x2: int,
    y2: int,
    w2: int,
):
    pygame.draw.polygon(
        surface, color, [(x1 - w1, y1), (x2 - w2, y2), (x2 + w2, y2), (x1 + w1, y1)]
    )


class GameWindow:
    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.dt = 0

    def run(self):
        self.dt = time.time() - self.last_time
        self.last_time = time.time()
        while True:
            self.window_surface.fill("black")

            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            drawQuad(self.window_surface, "green", 500, 500, 200, 500, 300, 100)

            pygame.display.flip()


if __name__ == "__main__":
    game = GameWindow()
    game.run()
