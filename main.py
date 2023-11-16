from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from db_todo import get_engine
from models import Base, Task

app = FastAPI()

engine = get_engine()
SessionLocal = sessionmaker(bind= engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""
Table:
id: int
task_name: str
description: str
completed: bool
"""
@app.get("/")
def root_welcome():
    return {"message": "Welcome to app"}

@app.get("/to_do_list")
def get_to_do_list(db: SessionLocal = Depends(get_db)):
    return db.query(Task).all()

@app.get("/to_do_list/{id}")
def get_exact_task(id: int, db: SessionLocal = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task == None:
        return JSONResponse(status_code= 404, content= {"message": "No such task id"})
    return task


@app.post("/to_do_list")
def create_task(name: str, description: str , db: SessionLocal = Depends(get_db)):
    task = Task(task_name = name, 
                description = description)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.put("/to_do_list/{id}")
def toggle_complete(id: int, db: SessionLocal = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task == None:
        return JSONResponse(status_code= 404, content= {"message": "No such task id"})
    task.completed = not task.completed
    db.commit()
    db.refresh(task)
    return task


@app.delete("/to_do_list/{id}")
def delete_task(id: int, db: SessionLocal = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task == None:
        return JSONResponse(status_code= 404, content= {"message": "No such task id"})
    db.delete(task)
    db.commit()
    return task
