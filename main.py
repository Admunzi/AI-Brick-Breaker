"""
Brick Breaker game in Python using pygame. It will be only one player.
Will use reinforcement learning to learn how to play.

The game is vertical, so the paddle will move left or right.

"""
import pickle

import numpy as np
from brick_breaker_agent import BrickBreakerAgent
import game_manager


def main():
    menu()


def menu():
    # show menu if user want train or use a trained model
    print("Welcome to Brick Breaker!")
    print("1. Train a new model")
    print("2. Use a trained model")
    print("3. Exit")
    option = input("Select an option: ")
    while option not in ['1', '2', '3']:
        option = input("Select an option: ")

    if option == '1':
        print("Training a new model")
        train()
    elif option == '2':
        print("Using a trained model")
        trained_model()
    elif option == '3':
        print("Bye!")
        exit()


def train():
    learner, game = play(rounds=200000, discount_factor=0.2, learning_rate=0.1, exploitation_ratio=0.85,
                         animate=False)
    save_model(game, learner)


def trained_model():
    game, learner = load_model()
    learner2 = BrickBreakerAgent(game, policy=learner.get_policy())
    learner2.exploitation_ratio = 1.0  # remove exploration from the trained model
    play(rounds=1, learner=learner2, game=game, animate=True)


def save_model(game, learner):
    game.save()
    learner.save()


def load_model():
    game = game_manager.GameManager()
    game.load()

    with open("result/learner.obj", "rb") as file:
        learner = pickle.load(file)
    return game, learner


def play(rounds=250, discount_factor=0.1, learning_rate=0.1,
         exploitation_ratio=0.9, learner=None, game=None, animate=False):
    if game is None:
        game = game_manager.GameManager()

    if learner is None:
        print("Begin new Train!")
        learner = BrickBreakerAgent(game, discount_factor=discount_factor, learning_rate=learning_rate,
                                    exploitation_ratio=exploitation_ratio)

    max_points = 0
    first_max_reached = 0
    total_rw = 0
    steps = []

    for played_games in range(0, rounds):
        state = game.reset()
        reward, done = None, None

        itera = 0
        while (done != True) and (itera < 30000 and game.get_total_reward() <= 1000000):
            old_state = np.array(state)
            next_action = learner.get_next_step(state, game)
            state, reward, done = game.step(next_action, animate=animate)
            if rounds > 1:
                learner.update(game, old_state, next_action, reward, state, done)
            itera += 1

        steps.append(itera)

        total_rw += game.get_total_reward()
        if game.get_total_reward() > max_points:
            max_points = game.get_total_reward()
            first_max_reached = played_games

        if played_games % 500 == 0 and played_games > 1 and not animate:
            print("-- Partidas[", played_games, "] Avg.Puntos[", int(total_rw / played_games), "]  AVG Steps[",
                  int(np.array(steps).mean()), "] Max Score[", max_points, "]")
            save_model(game, learner)

    if played_games > 1:
        print('Partidas[', played_games, '] Avg.Puntos[', int(total_rw / played_games), '] Max score[', max_points,
              '] en partida[', first_max_reached, ']')

    # learner.print_policy()
    return learner, game


if __name__ == '__main__':
    main()
