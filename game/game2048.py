import pygame
import random

# Definitions
WIDTH = 800
HEIGHT = 800
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE
TILE_MARGIN = 3
TEXT_SIZE = 60

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
        row * TILE_SIZE + TILE_MARGIN,
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


# Board render
def render_board(screen, board_map):
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
    print(f"Total score: {total_score}")
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


if __name__ == "__main__":
    import pygame

    # Board map
    board_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # pygame setup
    pygame.init()
    font = pygame.font.SysFont("Arial", TEXT_SIZE, bold=True)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    spawn_tile(board_map)
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                new_board = handle_key(event.key, board_map)
                if new_board is not None:
                    board_map = new_board
                    spawn_tile(board_map)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(BG_COLOR)

        # RENDER YOUR GAME HERE
        render_board(screen, board_map)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
