from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .data.db_operations import get_random_sudoku, get_sudoku

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
async def get_sudoku_by_difficulty(difficulty: str):
    try:
        result = get_sudoku(difficulty)
        return result
    except Exception as e:
        logger.error(f"Error fetching sudoku with difficulty {difficulty}: {e}")
        return {"error": str(e)}