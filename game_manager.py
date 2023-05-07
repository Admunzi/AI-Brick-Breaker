class GameManager:
    def __init__(self):
        self.life = 3
        self.score = 0
        self.game_over = False

    def add_score(self, score):
        self.score += score

    def get_score(self):
        return self.score

    def lose_life(self):
        self.life -= 1

    def get_life(self):
        return self.life

    def set_game_over(self, game_over):
        self.game_over = game_over

    def get_game_over(self):
        return self.game_over
