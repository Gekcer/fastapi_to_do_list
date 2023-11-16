from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key= True)
    task_name = Column(String, nullable= False)
    description = Column(String, nullable= True)
    completed = Column(Boolean, default= False)