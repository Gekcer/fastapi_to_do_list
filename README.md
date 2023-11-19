## To-Do-List Using FastAPI, SQLAlchemy, PostgreSQL
# Step 1: Creating Database and defining API interface
# Database 
Database created using PostgreSQL, pgAdmin 4 and SQLAlchemy. 
Table Task consists of 
- id: int - primary key of the table
- task_name: str - name of task
- description: str - task description, is nullable
- completed: bool - status, that says whether the task is completed
  
To create the table Task, I used declarative_base() class from sqlalchemy, that allows to use the database table as Python Object:

```
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key= True)
    task_name = Column(String, nullable= False)
    description = Column(String, nullable= True)
    completed = Column(Boolean, default= False)
```

db_tood.py file imports database parameters and has a function that creates the engine for database. Engine allows SQLAlchemy to connect database, execute queries and get the results.
```
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

def get_engine():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

```
I use dotenv library to get parameters of database from config.py file. config.py and .env files are not in the reposiroty:
```
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
```
# main.py
main.py creates FastAPI() app, engine and the session. The session is created using sessionmaker from sqlalchemy.orm.
Sessions are used to implement transactions. These transactions consist of one or more operations, for example CRUD operations.

# Depends
Depends are such functions which have to be implemented before the main function. For example:
```
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/to_do_list/{id}")
def get_exact_task(id: int, db: SessionLocal = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    if task == None:
        return JSONResponse(status_code= 404, content= {"message": "No such task id"})
    return task
```
get_exact_task(id, db) returns task with id argument. But before it returns the task, the program has to implement get_db() function to create the session. While the session is active, we can make SQL querys to database.

# Step 2: Adding autorization
