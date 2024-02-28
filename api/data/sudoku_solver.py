import json
import os
import random
from data import Difficulty

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

def solve_sudoku(puzzle: list) -> list:
    def is_valid(arr: list, row: int, col: int, num: int) -> bool:
        for x in range(9):
            if arr[row][x] == num or arr[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if arr[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(arr: list) -> bool:
        for row in range(9):
            for col in range(9):
                if arr[row][col] == '.':
                    for num in range(1, 10):
                        if is_valid(arr, row, col, str(num)):
                            arr[row][col] = str(num)
                            if solve(arr):
                                return True
                            arr[row][col] = '.'
                    return False
        return True

    solve(puzzle)
    return puzzle


def get_sudoku(difficulty: str) -> list:
    selected_sudoku = [sudoku for sudoku in data if sudoku['difficulty'] == difficulty]
    return random.choice(selected_sudoku) if selected_sudoku else None
    

# for sudoku in data:
#     puzzle = sudoku['puzzle']
#     print(validate_sudoku(puzzle))
#     solution = sudoku['solution']
#     print(validate_sudoku(solution))
#     print("solving...")
#     solved_puzzle = solve_sudoku(puzzle)
#     print(solved_puzzle == solution)

print(get_sudoku('low'))
