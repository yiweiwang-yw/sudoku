import boto3
from boto3.dynamodb.conditions import Key
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SudokuPuzzles')


def get_random_sudoku() -> list:
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
    
def get_sudoku(difficulty: str):
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

if __name__ == '__main__':
    for i in range(10):
        print(get_random_sudoku())
        print(get_sudoku('low'))
        print(get_sudoku('medium'))
        print(get_sudoku('high'))
    
    
