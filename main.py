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
    
def get_db():
    db= Session_local()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
'''
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
'''
class AnswerModel(OurBaseModel):
    quiz_id: int
    user_id: int
    answers_list: List[str]

class ScorecardModel(OurBaseModel):
    user_id: int
    quiz_id: int
    answer_id: int
    score: int    

def calculate_score(answers_id):
    return 0

@app.get("/quizzes", status_code=status.HTTP_200_OK)
async def get_quiz(db: Session = Depends(get_db)):
    quiz = db.query(Quiz).all() 
    return quiz

@app.get("/quizzes/{quiz_id}", status_code=status.HTTP_200_OK)
async def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    return quiz

@app.post("/submit", response_model=dict, status_code= status.HTTP_201_CREATED)
async def create_answer(answer: AnswerModel, db: Session = Depends(get_db)):
    try:
        new_answer = Answer(quiz_id=answer.quiz_id, user_id=answer.user_id, answers_list=answer.answers_list)
        db.add(new_answer)
        db.commit()

        response_data = {"message": "Answer added successfully", "answer": answer.model_dump()}
        return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error adding answer to the database")


@app.get("/result/{quiz_id}", status_code=status.HTTP_200_OK)
async def get_result(quiz_id: int, db: Session = Depends(get_db)):
    scorecard = []
    answers = db.query(Answer).filter(Answer.quiz_id == quiz_id).all()
    quiz = db.query(Quiz).filter(Quiz.quiz_id == quiz_id).first()
    questions = quiz.questions
    correct_answers = []
    marks = []
    for i in range(len(questions)):
        question = questions[i]
        correct_answers.append(question["correct_answer"])
        marks.append(question["marks"])

    for answer in answers:
        answer_dict = {key: value for key, value in answer.__dict__.items() if not key.startswith('_') and not callable(value)}
        user_id = answer_dict["user_id"]
        ans_list = answer_dict["answers_list"]
        score = 0
        users_correct_answers = []
        j=0
        for j in range(len(ans_list)):
            print(f"\n {j+1}  {ans_list[j]}  {correct_answers[j]}\n")
            if correct_answers[j] == ans_list[j]:
                score += marks[j]
                users_correct_answers.append({"question no": j+1, "answer": ans_list[j]})
        scorecard.append({"user_id": user_id, "score": score, "correct_answers": users_correct_answers})
    return scorecard
    

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
