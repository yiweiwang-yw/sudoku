from fastapi import FastAPI

app = FastAPI()

# run myenv\Scripts\activate.bat for virtual environment on Windows

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}