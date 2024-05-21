# call http://127.0.0.1:8000/api/python/get_randomsudoku 1000 times and test the performance of the API.

import time
import requests

start_time = time.time()
unique_puzzle_ids = set()
for i in range(100):
    response = requests.get('http://127.0.0.1:8000/api/python/sudoku/difficulty/low')
    print(response.json())
    unique_puzzle_ids.add(response.json()['puzzle_id'])
end_time = time.time()
print(f'Time taken to make 100 requests: {end_time - start_time} seconds')
print(f'Unique puzzle ids: {len(unique_puzzle_ids)}')
