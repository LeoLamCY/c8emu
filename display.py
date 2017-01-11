import pygame
from chip8 import Chip8
import numpy as np
from PIL import Image
import pygame.surfarray as surfarray
from pygame import midi
import time

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
        self.sound = pygame.mixer.Sound('sound\\beep.wav')

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

            self.draw_screen()

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

    def draw_screen(self):
        surf = pygame.surfarray.make_surface(self.viewport)
        surf = pygame.transform.scale(
            surf, (self.screen_width, self.screen_height))
        self.screen.blit(surf, (0, 0))

    def draw_sprite(self, x, y, sprite):
        collision = 0
        for i in range(len(sprite)):
            for j in range(8):
                x_pos = x + j
                y_pos = y + i

                if x_pos >= self.width or x_pos < 0:
                    continue

                if y_pos >= self.height or y_pos < 0:
                    continue

                shifted = sprite[i] << j
                if shifted & 0x80 > 0:
                    if self.viewport[x_pos][y_pos] == 250:
                        self.viewport[x_pos][y_pos] = 0
                        collision = 1
                    else:
                        self.viewport[x_pos][y_pos] = 250

        self.viewport_changed = True
        return collision

    def pause(self):
        self.paused = True

    def isKeyPressed(self, key):
        return pygame.key.get_pressed()[self.keys[key]]

    def playSound(self):
        self.sound.play()
