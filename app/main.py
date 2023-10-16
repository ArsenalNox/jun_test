import requests
import json 
import peewee
import os

from typing import Union, Optional, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, validator, Field

from app.models import Answer as Db_answer, Questions as Db_quesion
from app.models import pg_db

print(os.getcwd())

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')


with pg_db:
    pg_db.create_tables([Db_answer])


class Questions(BaseModel):
    questions_num: Optional[int] = None


class Answer(BaseModel):
    question_id: int
    created_at: str
    category: str
    question_text: str
    answer: str


@app.get('/', response_class=HTMLResponse)
async def return_index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


#Получить ворпос/вопросы
@app.post("/get")
async def get_questions(questions: Questions | None = None):
    num = 1 
    if questions != None:
        num = questions.questions_num

    tmp_questions = []
    while True:
        """
        Получать вопросы и сравнивать их с теми, на которые уже ответили в бд 
        Если айди вопроса уже есть в бд то получить новый вопрос
        """
        request = requests.get(f"https://jservice.io/api/random?count={1}")
        quesion = request.json()[0]

        check = Db_answer.select().where(
            Db_answer.question_id == quesion['id']
        ).count()

        if check < 1:
            tmp_questions.append(quesion)
        
        if len(tmp_questions) < num:
            continue
        else:
            break
    
    return {"questions": tmp_questions}


#Записать ответ
@app.post("/set_answer")
async def write_answers(answers: List[Answer]):
    for answer in answers:
        new_answer = Db_answer.create(
            question_id = answer.question_id,
            created_at = answer.created_at,
            category = answer.category,
            question_text = answer.question_text,
            answer = answer.answer
        )
        print(new_answer)

    return {"answers": answers}