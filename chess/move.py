import numpy as np


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(
        self, start_sq: tuple[int, int], end_sq: tuple[int, int], board: np.ndarray
    ):
        self.start_sq = start_sq
        self.end_sq = end_sq
        self.piece_moved = board[start_sq[0]][start_sq[1]]
        self.piece_captured = board[end_sq[0]][end_sq[1]]
        self.move_id = (
            start_sq[0] * 1000 + start_sq[1] * 100 + end_sq[0] * 10 + end_sq[1]
        )

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def __str__(self):
        return self.get_chess_notation()

    def __hash__(self):
        return self.move_id

    def is_pawn_promotion(self) -> bool:
        return (
            (self.piece_moved == "wP" and self.end_sq[0] == 0)
            or (self.piece_moved == "bP" and self.end_sq[0] == 7)
        )

    def get_chess_notation(self) -> str:
        return self.get_rank_file(
            self.start_sq[0], self.start_sq[1]
        ) + self.get_rank_file(self.end_sq[0], self.end_sq[1])

    def get_rank_file(self, r: int, c: int) -> str:
        return self.cols_to_files[c] + self.rows_to_ranks[r]


