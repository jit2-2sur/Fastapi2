from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from database import Session_local
from models import *


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


# Creates and yields a database session, ensuring it closes even if errors occur.
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
"""
class OptionModel(BaseModel):
    option_no: int
    option_desc: str

class QuestionModel(BaseModel):
    question_no: int
    question_desc: str
    marks: int
    options: List[OptionModel]
    correct_option_no: int

class QuizModel(BaseModel):
    title: str
    time_duration: int
    questions: List[QuestionModel]
"""


# Defines a data model to represent answers for a quiz, including quiz ID, user ID, and a list of answers. Used for data representation and data validation
class AnswerModel(OurBaseModel):
    quiz_id: int
    user_id: int
    answers_list: List[str]


# root has no content
@app.get("/")
async def root():
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


# get_quizzes returns all quizzes list with their questions, options and all other details
@app.get("/quizzes", status_code=status.HTTP_200_OK)
async def get_quiz(db: Session = Depends(get_db)):
    quiz = db.query(Quiz).all()
    # handles situation when there is no quiz in database
    if quiz == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no quiz",
        )
    return quiz


# retrieves specific quizzes by quiz_id
@app.get("/quizzes/{quiz_id}", status_code=status.HTTP_200_OK)
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    # handles situation when there is no quiz with given quiz_id in database
    if quiz == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no quiz",
        )
    return quiz


# submits/adds data to database
@app.post("/submit", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_answer(answer: AnswerModel, db: Session = Depends(get_db)):
    try:
        # Validating data
        if not answer.answers_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Answers list cannot be empty",
            )

        # Ensuring data types are correct
        if not isinstance(answer.quiz_id, int) or not isinstance(answer.user_id, int):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid data types for quiz_id or user_id",
            )

        new_answer = Answer(
            quiz_id=answer.quiz_id,
            user_id=answer.user_id,
            answers_list=answer.answers_list,
        )
        db.add(new_answer)  # adding answer to database
        db.commit()

        response_data = {
            "message": "Answer added successfully",
            "answer": answer.model_dump(),
        }
        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)

    # to handle cases when data don't get added to database
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error adding answer to the database"
        )


# retriving results for all users along with their correct answers for specific quiz
@app.get("/result/{quiz_id}", status_code=status.HTTP_200_OK)
async def get_result(quiz_id: int, db: Session = Depends(get_db)):
    scorecard = []
    # getting answers of all users for that specific quiz
    answers = db.query(Answer).filter(Answer.quiz_id == quiz_id).all()
    # getting that specific quiz details
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    # getting all questions of that specific quiz
    questions = quiz.questions

    # getting and storing all correct answers and marks for each question in lists
    correct_answers = []
    marks = []
    for i in range(len(questions)):
        question = questions[i]
        correct_answers.append(
            question["correct_answer"]
        )  # getting correct answer for that question
        marks.append(question["marks"])  # getting max marks for that question

    # geetting answers of each user
    for answer in answers:
        # converting users answer detail to dictionary to easily work with
        answer_dict = {
            key: value
            for key, value in answer.__dict__.items()
            if not key.startswith("_") and not callable(value)
        }
        # collecting user_id and answers of that user
        user_id = answer_dict["user_id"]
        ans_list = answer_dict["answers_list"]

        # calculating score for that user
        score = 0
        users_correct_answers = []
        j = 0
        # checking correctness of each answer, if correct then scores updating and correct answer list updation
        for j in range(len(ans_list)):
            if correct_answers[j] == ans_list[j]:
                score += marks[j]
                users_correct_answers.append(
                    {"question no": j + 1, "answer": ans_list[j]}
                )
        # storing all users score and correct answers in one variable
        scorecard.append(
            {
                "user_id": user_id,
                "score": score,
                "correct_answers": users_correct_answers,
            }
        )
    # returning each user given that quiz, along with their scores and list of correct answers
    return scorecard


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
