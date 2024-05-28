from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from typing import List
from .data.db_operations import get_random_sudoku, get_sudoku
from .data.sudoku_solver import solve_next_step


class PuzzleRequest(BaseModel):
    puzzle: List[List[str]]


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        result = get_random_sudoku()
        return result
    except Exception as e:
        logger.error(f"Error fetching random sudoku: {e}")
        return {"error": str(e)}
# get a sudoku by difficulty


@app.get("/api/python/sudoku/difficulty/{difficulty}")
async def get_sudoku_by_difficulty_resolver(difficulty: str):
    try:
        result = get_sudoku(difficulty)
        return result
    except Exception as e:
        logger.error(
            f"Error fetching sudoku with difficulty {difficulty}: {e}")
        return {"error": str(e)}


@app.post("/api/python/solve_next_step")
async def solve_next_step_resolver(puzzle_request: PuzzleRequest):
    try:
        print("Received puzzle_request:", puzzle_request)
        puzzle = puzzle_request.puzzle
        print("Puzzle:", puzzle)
        result = solve_next_step(puzzle)
        return {"puzzle": result}
    except Exception as e:
        logger.error(f"Error solving next step: {e}")
        raise HTTPException(status_code=500, detail=str(e))
