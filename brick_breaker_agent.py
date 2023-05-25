import pickle
import numpy as np
import pygame


class BrickBreakerAgent:
    def __init__(self, game, policy=None, discount_factor=0.1, learning_rate=0.1, exploitation_ratio=0.9):

        if policy is not None:
            self._q_table = policy
        else:
            position = list(game.positions_space.shape)
            position.append(len(game.action_space))
            self._q_table = np.zeros(position)

        self.discount_factor = discount_factor
        self.learning_rate = learning_rate
        self.exploitation_ratio = exploitation_ratio

    def get_next_step(self, state, game):
        pygame.event.get()
        # Aleatory step
        next_step = np.random.choice(list(game.action_space))

        # If the random number is less than the exploitation ratio, we take the maximum
        if np.random.uniform() <= self.exploitation_ratio:
            # We take the maximum value of the q_table
            idx_action = np.random.choice(np.flatnonzero(
                self._q_table[state[0], state[1], state[2]] == self._q_table[state[0], state[1], state[2]].max()
            ))
            next_step = list(game.action_space)[idx_action]

        return next_step

    # Update the q_table
    def update(self, game, old_state, action_taken, reward_action_taken, new_state, reached_end):
        idx_action_taken = list(game.action_space).index(action_taken)

        actual_q_value_options = self._q_table[old_state[0], old_state[1], old_state[2]]
        actual_q_value = actual_q_value_options[idx_action_taken]

        future_q_value_options = self._q_table[new_state[0], new_state[1], new_state[2]]
        future_max_q_value = reward_action_taken + self.discount_factor * future_q_value_options.max()
        if reached_end:
            future_max_q_value = reward_action_taken  # maximum reward

        self._q_table[old_state[0], old_state[1], old_state[2], idx_action_taken] = actual_q_value + \
                                                            self.learning_rate * (future_max_q_value - actual_q_value)

    def get_policy(self):
        return self._q_table

    def save(self):
        with open("result/learner.obj", 'wb') as file:
            pickle.dump(self, file)
