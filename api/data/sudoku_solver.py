from typing import List


Board = List[List[str]]
SIZE = 9
ALLOWED_VALUES = {str(number) for number in range(1, 10)} | {"."}


class InvalidPuzzleError(ValueError):
    pass


class UnsolvablePuzzleError(ValueError):
    pass


def validate_sudoku(puzzle: Board) -> bool:
    if (
        not isinstance(puzzle, list)
        or len(puzzle) != SIZE
        or any(not isinstance(row, list) or len(row) != SIZE for row in puzzle)
        or any(cell not in ALLOWED_VALUES for row in puzzle for cell in row)
    ):
        return False

    def has_duplicates(values: List[str]) -> bool:
        filled_values = [value for value in values if value != "."]
        return len(filled_values) != len(set(filled_values))

    if any(has_duplicates(row) for row in puzzle):
        return False

    if any(has_duplicates([puzzle[row][col] for row in range(SIZE)]) for col in range(SIZE)):
        return False

    return not any(
        has_duplicates(
            [
                puzzle[row][col]
                for row in range(block_row, block_row + 3)
                for col in range(block_col, block_col + 3)
            ]
        )
        for block_row in range(0, SIZE, 3)
        for block_col in range(0, SIZE, 3)
    )


def _validate_puzzle(puzzle: Board) -> None:
    if not isinstance(puzzle, list) or len(puzzle) != SIZE:
        raise InvalidPuzzleError("Puzzle must contain exactly 9 rows.")
    if any(not isinstance(row, list) or len(row) != SIZE for row in puzzle):
        raise InvalidPuzzleError("Each puzzle row must contain exactly 9 cells.")
    if any(cell not in ALLOWED_VALUES for row in puzzle for cell in row):
        raise InvalidPuzzleError("Cells must contain '.' or a digit from 1 to 9.")
    if not validate_sudoku(puzzle):
        raise InvalidPuzzleError("Puzzle contains conflicting values.")


def is_valid(board: Board, row: int, col: int, value: str) -> bool:
    if value in board[row] or any(board[index][col] == value for index in range(SIZE)):
        return False

    block_row, block_col = 3 * (row // 3), 3 * (col // 3)
    return all(
        board[current_row][current_col] != value
        for current_row in range(block_row, block_row + 3)
        for current_col in range(block_col, block_col + 3)
    )


def _find_next_cell(board: Board):
    best_cell = None
    best_candidates = None

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] != ".":
                continue
            candidates = [
                str(number)
                for number in range(1, 10)
                if is_valid(board, row, col, str(number))
            ]
            if not candidates:
                return row, col, []
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_cell = (row, col)
                best_candidates = candidates

    if best_cell is None:
        return None
    return best_cell[0], best_cell[1], best_candidates


def _solve(board: Board) -> bool:
    next_cell = _find_next_cell(board)
    if next_cell is None:
        return True

    row, col, candidates = next_cell
    for value in candidates:
        board[row][col] = value
        if _solve(board):
            return True
        board[row][col] = "."
    return False


def solve_sudoku(puzzle: Board) -> Board:
    _validate_puzzle(puzzle)
    solution = [row.copy() for row in puzzle]
    if not _solve(solution):
        raise UnsolvablePuzzleError("Puzzle has no solution.")
    return solution


def solve_next_step(puzzle: Board) -> Board:
    solution = solve_sudoku(puzzle)
    result = [row.copy() for row in puzzle]
    for row in range(SIZE):
        for col in range(SIZE):
            if result[row][col] == ".":
                result[row][col] = solution[row][col]
                return result
    return result
