import pygame
from chip8 import Chip8
import numpy as np
from PIL import Image
import pygame.surfarray as surfarray

# numpy height width
# pillow width height


class Display(object):
    screen_width = 320
    screen_height = 160
    width = 64
    height = 32
    viewport = np.zeros((width, height), np.uint8)
    resized_viewport = Image.fromarray(
        viewport).resize((screen_width, screen_height))
    color = (255, 255, 255)
    viewport_changed = False
    paused = False
    keys = {
        1: pygame.K_1,
        2: pygame.K_2,
        3: pygame.K_3,
        4: pygame.K_q,
        5: pygame.K_w,
        6: pygame.K_e,
        7: pygame.K_a,
        8: pygame.K_s,
        9: pygame.K_d,
        10: pygame.K_z,
        0: pygame.K_x,
        11: pygame.K_c,
        12: pygame.K_4,
        13: pygame.K_5,
        14: pygame.K_6,
        15: pygame.K_7
    }

    def __init__(self, rom):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        self.done = False

        self.chip8 = Chip8(self)
        self.chip8.load_rom(rom)
        self.clock = pygame.time.Clock()

    def start(self):
        x = 0
        y = 0
        self.viewport_changed = True

        while not self.done:
            if not self.paused:
                self.chip8.emulateCycle()
            if not self.chip8.running:
                self.done = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.paused = False

            # pressed = pygame.key.get_pressed()
            # if pressed[pygame.K_UP]:
            #     y += 3
            # pygame.draw.rect(self.screen, self.color,
            #                  pygame.Rect(x, y, 60, 60))

            # for y in range(20):
            #     for x in range(50):
            #         self.viewport[y][x] = 1

            if self.viewport_changed:
                self.draw_screen()
                self.viewport_changed = False
            # self.draw_screen()
            pygame.display.flip()
            self.clock.tick(400)

    def clear_screen(self):
        self.screen.fill((0, 0, 0))
        self.viewport = np.zeros((self.width, self.height), np.uint8)
        self.viewport_changed = True

    def resize_viewport(self):
        self.resized_viewport = Image.fromarray(
            self.viewport).resize((self.screen_width, self.screen_height))
        self.resized_viewport = np.array(self.resized_viewport, np.uint8)
        # print(self.viewport.shape)
        # print(self.resized_viewport.shape)

    def draw_screen(self):
        # self.resize_viewport()
        # self.screen.fill((0, 0, 0))
        surf = pygame.surfarray.make_surface(self.viewport)
        surf = pygame.transform.scale(
            surf, (self.screen_width, self.screen_height))
        self.screen.blit(surf, (0, 0))
        # screen_pixel_array = pygame.PixelArray(self.screen)
        # for y in range(self.screen_height):
        #     for x in range(self.screen_width):
        #         if surf.get_at((x, y)) != (0, 0, 0, 255):
        #             screen_pixel_array[x][y] = self.color

    def draw_sprite(self, x, y, sprite):
        collision = 0
        # self.viewport = np.zeros((self.width, self.height), np.uint8)
        for i in range(len(sprite)):
            for j in range(8):
                x_pos = x + j
                y_pos = y + i

                if x_pos >= self.width:
                    # x_pos -= self.width
                    continue
                elif x_pos < 0:
                    # x_pos += self.width
                    continue

                if y_pos >= self.height:
                    # y_pos -= self.height
                    continue
                elif y_pos < 0:
                    # y += self.height
                    continue

                shifted = sprite[i] << j
                # if sprite == [128]:
                #     print(x_pos, y_pos)
                #     print(sprite)
                if shifted & 0x80 > 0:
                    if self.viewport[x_pos][y_pos] == 250:
                        self.viewport[x_pos][y_pos] = 0
                        collision = 1
                    else:
                        self.viewport[x_pos][y_pos] = 250

        self.viewport_changed = True
        return collision

        # pixel = pygame.Surface((1, 1))
        # pixel.fill(color)
        # for y in range(height):
        #     for x in range(width):

    def pause(self):
        self.paused = True

    def isKeyPressed(self, key):
        return pygame.key.get_pressed()[self.keys[key]]
