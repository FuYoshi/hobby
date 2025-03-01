#!/usr/bin/python
"""
Filename: solver.py
Authors: Yoshi Fu
Project: Sudoku Solver
Date: February 2025

Summary:
TODO
"""


SQUARE_SIZE: int = 3
SUDOKU_SIZE: int = SQUARE_SIZE**2


test_sudoku: list[list[int]] = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def print_sudoku(sudoku: list[list[int]]) -> None:
    """Print a sudoku board.

    Args:
        sudoku (list[list[int]]): sudoku board.
    """
    for row in sudoku:
        print(row)
    print()


def check_row(sudoku: list[list[int]], row: int) -> bool:
    """Check if a row in a sudoku is valid.

    Args:
        sudoku (list[list[int]]): sudoku board.
        row (int): row to check.

    Returns:
        bool: True if row is valid, False otherwise.
    """
    return sorted(sudoku[row]) == list(range(1, SUDOKU_SIZE + 1))


def check_col(sudoku: list[list[int]], col: int) -> bool:
    """Check if a col in a sudoku is valid.

    Args:
        sudoku (list[list[int]]): sudoku board.
        col (int): col to check.

    Returns:
        bool: True if col is valid, False otherwise.
    """
    return sorted(sudoku[col]) == list(range(1, SUDOKU_SIZE + 1))


def check_square(sudoku: list[list[int]], row: int, col: int) -> bool:
    """Check if a square in a sudoku is valid.

    Args:
        sudoku (list[list[int]]): sudoku board.
        row (int): row of square.
        col (int): col of square.

    Returns:
        bool: True if square is valid, False otherwise.
    """
    square: list = []
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            square.append(sudoku[row + i][col + j])
    return sorted(square) == list(range(1, SUDOKU_SIZE + 1))


def check_sudoku(sudoku: list[list[int]]) -> bool:
    """Check if a sudoku is valid.

    Args:
        sudoku (list[list[int]]): sudoku board.

    Returns:
        bool: True if sudoku is valid, False otherwise.
    """
    for i in range(len(sudoku)):
        if not check_row(sudoku, i):
            return False
        if not check_col(sudoku, i):
            return False

    for i in range(0, len(sudoku), SQUARE_SIZE):
        for j in range(0, len(sudoku[0]), SQUARE_SIZE):
            if not check_square(sudoku, i, j):
                return False
    return True


def empty_cells(sudoku: list[list[int]]) -> list[tuple[int, int]]:
    """Find empty positions in a sudoku.

    Args:
        sudoku (list[list[int]]): sudoku board.

    Returns:
        list[tuple[int, int]]: list of empty positions.
    """
    return [
        (row, col)
        for row, rows in enumerate(sudoku)
        for col, cell in enumerate(rows)
        if cell == 0
    ]


def valid_in_row(sudoku: list[list[int]], row: int, num: int) -> bool:
    """Check if a number is valid in a row.

    Args:
        sudoku (list[list[int]]): sudoku board.
        row (int): row to check.
        num (int): number to check.

    Returns:
        bool: True if number is valid, False otherwise.
    """
    return num not in sudoku[row]


def valid_in_col(sudoku: list[list[int]], col: int, num: int) -> bool:
    """Check if a number is valid in a col.

    Args:
        sudoku (list[list[int]]): sudoku board.
        col (int): col to check.
        num (int): number to check.

    Returns:
        bool: True if number is valid, False otherwise.
    """
    return num not in [sudoku[row][col] for row in range(SUDOKU_SIZE)]


def valid_in_square(sudoku: list[list[int]], row: int, col: int, num: int) -> bool:
    """Check if a number is valid in a square.

    Args:
        sudoku (list[list[int]]): sudoku board.
        row (int): row of square.
        col (int): col of square.
        num (int): number to check.

    Returns:
        bool: True if number is valid, False otherwise.
    """
    for i in range(SQUARE_SIZE):
        for j in range(SQUARE_SIZE):
            if sudoku[row + i][col + j] == num:
                return False
    return True


def valid_moves(sudoku: list[list[int]], row: int, col: int) -> list[int]:
    """Find valid moves for a cell in a sudoku.

    Args:
        sudoku (list[list[int]]): sudoku board.
        row (int): row of cell.
        col (int): col of cell.

    Returns:
        list[int]: list of valid moves.
    """
    return [
        num
        for num in range(1, SUDOKU_SIZE + 1)
        if valid_in_row(sudoku, row, num)
        and valid_in_col(sudoku, col, num)
        and valid_in_square(
            sudoku, row - row % SQUARE_SIZE, col - col % SQUARE_SIZE, num
        )
    ]


def try_move(sudoku: list[list[int]], row: int, col: int, num: int) -> None:
    """Try to make a move in a sudoku.

    Args:
        sudoku (list[list[int]]): sudoku board.
        row (int): row of cell.
        col (int): col of cell.
        num (int): number to place.
    """
    if (
        valid_in_row(sudoku, row, num)
        and valid_in_col(sudoku, col, num)
        and valid_in_square(
            sudoku, row - row % SQUARE_SIZE, col - col % SQUARE_SIZE, num
        )
    ):
        sudoku[row][col] = num


def solve_sudoku(sudoku: list[list[int]]) -> bool:
    """Solve a sudoku.

    Args:
        sudoku (list[list[int]]): sudoku board.

    Returns:
        bool: True if sudoku is solved, False otherwise.
    """
    cells: list[tuple[int, int]] = empty_cells(sudoku)
    if not cells:
        return True

    row: int
    col: int
    row, col = cells[0]
    for num in valid_moves(sudoku, row, col):
        try_move(sudoku, row, col, num)
        if solve_sudoku(sudoku):
            return True
        sudoku[row][col] = 0
    return False


def main() -> None:
    """Main function."""
    print_sudoku(test_sudoku)

    print(f"Solved: {solve_sudoku(test_sudoku)}")
    print_sudoku(test_sudoku)


if __name__ == "__main__":
    main()
