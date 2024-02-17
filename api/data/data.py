import enum
import os
import json
import types


class Difficulty(enum.Enum):
    low_difficulty = 1
    medium_difficulty = 5
    high_difficulty = 8
    
class title(enum.Enum):
    first_column = 'id'
    second_column = 'puzzle'
    three_column = 'solution'
    four_column = 'clues'
    fifth_column = 'difficulty'
    

def format_data(data: list) -> dict:
    formatted_data = {}
    formatted_data[title.first_column.value] = int(data[0])
    puzzle_matrix = [list(data[1][i:i+9]) for i in range(0, 81, 9)]
    formatted_data[title.second_column.value] = puzzle_matrix
    solution_matrix = [list(data[2][i:i+9]) for i in range(0, 81, 9)]
    formatted_data[title.three_column.value] = solution_matrix
    formatted_data[title.four_column.value] = int(data[3])
    difficulty = float(data[4].replace('\n', ''))
    formatted_data[title.fifth_column.value] = difficulty
    return formatted_data


script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, 'sudoku-3m.csv')
json_file_path = os.path.join(script_dir, 'sudoku_test.json')

low_difficulty_data = []
medium_difficulty_data = []
high_difficulty_data = []

with open(csv_file_path, 'r') as f:
    next(f)  # Skip the header line
    for line in f: 
        line = line.strip()
        if not line:
            break
        data = line.split(',')
        formatted_data = format_data(data)
    
        if formatted_data['difficulty'] <= Difficulty.low_difficulty.value and len(low_difficulty_data) < 10:
            low_difficulty_data.append(formatted_data)
        elif Difficulty.low_difficulty.value < formatted_data['difficulty'] <= Difficulty.medium_difficulty.value and len(medium_difficulty_data) < 10:
            medium_difficulty_data.append(formatted_data)
        elif Difficulty.medium_difficulty.value < formatted_data['difficulty'] <= Difficulty.high_difficulty.value and len(high_difficulty_data) < 10:
            high_difficulty_data.append(formatted_data)
            print(formatted_data['difficulty'])

all_data = low_difficulty_data + medium_difficulty_data + high_difficulty_data
with open(json_file_path, 'w') as write_file:
    json.dump(all_data, write_file)



test_array = ['1', '1..5.37..6.3..8.9......98...1.......8761..........6...........7.8.9.76.47...6.312', '198543726643278591527619843914735268876192435235486179462351987381927654759864312', '27', '2.2\n']


