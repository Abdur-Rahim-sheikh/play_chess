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

    def all_valid_moves(self):
        # for now all possible moves are valid, not considering check
        return self.all_possible_moves()

    def all_possible_moves(
        self,
    ):
        moves = []

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.white_to_move) or (
                    turn == "b" and not self.white_to_move
                ):
                    piece = self.board[r][c][1]
                    if piece == "P":
                        self.pawn_moves(r, c, moves)
                    elif piece == "R":
                        self.rook_moves(r, c, moves)
                    elif piece == "N":
                        self.knight_moves(r, c, moves)
                    elif piece == "B":
                        self.bishop_moves(r, c, moves)
                    elif piece == "Q":
                        self.queen_moves(r, c, moves)
                    elif piece == "K":
                        self.king_moves(r, c, moves)
        return moves

    def pawn_moves(self, r, c, moves):
        pass

    def rook_moves(self, r, c, moves):
        pass

    def knight_moves(self, r, c, moves):
        pass

    def bishop_moves(self, r, c, moves):
        pass

    def queen_moves(self, r, c, moves):
        pass

    def king_moves(self, r, c, moves):
        pass
