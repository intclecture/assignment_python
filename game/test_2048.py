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


from game2048 import merge_row, rotate_and_merge


def test_merge_row():
    new_row = merge_row([2, 2, 4, 0, 0])
    assert len(new_row) == 5
    assert new_row == [4, 4, 0, 0, 0]

    new_row = merge_row([0, 0, 0, 0, 4])
    assert len(new_row) == 5
    assert new_row == [4, 0, 0, 0, 0]

    new_row = merge_row([0, 4, 0, 0, 0])
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
    result = rotate_and_merge(0, board)
    assert result == [
        [4, 4, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # Down
    result = rotate_and_merge(1, board)
    assert result == [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0],
        [2, 4, 4, 0, 4],
    ]

    # Right
    result = rotate_and_merge(2, board)
    assert result == [
        [0, 0, 0, 4, 4],
        [0, 0, 0, 0, 4],
        [0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]

    # Up
    result = rotate_and_merge(3, board)
    assert result == [
        [2, 2, 4, 0, 4],
        [0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
