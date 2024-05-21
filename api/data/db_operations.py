import boto3
from boto3.dynamodb.conditions import Key
import uuid
import logging

logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SudokuPuzzles')


def get_random_sudoku() -> list:
    try:
        random_uuid = str(uuid.uuid4())
        
        last_key_evaluated = {
            'puzzle_id': random_uuid
        }

        response = table.scan(
            ExclusiveStartKey=last_key_evaluated,
            Limit=1
        )
        items = response.get('Items', [])
        
        if items:
            return items[0]
        else:
            return {"message": "No sudoku found"}
    except Exception as e:
        logger.error(f"Error in get_random_sudoku: {e}")
        raise
    
def get_sudoku(difficulty: str):
    try:
        random_uuid = str(uuid.uuid4())
        
        response = table.query(
            IndexName='difficulty-index',
            KeyConditionExpression=Key('difficulty').eq(difficulty) & Key('puzzle_id').gt(random_uuid),
            Limit=1
        )
        items = response.get('Items', [])
        
        if items:
            return items[0]
        else:
            return {"message": "No sudoku found"}
    
    except Exception as e:
        logger.error(f"Error in get_sudoku: {e}")
        raise
    
