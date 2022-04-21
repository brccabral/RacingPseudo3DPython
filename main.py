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
        self.spriteX = 0.0  # sprite position X
        self.clip = 0.0  # correct sprite Y position
        self.sprite: pygame.Surface = None
        self.sprite_rect: pygame.Rect = None

        self.grass_color: pygame.Color = "black"
        self.rumble_color: pygame.Color = "black"
        self.road_color: pygame.Color = "black"

    def project(self, camX: int, camY: int, camZ: int):
        if not self.z:
            return
        if not self.z - camZ:
            return
        self.scale = camD / (self.z - camZ)
        self.X = (1 + self.scale * (self.x - camX)) * WINDOW_WIDTH / 2
        self.Y = (1 - self.scale * (self.y - camY)) * WINDOW_HEIGHT / 2
        self.W = self.scale * roadW * WINDOW_WIDTH / 2

    def drawSprite(self, draw_surface: pygame.Surface):
        if self.sprite is None:
            return
        w = self.sprite.get_width()
        h = self.sprite.get_height()
        destX = self.X + self.scale * self.spriteX * WINDOW_WIDTH / 2
        destY = self.Y + 4
        destW = w * self.W / 266
        destH = h * self.W / 266

        destX += destW * self.spriteX
        destY += destH * -1

        clipH = destY + destH - self.clip
        if clipH < 0:
            clipH = 0
        if clipH >= destH:
            return

        # avoid scalling up images which causes lag
        if destW > w:
            return
        # TODO : mask the sprite if below ground
        scaled_sprite = pygame.transform.scale(self.sprite, (destW, destH))
        draw_surface.blit(scaled_sprite, (destX, destY))


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

        # background
        self.background_image = pygame.image.load("images/bg.png").convert_alpha()
        self.background_surface = pygame.Surface(
            (self.background_image.get_width() * 2, self.background_image.get_height())
        )
        self.background_surface.blit(self.background_image, (0, 0))
        self.background_surface.blit(
            self.background_image, (self.background_image.get_width(), 0)
        )
        self.background_rect = self.background_surface.get_rect(topleft=(0, 0))
        self.window_surface.blit(self.background_surface, self.background_rect)

        # sprites
        self.sprites: List[pygame.Surface] = []
        for i in range(1, 8):
            self.sprites.append(pygame.image.load(f"images/{i}.png").convert_alpha())

    def run(self):

        # create road lines for each segment
        lines: List[Line] = []
        for i in range(1600):
            line = Line()
            line.z = i * segL

            # change color at every other 3 lines (int floor division)
            grass_color = light_grass if (i // 3) % 2 else dark_grass
            rumble_color = white_rumble if (i // 3) % 2 else black_rumble
            road_color = light_road if (i // 3) % 2 else dark_road

            line.grass_color = grass_color
            line.rumble_color = rumble_color
            line.road_color = road_color

            if 300 < i < 700:
                line.curve = 0.5

            if i > 750:
                line.y = math.sin(i / 30.0) * 1500

            # Sprites segments
            if i < 300 and i % 20 == 0:
                line.spriteX = -2.5
                line.sprite = self.sprites[4]

            if i % 17 == 0:
                line.spriteX = 2.0
                line.sprite = self.sprites[5]

            if i > 300 and i % 20 == 0:
                line.spriteX = -0.7
                line.sprite = self.sprites[3]

            if i > 800 and i % 20 == 0:
                line.spriteX = -1.2
                line.sprite = self.sprites[0]

            if i == 400:
                line.spriteX = -1.2
                line.sprite = self.sprites[6]

            lines.append(line)

        N = len(lines)
        pos = 0
        playerX = 0

        while True:
            self.dt = time.time() - self.last_time
            self.last_time = time.time()
            self.window_surface.fill("black")
            self.window_surface.blit(self.background_surface, self.background_rect)

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

                current.clip = maxy

                # don't draw "above ground"
                if current.Y >= maxy:
                    continue
                maxy = current.Y

                prev = lines[(n - 1) % N]  # previous line

                drawQuad(
                    self.window_surface,
                    current.grass_color,
                    0,
                    prev.Y,
                    WINDOW_WIDTH,
                    0,
                    current.Y,
                    WINDOW_WIDTH,
                )
                drawQuad(
                    self.window_surface,
                    current.rumble_color,
                    prev.X,
                    prev.Y,
                    prev.W * 1.2,
                    current.X,
                    current.Y,
                    current.W * 1.2,
                )
                drawQuad(
                    self.window_surface,
                    current.road_color,
                    prev.X,
                    prev.Y,
                    prev.W,
                    current.X,
                    current.Y,
                    current.W,
                )

            # draw sprites
            for n in range(startPos + 300, startPos, -1):
                lines[n % N].drawSprite(self.window_surface)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = GameWindow()
    game.run()
