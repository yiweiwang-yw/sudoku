import boto3
from boto3.dynamodb.conditions import Key
import logging
import os
import random
import uuid
from typing import Any, Dict

logger = logging.getLogger(__name__)
DIFFICULTIES = ("low", "medium", "high")


class NoSudokuFoundError(LookupError):
    pass


def _get_table():
    table_name = os.getenv("SUDOKU_TABLE_NAME", "SudokuPuzzles")
    return boto3.resource("dynamodb").Table(table_name)


def get_random_sudoku() -> Dict[str, Any]:
    return get_sudoku(random.choice(DIFFICULTIES))


def get_sudoku(difficulty: str) -> Dict[str, Any]:
    if difficulty not in DIFFICULTIES:
        raise ValueError("Difficulty must be low, medium, or high.")

    try:
        table = _get_table()
        random_uuid = str(uuid.uuid4())

        # Start at a random UUID in the sorted index and wrap to its beginning.
        response = table.query(
            IndexName="difficulty-index",
            KeyConditionExpression=Key("difficulty").eq(difficulty)
            & Key("puzzle_id").gt(random_uuid),
            Limit=1,
        )
        items = response.get("Items", [])

        if not items:
            response = table.query(
                IndexName="difficulty-index",
                KeyConditionExpression=Key("difficulty").eq(difficulty),
                Limit=1,
            )
            items = response.get("Items", [])

        if not items:
            raise NoSudokuFoundError("No sudoku found")
        return items[0]
    except NoSudokuFoundError:
        raise
    except Exception as e:
        logger.error(f"Error in get_sudoku: {e}")
        raise
