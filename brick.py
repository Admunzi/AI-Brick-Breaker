import random

import pygame
from conf import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        color, points = random.choice(list(BRICK_COLORS_AND_POINTS.items()))
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.points = points

    def update(self, game_manager):
        pass
