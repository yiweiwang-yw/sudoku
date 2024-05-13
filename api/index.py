from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .data.sudoku_solver import get_random_sudoku, get_sudoku

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# run myenv\Scripts\activate.bat for virtual environment on Windows

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

# get a random sudoku
@app.get("/api/python/get_randomsudoku")
async def get_random_sudoku_resolver():
    return get_random_sudoku()
# get a sudoku by difficulty
@app.get("/api/python/sudoku/difficulty/{difficulty}")
async def get_sudoku_by_difficulty(difficulty: str):
    return get_sudoku(difficulty)