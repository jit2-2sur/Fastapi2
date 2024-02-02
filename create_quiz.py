from models import *
from database import Session_local

db = Session_local()

users = [
    {"user_id": 1, "name": "Surajit"},
    {"user_id": 2, "name": "Partha"},
    {"user_id": 3, "name": "Raja"},
]

quizzes = [
    {
        "title": "Quiz 1",
        "time_duration": 30,
        "questions": [
            {
                "question_no": 1,
                "question_desc": "this is question 1",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "B",
            },
            {
                "question_no": 2,
                "question_desc": "this is question 2",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "C",
            },
            {
                "question_no": 3,
                "question_desc": "this is question 3",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "A",
            },
        ],
    },
    {
        "title": "Quiz 2",
        "time_duration": 45,
        "questions": [
            {
                "question_no": 1,
                "question_desc": "this is question 1",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "B",
            },
            {
                "question_no": 2,
                "question_desc": "this is question 2",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "C",
            },
            {
                "question_no": 3,
                "question_desc": "this is question 3",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "A",
            },
        ],
    },
    {
        "title": "Quiz 3",
        "time_duration": 60,
        "questions": [
            {
                "question_no": 1,
                "question_desc": "this is question 1",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "B",
            },
            {
                "question_no": 2,
                "question_desc": "this is question 2",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "C",
            },
            {
                "question_no": 3,
                "question_desc": "this is question 3",
                "marks": 1,
                "options": [
                    {"option_no": "A", "option_desc": "this is option 1"},
                    {"option_no": "B", "option_desc": "this is option 2"},
                    {"option_no": "C", "option_desc": "this is option 3"},
                    {"option_no": "D", "option_desc": "this is option 4"},
                ],
                "correct_answer": "A",
            },
        ],
    },
]

'''
answer_data = [
    {"answer_id": 1, "answers_list": ["B", "C", "A"]},
    {"answer_id": 2, "answers_list": ["B", "C", "D"]},
    {"answer_id": 3, "answers_list": ["A", "B", "C"]},
    {"answer_id": 4, "answers_list": ["B", "A", "C"]},
    {"answer_id": 5, "answers_list": ["B", "C", "A"]},
    {"answer_id": 6, "answers_list": ["A", "C", "C"]},
]

scorecard_data = {
    ///
}
'''

for user in users:
    new_user = User(**user)
    db.add(new_user)

for quiz in quizzes:
    new_quiz = Quiz(**quiz)
    db.add(new_quiz)

db.commit()