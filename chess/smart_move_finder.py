import random
from chess import GameState, Move


class SmartMoveFinder:
    pieceScore = {
        "K": 0,
        "Q": 9,
        "R": 5,
        "B": 3,
        "N": 3,
        "P": 1,
    }
    CHECKMATE = 100
    STALEMATE = 0

    def __init__(self, depth=2):
        pass

    def find_move(self, gs: GameState, valid_moves: set) -> Move:
        # return self.find_random_move(valid_moves)
        return self.find_greedy_move(gs, valid_moves)

    def score_board(self, board: list) -> int:
        score = 0
        for row in board:
            for square in row:
                if square[0] == "w":
                    score += self.pieceScore[square[1]]
                if square[0] == "b":
                    score -= self.pieceScore[square[1]]
        return score

    @staticmethod
    def find_random_move(valid_moves: set) -> Move:
        return random.choice(list(valid_moves))

    def find_greedy_move(self, gs: GameState, valid_moves: set) -> Move:
        turn_multiplier = 1 if gs.white_to_move else -1
        max_score = -self.CHECKMATE
        best_move = None
        for player_move in valid_moves:
            gs.make_move(player_move)
            if gs.checkmate:
                score = self.CHECKMATE
            elif gs.stalemate:
                score = self.STALEMATE
            else:
                score = turn_multiplier * self.score_board(gs.board)
            gs.undo_move()
            if score > max_score:
                max_score = score
                best_move = player_move

        return best_move
