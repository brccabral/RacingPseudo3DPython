import math
import time
from typing import List
import pygame
import sys

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

roadW = 2000  # road width (left to right)
segL = 200  # segment length (top to bottom)
camD = 0.84  # camera depth

dark_grass = pygame.Color(0, 154, 0)
light_grass = pygame.Color(16, 200, 16)
white_rumble = pygame.Color(255, 255, 255)
black_rumble = pygame.Color(0, 0, 0)
dark_road = pygame.Color(105, 105, 105)
light_road = pygame.Color(107, 107, 107)


class Line:
    def __init__(self):
        self.x = self.y = self.z = 0.0  # game position (3D space)
        self.X = self.Y = self.W = 0.0  # game position (2D projection)
        self.scale = 0.0  # scale from camera position
        self.curve = 0.0  # curve radius

    def project(self, camX: int, camY: int, camZ: int):
        if not self.z:
            return
        if not self.z - camZ:
            return
        self.scale = camD / (self.z - camZ)
        self.X = (1 + self.scale * (self.x - camX)) * WINDOW_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * WINDOW_HEIGHT / 2
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

        # create road lines for each segment
        lines: List[Line] = []
        for i in range(1600):
            line = Line()
            line.z = i * segL

            if 300 < i < 700:
                line.curve = 0.5

            if i > 750:
                line.y = math.sin(i / 30.0) * 1500

            lines.append(line)

        N = len(lines)
        pos = 0
        playerX = 0

        while True:
            self.dt = time.time() - self.last_time
            self.last_time = time.time()
            self.window_surface.fill("black")

            for event in pygame.event.get([pygame.QUIT]):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                pos += 200
            if keys[pygame.K_DOWN]:
                pos -= 200
            if keys[pygame.K_RIGHT]:
                playerX += 200
            if keys[pygame.K_LEFT]:
                playerX -= 200

            # loop the circut from start to finish
            while pos >= N * segL:
                pos -= N * segL
            while pos < 0:
                pos += N * segL
            startPos = pos // segL

            x = dx = 0.0  # curve offset on x axis

            camH = 1500 + lines[startPos].y
            maxy = WINDOW_HEIGHT

            # draw road
            for n in range(startPos, startPos + 300):
                current = lines[n % N]
                # loop the circut from start to finish = pos - (N * segL if n >= N else 0)
                current.project(playerX - x, camH, pos - (N * segL if n >= N else 0))
                x += dx
                dx += current.curve

                # don't draw "above ground"
                if current.Y >= maxy:
                    continue
                maxy = current.Y

                prev = lines[(n - 1) % N]  # previous line

                # change color at every other 3 lines (int floor division)
                grass_color = light_grass if (n // 3) % 2 else dark_grass
                rumble_color = white_rumble if (n // 3) % 2 else black_rumble
                road_color = light_road if (n // 3) % 2 else dark_road

                drawQuad(
                    self.window_surface,
                    grass_color,
                    0,
                    prev.Y,
                    WINDOW_WIDTH,
                    0,
                    current.Y,
                    WINDOW_WIDTH,
                )
                drawQuad(
                    self.window_surface,
                    rumble_color,
                    prev.X,
                    prev.Y,
                    prev.W * 1.2,
                    current.X,
                    current.Y,
                    current.W * 1.2,
                )
                drawQuad(
                    self.window_surface,
                    road_color,
                    prev.X,
                    prev.Y,
                    prev.W,
                    current.X,
                    current.Y,
                    current.W,
                )

            pygame.display.flip()
            # self.clock.tick(60)


if __name__ == "__main__":
    game = GameWindow()
    game.run()
