import unittest
from unittest.mock import Mock, patch

from api.data import db_operations


class DynamoDbOperationsTests(unittest.TestCase):
    @patch("api.data.db_operations._get_table")
    def test_difficulty_query_wraps_when_random_range_is_empty(self, get_table):
        table = Mock()
        table.query.side_effect = [
            {"Items": []},
            {"Items": [{"puzzle_id": "first"}]},
        ]
        get_table.return_value = table

        self.assertEqual(
            {"puzzle_id": "first"}, db_operations.get_sudoku("medium")
        )
        self.assertEqual(2, table.query.call_count)

    @patch("api.data.db_operations.get_sudoku")
    @patch("api.data.db_operations.random.choice", return_value="low")
    def test_random_puzzle_uses_a_supported_difficulty(self, choice, get_sudoku):
        get_sudoku.return_value = {"puzzle_id": "puzzle"}

        result = db_operations.get_random_sudoku()

        choice.assert_called_once_with(db_operations.DIFFICULTIES)
        get_sudoku.assert_called_once_with("low")
        self.assertEqual({"puzzle_id": "puzzle"}, result)


if __name__ == "__main__":
    unittest.main()
