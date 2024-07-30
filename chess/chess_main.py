import logging

import pygame as p

from chess import GameState, SmartMoveFinder

logger = logging.getLogger(__name__)
WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
colors = []


def load_images():
    if IMAGES:
        return
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


def highlight_squares(screen, gs, valid_moves, sq_selected):
    if sq_selected:
        r, c = sq_selected
        if gs.board[r][c][0] == ("w" if gs.white_to_move else "b"):
            # highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency value
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color("yellow"))
            for move in valid_moves:
                if move.start_sq == (r, c):
                    screen.blit(s, (move.end_sq[1] * SQ_SIZE, move.end_sq[0] * SQ_SIZE))


def draw_game_state(screen, gs, valid_moves, sq_selected):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, sq_selected)
    draw_pieces(screen, gs.board)


def draw_board(screen):
    global colors
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


def animate_move(move, screen, board, clock):
    global colors
    delta_r = move.end_sq[0] - move.start_sq[0]
    delta_c = move.end_sq[1] - move.start_sq[1]
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(delta_r) + abs(delta_c)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (
            move.start_sq[0] + delta_r * frame / frame_count,
            move.start_sq[1] + delta_c * frame / frame_count,
        )
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[0] if (move.end_sq[0] + move.end_sq[1]) % 2 == 0 else colors[1]
        end_square = p.Rect(
            move.end_sq[1] * SQ_SIZE, move.end_sq[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE
        )
        p.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != "--":
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        logger.warning(
            f"Moving {move.piece_moved} to {r}, {c} and capturing {move.piece_captured}"
        )
        screen.blit(
            IMAGES[move.piece_moved],
            p.Rect(int(c * SQ_SIZE), int(r * SQ_SIZE), SQ_SIZE, SQ_SIZE),
        )
        p.display.flip()
        clock.tick(60)


def draw_end_game_text(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, True)
    text_object = font.render(text, 0, p.Color("Gray"))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(
        WIDTH / 2 - text_object.get_width() / 2,
        HEIGHT / 2 - text_object.get_height() / 2,
    )
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color("Red"))
    screen.blit(text_object, text_location.move(2, 2))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    smf = SmartMoveFinder()
    valid_moves = gs.all_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False
    load_images()
    running = True
    sq_selected = ()  # no square is selected, keep track of the last click of the user (tuple: (row, col))
    player_clicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])

    player_one = True  # if a human is playing white, then this will be True, if an AI is playing then it will be False
    player_two = False  # same as above but for black
    while running:
        human_turn = (gs.white_to_move and player_one) or (
            not gs.white_to_move and player_two
        )

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not human_turn:
                    continue
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
                        animate = True
                    else:
                        logger.warning(
                            f"Invalid move: {move}, allowed are:{[str(move) for move in valid_moves]}"
                        )
                    sq_selected = ()
                    player_clicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and p.key.get_mods() and p.KMOD_CTRL:
                    gs.undo_move()

                    if len(gs.move_log) % 2 == 0:
                        gs.undo_move()
                    move_made = True
                elif e.key == p.K_r and p.key.get_mods() and p.KMOD_CTRL:
                    gs = GameState()
                    valid_moves = gs.all_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False

        if move_made:
            valid_moves = gs.all_valid_moves()
        # AI move finder logic
        if not gs.checkmate and not gs.stalemate and not human_turn:
            ai_move = smf.find_move(gs, valid_moves)
            gs.make_move(ai_move)
            move_made = True
            animate = True
        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.all_valid_moves()
            move_made = False
            animate = False
        draw_game_state(screen, gs, valid_moves, sq_selected)
        if gs.checkmate:
            if gs.white_to_move:
                draw_end_game_text(screen, "Black wins by checkmate")
            else:
                draw_end_game_text(screen, "White wins by checkmate")
        elif gs.stalemate:
            draw_end_game_text(screen, "Stalemate")
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
