import numpy as np

from .move import Move


class GameState:
    def __init__(self):
        self.board = np.array(
            [
                ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["--", "--", "--", "--", "--", "--", "--", "--"],
                ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]
        )

        self.white_to_move = True
        self.move_log = []

    def get_move(self, start_sq: tuple[int, int], end_sq: tuple[int, int]) -> Move:
        return Move(start_sq, end_sq, self.board)

    def make_move(self, move: Move) -> None:
        self.board[move.start_sq[0]][move.start_sq[1]] = "--"
        self.board[move.end_sq[0]][move.end_sq[1]] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self) -> None:
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_sq[0]][move.start_sq[1]] = move.piece_moved
            self.board[move.end_sq[0]][move.end_sq[1]] = move.piece_captured
            self.white_to_move = not self.white_to_move
        else:
            print("No moves to undo")
