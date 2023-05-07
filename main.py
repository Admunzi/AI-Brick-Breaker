"""
Brick Breaker game in Python using pygame. It will be only one player.
Will use reinforcement learning to learn how to play.

The game is vertical, so the paddle will move left or right.

"""

import pygame
from brick import Brick
from paddle import Paddle
from ball import Ball
from game_manager import GameManager
from conf import *

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")
CLOCK = pygame.time.Clock()
game_manager = GameManager()


def main():
    all_sprites, bricks_sprites, ball, paddle = create_sprites()

    start_game(all_sprites, ball, bricks_sprites, paddle)

    if game_manager.get_game_over():
        print("Game Over")
        print(f"{game_manager.get_score()} points collected")
    else:
        print("You Win")
        print(f"{game_manager.get_score()} points collected")

    pygame.quit()


def start_game(all_sprites, ball, bricks_sprites, paddle):
    running = True
    while running:
        CLOCK.tick(FPS)
        running = check_events_game(running)

        if game_manager.get_life() <= 0:
            game_manager.set_game_over(True)
            running = False

        if len(bricks_sprites) == 0:
            game_manager.set_game_over(False)
            running = False

        all_sprites.update(game_manager)

        check_ball_hit_paddle(ball, paddle)
        check_ball_hit_bricks(ball, bricks_sprites)

        # Draw / render
        SCREEN.fill(BLACK)
        all_sprites.draw(SCREEN)

        draw_text(SCREEN, "Score " + str(game_manager.get_score()), 18, 50, 10)
        draw_text(SCREEN, str(game_manager.get_life()) + " Lifes", 18, WIDTH - 40, 10)

        # After drawing everything, flip the display
        pygame.display.flip()


def check_events_game(running):
    # Events in the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


def check_ball_hit_paddle(ball, paddle):
    hits = ball.rect.colliderect(paddle.rect)
    if hits:
        ball.speed_y *= -1


def check_ball_hit_bricks(ball, bricks_sprites):
    hits = pygame.sprite.spritecollide(ball, bricks_sprites, True)
    if hits:
        ball.speed_y *= -1
        game_manager.add_score(hits[0].points)


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


def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont('Arial', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


if __name__ == '__main__':
    main()
