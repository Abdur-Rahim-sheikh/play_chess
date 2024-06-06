import random

class SmartMoveFinder:
    def __init__(self, depth=2):
        pass

    def find_move(self, valid_moves, board):
        return find_random_move(valid_moves)
def find_random_move(valid_moves: set):
    return random.choice(list(valid_moves))