from sqlalchemy import Column, Integer, String, Boolean, JSON, ARRAY, DateTime, ForeignKey, UniqueConstraint
from pydantic import BaseModel
from typing import List

from database import Base, engine

def create_tables():
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    time_duration = Column(Integer)
    questions = Column(ARRAY(JSON))

class Answer(Base):
    __tablename__ = "answers"
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    answers_list = Column(ARRAY(String))
