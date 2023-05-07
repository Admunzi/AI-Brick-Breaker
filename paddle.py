import pygame
from conf import *


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((100, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 10)

        self.speed = 5

    def update(self, game_manager):
        key_state = pygame.key.get_pressed()

        if key_state[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_state[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
