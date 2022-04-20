import time
import pygame
import sys

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

roadW = 2000  # road width (left to right)
segL = 200  # segment length (top to bottom)
camD = 0.84  # camera depth


class Line:
    def __init__(self):
        self.x = self.y = self.z = 0.0  # game position (3D space)
        self.X = self.Y = self.W = 0.0  # game position (2D projection)
        self.scale = 0.0  # scale from camera position

    def project(self, camX: int, camY: int, camZ: int):
        self.scale = camD / (self.z - camZ)
        self.X = (1 + self.scale * (self.x - self.camX)) * WINDOW_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - self.camY)) * WINDOW_HEIGHT / 2
        self.W = self.scale * roadW * WINDOW_WIDTH / 2


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
        pygame.display.set_caption("Racing Pseudo 3D")
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
