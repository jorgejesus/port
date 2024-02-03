from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    file_path = "results_research.txt"
    # Clean up or restart an empty file
    with open(file_path, 'w') as file:  
        pass 
    yield


app = FastAPI(lifespan=lifespan)


# CORS support otherwise port is blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Endpoint 1: Accept a POST with a JSON payload and append it to a file
@app.post("/append/")
async def append_to_file(payload: dict):
    file_path = "results_research.txt"
    try:
        with open(file_path, "a") as file:
            file.write(str(payload) + "\n")  # Convert the dict to string and append a newline for readability
        return {"message": "Payload appended successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Endpoint 2: Return the results_research.txt file for GET requests
@app.get("/results/")
async def get_results():
    file_path = "results_research.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)