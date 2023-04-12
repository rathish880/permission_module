from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import FileResponse
from generate_pdf import render_pdf
import os


class History(BaseModel):
    lx: object


app = FastAPI()
origins = ["http://localhost:3000", "http://192.168.43.29:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.put("/generate_pdf")
def generate_pdf(history: History):
    print(history.lx)
    fileName = render_pdf()
    file_path = os.path.abspath(fileName)
    return FileResponse(path=file_path, filename=fileName)
