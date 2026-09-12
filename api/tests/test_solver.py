import unittest

from api.data.sudoku_solver import (
    InvalidPuzzleError,
    UnsolvablePuzzleError,
    solve_next_step,
    solve_sudoku,
    validate_sudoku,
)


PUZZLE = [
    list("53..7...."),
    list("6..195..."),
    list(".98....6."),
    list("8...6...3"),
    list("4..8.3..1"),
    list("7...2...6"),
    list(".6....28."),
    list("...419..5"),
    list("....8..79"),
]

SOLUTION = [
    list("534678912"),
    list("672195348"),
    list("198342567"),
    list("859761423"),
    list("426853791"),
    list("713924856"),
    list("961537284"),
    list("287419635"),
    list("345286179"),
]


class SudokuSolverTests(unittest.TestCase):
    def test_solves_puzzle_without_mutating_givens(self):
        original = [row.copy() for row in PUZZLE]

        result = solve_sudoku(PUZZLE)

        self.assertEqual(SOLUTION, result)
        self.assertEqual(original, PUZZLE)
        self.assertTrue(validate_sudoku(result))

    def test_completed_puzzle_is_returned_unchanged(self):
        self.assertEqual(SOLUTION, solve_sudoku(SOLUTION))

    def test_rejects_wrong_dimensions_values_and_conflicts(self):
        invalid_puzzles = [
            PUZZLE[:-1],
            [row[:-1] for row in PUZZLE],
            [[*row] for row in PUZZLE],
            [[*row] for row in PUZZLE],
        ]
        invalid_puzzles[2][0][2] = "0"
        invalid_puzzles[3][0][2] = "5"

        for puzzle in invalid_puzzles:
            with self.subTest(puzzle=puzzle):
                with self.assertRaises(InvalidPuzzleError):
                    solve_sudoku(puzzle)

    def test_rejects_valid_but_unsatisfiable_puzzle(self):
        unsatisfiable = [row.copy() for row in PUZZLE]
        unsatisfiable[0][2] = "1"

        with self.assertRaises(UnsolvablePuzzleError):
            solve_sudoku(unsatisfiable)

    def test_next_step_adds_one_solution_value(self):
        result = solve_next_step(PUZZLE)

        original_filled = sum(cell != "." for row in PUZZLE for cell in row)
        result_filled = sum(cell != "." for row in result for cell in row)
        self.assertEqual(original_filled + 1, result_filled)
        self.assertEqual("4", result[0][2])


if __name__ == "__main__":
    unittest.main()
