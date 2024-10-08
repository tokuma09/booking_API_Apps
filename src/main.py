from fastapi import FastAPI
from pydantic import BaseModel


class Data(BaseModel):
    x: float
    y: float


app = FastAPI()


@app.get(path="/")
def index():
    return {"message": "Hello World!"}
