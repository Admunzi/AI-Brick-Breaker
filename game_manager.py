import pickle
import numpy as np
import pygame
from brick import Brick
from paddle import Paddle
from ball import Ball
from conf import *
from math import ceil, floor

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
CLOCK = pygame.time.Clock()


def create_sprites():
    all_sprites = pygame.sprite.Group()
    bricks_sprites = pygame.sprite.Group()
    paddle, ball = Paddle(), Ball()

    # Add bricks to sprite groups
    for i in range(BRICK_COLUMNS):
        for j in range(BRICK_ROWS):
            # Create brick cords x and y, spacing between bricks and center the bricks in the screen
            brick = Brick(i * (BRICK_WIDTH + BRICK_SPACING) + BRICK_SPACING + 50,
                          j * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_SPACING + 50)

            all_sprites.add(brick)
            bricks_sprites.add(brick)

    # Add sprites to sprite groups
    all_sprites.add(paddle)
    all_sprites.add(ball)

    return all_sprites, bricks_sprites, ball, paddle


def draw_text(text, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    SCREEN.blit(text_surface, text_rect)


class GameManager:
    def __init__(self):
        self.life = 3
        self.game_over = False

        self.action_space = ['Right', 'Left']
        self.state = [0, 0, 0]
        self._step_penalization = 0
        self.total_reward = 0

        rows = ceil(HEIGHT / 5)
        columns = ceil(WIDTH / 3.75)

        self.positions_space = np.array([[[0 for z in range(columns)]
                                          for y in range(rows)]
                                         for x in range(rows)])

        self.all_sprites, self.bricks_sprites, self.ball, self.paddle = create_sprites()

    def reset(self):
        self.life = 3
        self.game_over = False
        self.state = [0, 0, 0]
        self._step_penalization = 0

        self.all_sprites, self.bricks_sprites, self.ball, self.paddle = create_sprites()

        return self.state

    def step(self, action, animate=False):
        score = self.apply_action(action, animate)
        done = self.life <= 0  # final
        reward = score - self._step_penalization
        self.total_reward += reward
        return self.state, reward, done

    def apply_action(self, action, animate=False):
        self.paddle.move(action)
        score = self.advances_frame()

        if animate:
            self._animate_frame()

        self.state = [floor(self.paddle.rect.x / 5), floor(self.ball.rect.x / 5), floor(self.ball.rect.y / 5)]
        return score

    def _animate_frame(self):
        CLOCK.tick(FPS)

        # Draw / render
        SCREEN.fill(BLACK)
        self.all_sprites.draw(SCREEN)

        draw_text(str(self.get_life()) + " Lifes", 18, WIDTH - 40, 10)

        # After drawing everything, flip the display
        pygame.display.flip()

    def advances_frame(self):
        self.all_sprites.update(self)
        score = 0

        self.check_ball_hit_bricks()
        if self.check_ball_hit_paddle():
            score += 20
        if self.check_ball_hit_bottom():
            score -= 5

        return score

    def check_ball_hit_bottom(self):
        if self.ball.rect.bottom > HEIGHT - 5:
            self.ball.rect.center = (WIDTH / 2, HEIGHT / 2)
            self.lose_life()
            return True

    def check_ball_hit_paddle(self):
        if self.paddle.rect.colliderect(self.ball.rect):
            self.ball.speed_y *= -1
            return True

    def check_ball_hit_bricks(self):
        hits = pygame.sprite.spritecollide(self.ball, self.bricks_sprites, True)
        if hits:
            self.ball.speed_y *= -1

    def lose_life(self):
        self.life -= 1

    def get_life(self):
        return self.life

    def set_game_over(self, game_over):
        self.game_over = game_over

    def get_game_over(self):
        return self.game_over

    def get_total_reward(self):
        return self.total_reward

    def save(self):
        # Create a dictionary with all the data to save
        data = {
            'state': self.state,
            '_step_penalization': self._step_penalization,
            'total_reward': self.total_reward,
            'positions_space': self.positions_space,
        }

        with open("result/game.obj", 'wb') as file:
            pickle.dump(data, file)

    def load(self):
        with open("result/game.obj", 'rb') as file:
            data = pickle.load(file)

        self.state = data['state']
        self._step_penalization = data['_step_penalization']
        self.positions_space = data['positions_space']
