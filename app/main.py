from fastapi import FastAPI

from .database import Base, engine, SessionLocal

app = FastAPI()

@app.get('users')
def read_users():


    return {"message": "List of users"}

