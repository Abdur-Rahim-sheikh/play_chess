import logging

import numpy as np

from .move import Move

logger = logging.getLogger(__name__)


class GameState:
    BLANK = "--"

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
        self.kings_position = {
            "w": (7, 4),
            "b": (0, 4),

        }
        self.move_log = []
        self.move_functions = {
            "P": self.pawn_moves,
            "R": self.rook_moves,
            "N": self.knight_moves,
            "B": self.bishop_moves,
            "Q": self.queen_moves,
            "K": self.king_moves,
        }

    def get_move(self, start_sq: tuple[int, int], end_sq: tuple[int, int]) -> Move:
        return Move(start_sq, end_sq, self.board)

    def make_move(self, move: Move) -> None:
        self.board[move.start_sq[0]][move.start_sq[1]] = "--"
        self.board[move.end_sq[0]][move.end_sq[1]] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved[1] == 'K':
            self.kings_position[move.piece_moved[0]] = (move.end_sq[0], move.end_sq[1])

    def undo_move(self) -> None:
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_sq[0]][move.start_sq[1]] = move.piece_moved
            self.board[move.end_sq[0]][move.end_sq[1]] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved[1] == 'K':
                self.kings_position[move.piece_moved[0]] = (move.start_sq[0], move.start_sq[1])
        else:
            logger.info("No moves to undo")

    def all_valid_moves(self) -> set[Move]:
        # generate all possible moves
        moves = self.all_possible_moves()
        #  for each move make opponent's move
        for move in list(moves):
            self.make_move(move)
            self.white_to_move = not self.white_to_move # to be able to know if in check the same color
            #  generate all possible moves for opponent after our move
            # if opponent can capture our king, remove that move
            if self.in_check():
                moves.remove(move)
            self.white_to_move = not self.white_to_move
            self.undo_move()
        

        return moves

    def in_check(self) -> bool:
        king_color = "w" if self.white_to_move else "b"
        return self.square_under_attack(self.kings_position[king_color])


    def square_under_attack(self, sq: tuple[int, int]) -> bool:
        self.white_to_move = not self.white_to_move
        opponent_moves = self.all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_sq == sq:
                return True
        return False

    def all_possible_moves(self) -> set[Move]:
        moves = set()

        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece_color = self.board[r][c][0]
                if (piece_color == "w" and self.white_to_move) or (
                    piece_color == "b" and not self.white_to_move
                ):
                    piece = self.board[r][c][1]
                    if piece == self.BLANK:
                        continue
                    self.move_functions[piece](r, c, moves)
        return moves

    def __valid_move(self, start_sq: tuple[int, int], end_sq: tuple[int, int]) -> bool:
        return (
            0 <= end_sq[0] < 8
            and 0 <= end_sq[1] < 8
            and start_sq != end_sq
            and self.board[start_sq[0]][start_sq[1]][0]
            != self.board[end_sq[0]][end_sq[1]][0]
        )

    def __fill_direction(self, r, c, dr, dc, moves) -> None:
        row, col = r + dr, c + dc

        while self.__valid_move((r, c), (row, col)):
            
            moves.add(self.get_move((r, c), (row, col)))

            if self.board[row][col] != self.BLANK:
                break
            row, col = row + dr, col + dc
        

    def pawn_moves(self, r, c, moves) -> None:
        if self.white_to_move:
            if r - 1 >= 0 and self.board[r - 1][c] == "--":
                moves.add(self.get_move((r, c), (r - 1, c)))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.add(self.get_move((r, c), (r - 2, c)))

            if r - 1 >= 0 and c - 1 >= 0 and self.board[r - 1][c - 1][0] == "b":
                moves.add(self.get_move((r, c), (r - 1, c - 1)))
            if r - 1 >= 0 and c + 1 < 8 and self.board[r - 1][c + 1][0] == "b":
                moves.add(self.get_move((r, c), (r - 1, c + 1)))
        else:
            if r + 1 < 8 and self.board[r + 1][c] == "--":
                moves.add(self.get_move((r, c), (r + 1, c)))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.add(self.get_move((r, c), (r + 2, c)))
            if r + 1 < 8 and c - 1 >= 0 and self.board[r + 1][c - 1][0] == "w":
                moves.add(self.get_move((r, c), (r + 1, c - 1)))
            if r + 1 < 8 and c + 1 < 8 and self.board[r + 1][c + 1][0] == "w":
                moves.add(self.get_move((r, c), (r + 1, c + 1)))

    def rook_moves(self, r:int, c:int, moves:set[Move]) -> None:

        #   left
        self.__fill_direction(r, c, -1, 0, moves)
        #   right
        self.__fill_direction(r, c, 1, 0, moves)
        #   up
        self.__fill_direction(r, c, 0, -1, moves)
        #   down
        self.__fill_direction(r, c, 0, 1, moves)

    def knight_moves(self, r:int, c:int, moves:set[Move]) -> None:
        hops = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        for dr, dc in hops:
            if self.__valid_move((r, c), (r + dr, c + dc)):
                moves.add(self.get_move((r, c), (r + dr, c + dc)))

    def bishop_moves(self, r:int, c:int, moves:set[Move]) -> None:

        #   up left
        self.__fill_direction(r, c, -1, -1, moves)
        #   up right
        self.__fill_direction(r, c, 1, -1, moves)
        #   down left
        self.__fill_direction(r, c, -1, 1, moves)
        #   down right
        self.__fill_direction(r, c, 1, 1, moves)

    def queen_moves(self, r:int, c:int, moves:set[Move]) -> None:

        #  rook moves
        self.rook_moves(r, c, moves)
        #  bishop moves
        self.bishop_moves(r, c, moves)

    def king_moves(self, r:int, c:int, moves:set[Move])-> None:
        around = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (1, 1),
        ]
        for dr, dc in around:
            row, col = r + dr, c + dc
            if self.__valid_move((r, c), (row, col)):
                moves.add(self.get_move((r, c), (row, col)))
