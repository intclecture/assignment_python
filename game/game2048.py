import pygame
import random

# Definitions
BOARD_SIZE = 800
SCORE_PANEL_HEIGHT = 90
WIDTH = BOARD_SIZE
HEIGHT = BOARD_SIZE + SCORE_PANEL_HEIGHT
GRID_SIZE = 4
TILE_SIZE = BOARD_SIZE // GRID_SIZE
TILE_MARGIN = 3
TEXT_SIZE = 60
SCORE_TEXT_SIZE = 42
MODE_TEXT_SIZE = 24
NOTIFY_TEXT_SIZE = 30
AUTO_MOVE_DELAY_MS = 140

# Colors​
BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR = (0, 0, 0)
DEFAULT_TILE_COLOR = (60, 58, 50)


def draw_cell(screen, row, col, value):
    rect = pygame.Rect(
        col * TILE_SIZE + TILE_MARGIN,
        SCORE_PANEL_HEIGHT + row * TILE_SIZE + TILE_MARGIN,
        TILE_SIZE - TILE_MARGIN * 2,
        TILE_SIZE - TILE_MARGIN * 2,
    )

    try:
        cell_color = TILE_COLORS[value]
    except KeyError:
        cell_color = DEFAULT_TILE_COLOR
    pygame.draw.rect(screen, cell_color, rect)
    if value != 0:
        text_screen = font.render(str(value), True, TEXT_COLOR)
        cell_x = rect.centerx - (text_screen.get_width() // 2)
        cell_y = rect.centery - (text_screen.get_height() // 2)
        screen.blit(text_screen, (cell_x, cell_y))


def draw_score(screen, score):
    score_text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    text_x = 20
    text_y = (SCORE_PANEL_HEIGHT - score_text.get_height()) // 2
    screen.blit(score_text, (text_x, text_y))


def draw_mode_status(screen, auto_mode):
    mode_text = "AUTO: ON (A)" if auto_mode else "AUTO: OFF (A)"
    mode_surface = mode_font.render(mode_text, True, TEXT_COLOR)
    x = WIDTH - mode_surface.get_width() - 20
    y = (SCORE_PANEL_HEIGHT - mode_surface.get_height()) // 2
    screen.blit(mode_surface, (x, y))


def draw_game_over_notice(screen):
    # Draw a dimmed layer to focus attention on the game over message.
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    message = notify_font.render("Play again? (y/n)", True, (255, 255, 255))

    message_x = (WIDTH - message.get_width()) // 2
    message_y = (HEIGHT - message.get_height()) // 2

    screen.blit(message, (message_x, message_y))


# Board render
def render_board(screen, board_map, score, auto_mode):
    draw_score(screen, score)
    draw_mode_status(screen, auto_mode)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            draw_cell(screen, row, col, board_map[row][col])


total_score = 0


def handle_key(key_event, board):
    global total_score
    new_board = None
    turn_score = 0
    match key_event:
        case pygame.K_LEFT:
            new_board, turn_score = rotate_and_merge(0, board)
        case pygame.K_RIGHT:
            new_board, turn_score = rotate_and_merge(2, board)
        case pygame.K_UP:
            new_board, turn_score = rotate_and_merge(3, board)
        case pygame.K_DOWN:
            new_board, turn_score = rotate_and_merge(1, board)
        case _:
            # Do nothing.
            pass
    total_score += turn_score
    return new_board


def spawn_tile(board_map):
    empty_cells = [
        (r, c)
        for r in range(GRID_SIZE)
        for c in range(GRID_SIZE)
        if board_map[r][c] == 0
    ]

    if empty_cells:
        v = random.choices([2, 4], weights=[0.9, 0.1])[0]
        r, c = random.choice(empty_cells)
        board_map[r][c] = v
        return True
    return False


def rotate(is_cw, board_map):
    new_map = None
    if is_cw:
        new_map = [list(r) for r in zip(*board_map[::-1])]
    else:
        new_map = [list(r) for r in zip(*board_map)][::-1]
    return new_map


def merge_row(row):
    org_len = len(row)
    new_row = []
    skip_merge = False
    score = 0

    for i in range(org_len):
        if skip_merge:
            skip_merge = False
            continue

        if row[i] == 0:
            continue
        elif i + 1 < len(row) and row[i] == row[i + 1]:
            new_row.append(row[i] * 2)
            skip_merge = True
            score += row[i]
            continue
        elif i < len(row):
            new_row.append(row[i])
    while len(new_row) < org_len:
        new_row.append(0)
    return new_row, score


def rotate_and_merge(rot, board):
    rotated_board = board

    # Rotate CW90
    for _ in range(rot):
        rotated_board = rotate(True, rotated_board)

    # Merge
    new_board = []
    score = 0
    for row in rotated_board:
        new_row, row_score = merge_row(row)
        score += row_score
        new_board.append(new_row)

    # Rotate CCW90
    for _ in range(rot):
        new_board = rotate(False, new_board)
    return new_board, score


def has_valid_moves(board_map):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell = board_map[row][col]
            if cell == 0:
                return True

            if col + 1 < GRID_SIZE and cell == board_map[row][col + 1]:
                return True
            if row + 1 < GRID_SIZE and cell == board_map[row + 1][col]:
                return True
    return False


def count_empty_cells(board_map):
    return sum(1 for row in board_map for cell in row if cell == 0)


# --- Expectimax AI ---

# Weights for the board evaluation heuristic.
_EMPTY_WEIGHT = 270
_MERGE_WEIGHT = 700
_MONO_WEIGHT = 47

# Snake-order monotonicity weights so high tiles gravitate to a corner.
_SNAKE_WEIGHTS = [
    [2**15, 2**14, 2**13, 2**12],
    [2**8,  2**9,  2**10, 2**11],
    [2**7,  2**6,  2**5,  2**4],
    [2**0,  2**1,  2**2,  2**3],
]


def _board_score(board_map):
    """Evaluate a board state without simulating further moves."""
    empty = count_empty_cells(board_map)

    # Sum of merged tile values (larger tiles kept together = higher score).
    merge_val = 0
    for row in board_map:
        for cell in row:
            merge_val += cell

    # Monotonicity: dot-product of tile values with snake weights.
    mono = sum(
        board_map[r][c] * _SNAKE_WEIGHTS[r][c]
        for r in range(GRID_SIZE)
        for c in range(GRID_SIZE)
    )

    return _EMPTY_WEIGHT * empty + _MERGE_WEIGHT * merge_val + _MONO_WEIGHT * mono


_ROTATIONS = {
    pygame.K_UP: 3,
    pygame.K_LEFT: 0,
    pygame.K_RIGHT: 2,
    pygame.K_DOWN: 1,
}


def _expectimax(board_map, depth, is_maximizer):
    """
    Expectimax tree search.

    Maximizer nodes: pick the best player move.
    Chance nodes: average over all possible tile spawns (2 with p=0.9, 4 with p=0.1).
    """
    if depth == 0 or not has_valid_moves(board_map):
        return _board_score(board_map)

    if is_maximizer:
        best = -1
        for rotation in _ROTATIONS.values():
            next_board, _ = rotate_and_merge(rotation, board_map)
            if next_board == board_map:
                continue
            val = _expectimax(next_board, depth - 1, False)
            if val > best:
                best = val
        # No valid move found – return static eval.
        return best if best >= 0 else _board_score(board_map)
    else:
        # Chance node: consider every empty cell with spawn probabilities.
        empty_cells = [
            (r, c)
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
            if board_map[r][c] == 0
        ]
        if not empty_cells:
            return _board_score(board_map)

        total = 0.0
        for r, c in empty_cells:
            for value, prob in ((2, 0.9), (4, 0.1)):
                child = [list(row) for row in board_map]
                child[r][c] = value
                total += prob * _expectimax(child, depth - 1, True)

        return total / len(empty_cells)


def choose_auto_move(board_map, depth=3):
    """Return the pygame key constant for the best move found by expectimax."""
    best_key = None
    best_score = -1
    for key, rotation in _ROTATIONS.items():
        next_board, _ = rotate_and_merge(rotation, board_map)
        if next_board == board_map:
            continue
        score = _expectimax(next_board, depth - 1, False)
        if score > best_score:
            best_score = score
            best_key = key

    return best_key


if __name__ == "__main__":
    import pygame

    # Board map
    board_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # pygame setup
    pygame.init()
    font = pygame.font.SysFont("Arial", TEXT_SIZE, bold=True)
    score_font = pygame.font.SysFont("Arial", SCORE_TEXT_SIZE, bold=True)
    mode_font = pygame.font.SysFont("Arial", MODE_TEXT_SIZE, bold=True)
    notify_font = pygame.font.SysFont("Arial", NOTIFY_TEXT_SIZE, bold=True)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    game_over = False
    auto_mode = False
    last_auto_move_at = 0

    spawn_tile(board_map)
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_y:
                        board_map = [
                            [0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)
                        ]
                        total_score = 0
                        spawn_tile(board_map)
                        game_over = False
                    elif event.key == pygame.K_n:
                        running = False
                    continue

                if event.key == pygame.K_q:
                    running = False
                    continue
                if event.key == pygame.K_a:
                    auto_mode = not auto_mode
                    continue
                new_board = handle_key(event.key, board_map)
                if new_board is not None:
                    if new_board != board_map:
                        board_map = new_board
                        spawn_tile(board_map)
                    game_over = not has_valid_moves(board_map)

        if auto_mode and not game_over:
            now = pygame.time.get_ticks()
            if now - last_auto_move_at >= AUTO_MOVE_DELAY_MS:
                ai_key = choose_auto_move(board_map)
                if ai_key is None:
                    game_over = True
                else:
                    new_board = handle_key(ai_key, board_map)
                    if new_board is not None and new_board != board_map:
                        board_map = new_board
                        spawn_tile(board_map)
                    game_over = not has_valid_moves(board_map)
                last_auto_move_at = now

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BG_COLOR)

        # RENDER YOUR GAME HERE
        render_board(screen, board_map, total_score, auto_mode)
        if game_over:
            draw_game_over_notice(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
