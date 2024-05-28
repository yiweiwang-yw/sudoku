import json
import os
import random
from typing import List

script_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(script_dir, 'sudoku_test.json')


def load_data():
    with open(json_file_path, 'r') as file:
        return json.load(file)


data = load_data()


def validate_sudoku(puzzle: list) -> bool:
    def check_array_valid(arr: list) -> bool:
        arr = [i for i in arr if i != '.']
        return len(arr) == len(set(arr))

    for row in puzzle:
        if not check_array_valid(row):
            return False

    for col in range(9):
        if not check_array_valid([row[col] for row in puzzle]):
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not check_array_valid([puzzle[x][y] for x in range(i, i+3) for y in range(j, j+3)]):
                return False
    return True


def is_valid(arr: List[List[str]], row: int, col: int, num: str) -> bool:
       for x in range(9):
            if arr[row][x] == num or arr[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if arr[i + start_row][j + start_col] == num:
                    return False
        return True


def solve_sudoku(puzzle: list) -> list:

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


def get_random_sudoku() -> list:
    return random.choice(data)


def solve_next_step(puzzle: List[List[str]]) -> List[List[str]]:
    # Return first solution step
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == '.':
                for num in range(1, 10):
                    if is_valid(puzzle, row, col, str(num)):
                        puzzle[row][col] = str(num)
                        return puzzle
    return puzzle


testpuzzle = [['9', '3', '1', '2', '8', '6', '.', '7', '5'], ['2', '5', '6', '9', '3', '7', '1', '.', '4'], ['4', '7', '.', '5', '.', '1', '3', '8', '2'], ['1', '4', '5', '3', '2', '8', '6', '9', '.'], ['3', '6', '7', '.', '1', '9', '4', '2', '8'], ['8', '9', '2', '.', '5', '4', '7', '1', '3'], ['6', '2', '8', '1', '4', '3', '5', '.', '7'], ['5', '.', '9', '7', '.', '2', '8', '6', '1'], ['7', '1', '3', '6', '9', '5', '2', '4', '.']]

if __name__ == '__main__':
    # Code for testing or direct execution
    data = load_data()  # Ensure data is loaded for script execution
    for sudoku in data:
        puzzle = sudoku['puzzle']
        print(puzzle)
        non_empty_cell_count = sum([1 for row in puzzle for cell in row if cell != '.'])
        # print(validate_sudoku(puzzle))
        # solution = sudoku['solution']
        # print(validate_sudoku(solution))
        # print("solving...")
        # solved_puzzle = solve_sudoku(puzzle)
        # print(solved_puzzle == solution)
        solve_next_step(puzzle)
        non_empty_cell_count_after = sum([1 for row in puzzle for cell in row if cell != '.'])
        print(non_empty_cell_count, non_empty_cell_count_after)
