from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic import BaseModel
from typing import List
from .data.db_operations import DIFFICULTIES, get_random_sudoku, get_sudoku
from .data.sudoku_solver import (
    InvalidPuzzleError,
    UnsolvablePuzzleError,
    solve_next_step,
    solve_sudoku,
)


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
        if "message" in result:
            raise HTTPException(status_code=404, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching random sudoku: {e}")
        raise HTTPException(
            status_code=503,
            detail="Puzzle storage is unavailable. Check the DynamoDB configuration.",
        )
# get a sudoku by difficulty


@app.get("/api/python/sudoku/difficulty/{difficulty}")
async def get_sudoku_by_difficulty_resolver(difficulty: str):
    if difficulty not in DIFFICULTIES:
        raise HTTPException(status_code=400, detail="Difficulty must be low, medium, or high.")
    try:
        result = get_sudoku(difficulty)
        if "message" in result:
            raise HTTPException(status_code=404, detail=result["message"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error fetching sudoku with difficulty {difficulty}: {e}")
        raise HTTPException(
            status_code=503,
            detail="Puzzle storage is unavailable. Check the DynamoDB configuration.",
        )


def solve_or_raise(puzzle: List[List[str]], next_step: bool = False):
    try:
        return solve_next_step(puzzle) if next_step else solve_sudoku(puzzle)
    except InvalidPuzzleError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except UnsolvablePuzzleError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@app.post("/api/python/solve_next_step")
async def solve_next_step_resolver(puzzle_request: PuzzleRequest):
    return {"puzzle": solve_or_raise(puzzle_request.puzzle, next_step=True)}


@app.post("/api/python/solve")
async def solve_resolver(puzzle_request: PuzzleRequest):
    return {"puzzle": solve_or_raise(puzzle_request.puzzle)}
