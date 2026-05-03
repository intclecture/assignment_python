def test_zip():
    m = zip([1, 2, 3], [4, 5, 6], [7, 8, 9])

    assert next(m) == (1, 4, 7)
    assert next(m) == (2, 5, 8)
    assert next(m) == (3, 6, 9)


def test_zip_2d():
    dim2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m = zip(*dim2d)

    assert next(m) == (1, 4, 7)
    assert next(m) == (2, 5, 8)
    assert next(m) == (3, 6, 9)


from game2048 import rotate


def test_cw90():
    dim2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m = zip(*dim2d[::-1])

    assert next(m) == (7, 4, 1)
    assert next(m) == (8, 5, 2)
    assert next(m) == (9, 6, 3)

    m = [list(r) for r in zip(*dim2d[::-1])]
    assert m[0] == [7, 4, 1]
    assert m[1] == [8, 5, 2]
    assert m[2] == [9, 6, 3]

    m = rotate(True, dim2d)
    assert m[0] == [7, 4, 1]
    assert m[1] == [8, 5, 2]
    assert m[2] == [9, 6, 3]


def test_ccw90():
    dim2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    m = [list(r) for r in zip(*dim2d)][::-1]

    assert m[0] == [3, 6, 9]
    assert m[1] == [2, 5, 8]
    assert m[2] == [1, 4, 7]

    m = rotate(False, dim2d)
    assert m[0] == [3, 6, 9]
    assert m[1] == [2, 5, 8]
    assert m[2] == [1, 4, 7]


from game2048 import choose_auto_move, has_valid_moves, merge_row, rotate_and_merge


def test_merge_row():
    new_row, _ = merge_row([2, 2, 4, 0, 0])
    assert len(new_row) == 5
    assert new_row == [4, 4, 0, 0, 0]

    new_row, _ = merge_row([0, 0, 0, 0, 4])
    assert len(new_row) == 5
    assert new_row == [4, 0, 0, 0, 0]

    new_row, _ = merge_row([0, 4, 0, 0, 0])
    assert len(new_row) == 5
    assert new_row == [4, 0, 0, 0, 0]


def test_rotate_and_merge():
    board = [
        [2, 2, 4, 0, 0],
        [0, 0, 0, 0, 4],
        [0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # Left
    result, _ = rotate_and_merge(0, board)
    assert result == [
        [4, 4, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # Down
    result, _ = rotate_and_merge(1, board)
    assert result == [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [2, 4, 4, 0, 4],
    ]

    # Right
    result, _ = rotate_and_merge(2, board)
    assert result == [
        [0, 0, 0, 4, 4],
        [0, 0, 0, 0, 4],
        [0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # Up
    result, _ = rotate_and_merge(3, board)
    assert result == [
        [2, 2, 4, 0, 4],
        [0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]


def test_has_valid_moves_when_empty_cell_exists():
    # Not game over: at least one empty tile exists, so a new move can always be made.
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 0, 2],
        [4, 8, 16, 32],
    ]

    assert has_valid_moves(board) is True


def test_has_valid_moves_when_merge_exists():
    # Not game over: no empty tiles, but the last row has adjacent equal values (32, 32)
    # so a merge is possible.
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2, 4],
        [8, 16, 32, 32],
    ]

    assert has_valid_moves(board) is True


def test_has_valid_moves_when_no_moves_left():
    # Game over: board is full and there are no adjacent equal tiles horizontally
    # or vertically, so no move can change the board.
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2, 4],
        [8, 16, 32, 64],
    ]

    assert has_valid_moves(board) is False


def test_choose_auto_move_returns_none_when_no_moves_left():
    # Expectimax search should detect there are no valid moves and return None.
    board = [
        [2, 4, 8, 16],
        [32, 64, 128, 256],
        [512, 1024, 2, 4],
        [8, 16, 32, 64],
    ]

    assert choose_auto_move(board) is None


def test_choose_auto_move_returns_direction_when_move_available():
    # At least one slide direction is valid; expectimax must pick one.
    board = [
        [2, 2, 4, 8],
        [16, 32, 64, 128],
        [256, 512, 1024, 2],
        [4, 8, 16, 32],
    ]

    assert choose_auto_move(board) is not None


def test_choose_auto_move_prefers_high_scoring_move():
    import pygame
    # Left slide merges [2,2] -> [4] and creates the most empty cells,
    # so expectimax should prefer K_LEFT over any other direction.
    board = [
        [2, 2, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    assert choose_auto_move(board, depth=2) == pygame.K_LEFT
