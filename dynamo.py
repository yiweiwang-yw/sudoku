import boto3
import json
import os
import uuid
import time


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
                    'WriteCapacityUnits': 25
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 25
        }
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(
        TableName='SudokuPuzzles')

    print("Table created successfully.")




def load_data_into_dynamodb(table,json_file_path):
    with open(json_file_path, 'r') as f:
        load_document_start_time = time.time()
        print('Loading data...')
        sudoku_data = json.load(f)
        load_document_end_time = time.time()
        print(f'Time taken to load document: {load_document_end_time - load_document_start_time} seconds')
        # store first 10 sudoku puzzles in DynamoDB
        print('Storing data...')
        number_of_puzzles = len(sudoku_data)
        count = 0
        start_time = time.time()
        with table.batch_writer() as batch:
            for i in range(number_of_puzzles):
                item = sudoku_data[i]
                item['puzzle_id'] = str(uuid.uuid4())
                batch.put_item(Item=item)
                count += 1
                print(f'Loaded {count}/{number_of_puzzles} puzzles')
        print('Data loaded successfully!')
        end_time = time.time()
        print(f'Time taken to load data: {end_time - start_time} seconds')
        print(f'average time per puzzle: {(end_time - start_time) / number_of_puzzles} seconds')
        
def count_items_in_table(table):
    response = table.scan()
    items = response['Items']
    count = 0
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    count = len(items)
    return count

if __name__ == '__main__':
    # create_sudoku_table()
    table = boto3.resource('dynamodb').Table('SudokuPuzzles')
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # json_file_path = os.path.join(current_dir, 'api', 'data', 'sudoku_30k.json')
    # load_data_into_dynamodb(table, json_file_path)
    # table.delete()
    print(count_items_in_table(table))
    
