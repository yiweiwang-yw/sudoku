import boto3
from boto3.dynamodb.conditions import Key
import logging
import os
import random
import uuid

logger = logging.getLogger(__name__)

def _get_table():
    table_name = os.getenv("SUDOKU_TABLE_NAME", "SudokuPuzzles")
    return boto3.resource("dynamodb").Table(table_name)


def get_random_sudoku() -> list:
    return get_sudoku(random.choice(["low", "medium", "high"]))
    
def get_sudoku(difficulty: str):
    try:
        table = _get_table()
        random_uuid = str(uuid.uuid4())
        
        response = table.query(
            IndexName='difficulty-index',
            KeyConditionExpression=Key('difficulty').eq(difficulty) & Key('puzzle_id').gt(random_uuid),
            Limit=1
        )
        items = response.get('Items', [])

        if not items:
            response = table.query(
                IndexName='difficulty-index',
                KeyConditionExpression=Key('difficulty').eq(difficulty),
                Limit=1
            )
            items = response.get('Items', [])

        return items[0] if items else {"message": "No sudoku found"}
    
    except Exception as e:
        logger.error(f"Error in get_sudoku: {e}")
        raise
    
