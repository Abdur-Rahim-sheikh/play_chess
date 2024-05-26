import pygame as p
import logging
from chess import GameState

logger = logging.getLogger(__name__)
WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    if IMAGES:
        return
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(
                screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def draw_pieces(screen, board):
    # we want first two rows and last two rows only for initial
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece == "--":
                continue
            screen.blit(
                IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    valid_moves = gs.all_valid_moves()
    move_made = False  # flag variable for when a move is made
    load_images()
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = gs.get_move(player_clicks[0], player_clicks[1])

                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                    else:
                        logger.warning(
                            f"Invalid move: {move}, allowed are:{[str(move) for move in valid_moves]}"
                        )
                    sq_selected = ()
                    player_clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and p.key.get_mods() and p.KMOD_CTRL:
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.all_valid_moves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
