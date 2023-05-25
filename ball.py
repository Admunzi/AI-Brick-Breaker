from random import random
import pygame as pygame
from conf import *


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # the ball spawn aleatory in the width of the screen
        self.rect.center = (random() * WIDTH, HEIGHT / 2)

        self.speed_x = 5
        self.speed_y = 5

    def update(self, game_manager):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # if it touches any of the other sides, it revolts.
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1





