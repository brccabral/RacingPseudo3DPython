import time
import pygame
import sys


class GameWindow:
    def __init__(self):
        pygame.init()
        self.window_surface = pygame.display.set_mode((640, 480))
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

            pygame.display.flip()


if __name__ == "__main__":
    game = GameWindow()
    game.run()
