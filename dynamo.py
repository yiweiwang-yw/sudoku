import boto3
import json
import os
import uuid


def create_sudoku_table():
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    # Define the table schema
    table = dynamodb.create_table(
        TableName='SudokuPuzzles',
        KeySchema=[
            {
                'AttributeName': 'puzzle_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'puzzle_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'difficulty',
                'AttributeType': 'S'
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'difficulty-index',
                'KeySchema': [
                    {
                        'AttributeName': 'difficulty',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'puzzle_id',
                        'KeyType': 'RANGE'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(
        TableName='SudokuPuzzles')

    print("Table created successfully.")




def load_data_into_dynamodb(table):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, 'api', 'data', 'sudoku_full.json')
    with open(json_file_path, 'r') as f:
        print('Loading data...')
        sudoku_data = json.load(f)
        # store first 10 sudoku puzzles in DynamoDB
        print('Storing data...')
        for i in range(10):
            item = sudoku_data[i]
            item['puzzle_id'] = str(uuid.uuid4())
            table.put_item(Item=item)
        print('Data loaded successfully!')



if __name__ == '__main__':
    # create_sudoku_table()
    table = boto3.resource('dynamodb').Table('SudokuPuzzles')
    load_data_into_dynamodb(table)
    response = table.scan()
    print(response['Items'])
