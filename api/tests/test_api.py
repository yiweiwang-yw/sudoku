import unittest

from fastapi import HTTPException

from api.index import solve_or_raise

from api.tests.test_solver import PUZZLE


class SudokuApiTests(unittest.TestCase):
    def test_maps_invalid_puzzle_to_422(self):
        conflicting = [row.copy() for row in PUZZLE]
        conflicting[0][2] = "5"

        with self.assertRaises(HTTPException) as raised:
            solve_or_raise(conflicting)

        self.assertEqual(422, raised.exception.status_code)
        self.assertEqual("Puzzle contains conflicting values.", raised.exception.detail)

    def test_maps_unsatisfiable_puzzle_to_409(self):
        unsatisfiable = [row.copy() for row in PUZZLE]
        unsatisfiable[0][2] = "1"

        with self.assertRaises(HTTPException) as raised:
            solve_or_raise(unsatisfiable)

        self.assertEqual(409, raised.exception.status_code)
        self.assertEqual("Puzzle has no solution.", raised.exception.detail)


if __name__ == "__main__":
    unittest.main()
