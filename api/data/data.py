import enum
import os
import json
import types
import time

class Difficulty(enum.Enum):
    low_difficulty = 1
    medium_difficulty = 4
    
class title(enum.Enum):
    second_column = 'puzzle'
    three_column = 'solution'
    four_column = 'clues'
    fifth_column = 'difficulty'
    

def format_data(data: list) -> dict:
    formatted_data = {}
    puzzle_matrix = [list(data[1][i:i+9]) for i in range(0, 81, 9)]
    formatted_data[title.second_column.value] = puzzle_matrix
    solution_matrix = [list(data[2][i:i+9]) for i in range(0, 81, 9)]
    formatted_data[title.three_column.value] = solution_matrix
    formatted_data[title.four_column.value] = int(data[3])
    difficulty = float(data[4].replace('\n', ''))
    if difficulty <= Difficulty.low_difficulty.value:
        difficulty_value = 'low'
    elif Difficulty.low_difficulty.value < difficulty <= Difficulty.medium_difficulty.value:
        difficulty_value = 'medium'
    else:
        difficulty_value = 'high'
    formatted_data[title.fifth_column.value] = difficulty_value
    return formatted_data


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'sudoku-3m.csv')
json_file_path = os.path.join(script_dir, 'sudoku_30k.json')

low_difficulty_data = []
medium_difficulty_data = []
high_difficulty_data = []

def process_data(format_data, csv_file_path):
    start_time = time.time()
    print('Processing data...')
    total_number_of_lines = sum(1 for line in open(csv_file_path))
    counter = 0
    with open(csv_file_path, 'r') as f:
        next(f)  # Skip the header line
        for line in f: 
            line = line.strip()
            if not line:
                break
            data = line.split(',')
            formatted_data = format_data(data)

            if formatted_data['difficulty'] =='low':
                low_difficulty_data.append(formatted_data)
            elif formatted_data['difficulty'] =='medium':
                medium_difficulty_data.append(formatted_data)
            elif formatted_data['difficulty'] == 'high':
                high_difficulty_data.append(formatted_data)
            counter += 1
            print(f'Processed {counter} of {total_number_of_lines} lines')
    end_time = time.time()
    print(f'Processing data took {end_time - start_time} seconds')
    
def process_30k_data(format_data, csv_file_path):
    start_time = time.time()
    print('Processing data...')
    total_number_of_lines = 30000
    counter = 0
    
    low_difficulty_count, medium_difficulty_count, high_difficulty_count = 0, 0, 0
    
    with open(csv_file_path, 'r') as f:
        next(f)  # Skip the header line
        for line in f: 
            line = line.strip()
            if not line:
                break
            
            data = line.split(',')
            formatted_data = format_data(data)
            
            if formatted_data['difficulty'] == 'low' and low_difficulty_count < 10000:
                low_difficulty_data.append(formatted_data)
                low_difficulty_count += 1
                counter += 1
            elif formatted_data['difficulty'] == 'medium' and medium_difficulty_count < 10000:
                medium_difficulty_data.append(formatted_data)
                medium_difficulty_count += 1
                counter += 1
            elif formatted_data['difficulty'] == 'high' and high_difficulty_count < 10000:
                high_difficulty_data.append(formatted_data)
                high_difficulty_count += 1
                counter += 1

            if low_difficulty_count >= 10000 and medium_difficulty_count >= 10000 and high_difficulty_count >= 10000:
                break
            
            print(f'Processed {counter} of {total_number_of_lines} lines')
    
    end_time = time.time()
    print(f'Processing data took {end_time - start_time} seconds')
    print(f'Low difficulty puzzles: {low_difficulty_count}')
    print(f'Medium difficulty puzzles: {medium_difficulty_count}')
    print(f'High difficulty puzzles: {high_difficulty_count}')

process_30k_data(format_data, csv_file_path)

def write_all_data_to_json(json_file_path):
    all_data = low_difficulty_data + medium_difficulty_data + high_difficulty_data
    with open(json_file_path, 'w') as write_file:
        json.dump(all_data, write_file)

write_all_data_to_json(json_file_path)


# def validate_30k_json(json_file_path):
#     with open(json_file_path, 'r') as f:
#         low_difficulty_count, medium_difficulty_count, high_difficulty_count = 0, 0, 0
#         data = json.load(f)
#         print(f'Total number of puzzles: {len(data)}')
#         for puzzle in data:
#             if puzzle['difficulty'] == 'low':
#                 low_difficulty_count += 1
#             elif puzzle['difficulty'] == 'medium':
#                 medium_difficulty_count += 1
#             else:
#                 high_difficulty_count += 1
#         print(f'Low difficulty puzzles: {low_difficulty_count}')
#         print(f'Medium difficulty puzzles: {medium_difficulty_count}')
#         print(f'High difficulty puzzles: {high_difficulty_count}')
        
# validate_30k_json(json_file_path)

