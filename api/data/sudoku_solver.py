import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'sudoku_test.json')

with open(json_file_path, 'r') as file:
    data = json.load(file)
    
def validate_sudoku(puzzle: list) -> bool:
    def is_valid(arr: list) -> bool:
        arr = [i for i in arr if i != '.']
        return len(arr) == len(set(arr))
    
    for row in puzzle:
        if not is_valid(row):
            return False
        
    for col in range(9):
        if not is_valid([row[col] for row in puzzle]):
            return False
        
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not is_valid([puzzle[x][y] for x in range(i, i+3) for y in range(j, j+3)]):
                return False
    return True
for sudoku in data:
    puzzle = sudoku['puzzle']
    print(validate_sudoku(puzzle))
    solution = sudoku['solution']
    print(validate_sudoku(solution))
    