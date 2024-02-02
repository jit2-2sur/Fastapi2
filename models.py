"""
this file is for creating all the data models used in this task
"""

from sqlalchemy import Column, Integer, String, JSON, ARRAY, ForeignKey

from database import Base, engine


# this function is called to create all the database tables
def create_tables():
    Base.metadata.create_all(engine)


# datamodel to create users table in database
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


# datamodel to create quizzes table in database. it stores all quiz information along with all questions and their options
class Quiz(Base):
    __tablename__ = "quizzes"
    quiz_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    time_duration = Column(Integer)
    questions = Column(ARRAY(JSON))


# datamodel to create answers table in database. it stores all submitted answers by user
class Answer(Base):
    __tablename__ = "answers"
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.quiz_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    answers_list = Column(ARRAY(String))
