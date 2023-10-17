import requests
import json 
import peewee
import os

from typing import Union, Optional, List

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, validator, Field

from dotenv import load_dotenv

load_dotenv()

if os.getenv('environment') == 'dev':
    from models import Answer as Db_answer, Questions as Db_quesion
    from models import pg_db
else:
    from app.models import Answer as Db_answer, Questions as Db_quesion
    from app.models import pg_db

app = FastAPI()


if os.getenv('environment') == 'dev':
    app.mount('/static', StaticFiles(directory='static'), name='static')
    templates = Jinja2Templates(directory='templates')
else:
    app.mount('/static', StaticFiles(directory='app/static'), name='static')
    templates = Jinja2Templates(directory='app/templates')

#Создание таблиц базы данных если они не существуют
with pg_db:
    pg_db.create_tables([Db_answer, Db_quesion])


#Валидатор для кол-ва вопросов
class Questions(BaseModel):
    questions_num: Optional[int] = None


#Валидатор для ответов
class Answer(BaseModel):
    question_id: int
    created_at: str
    category: str
    question_text: str
    answer: str


@app.get('/', response_class=HTMLResponse)
async def return_index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

#Записать в бд вопросы 
@app.post("/load_questions", status_code=201)
async def load_questions(questions: Questions | None = None):
    num = 1 
    if questions != None:
        num = questions.questions_num

    #Выбрать последние N записанных вопросов
    select_questions = Db_quesion.select().where(
        Db_quesion.is_used == False
        ).order_by(Db_quesion.id.desc()).limit(num).execute()

    return_questions = []
    for q in select_questions:
        return_questions.append({
            "id": q.question_id,
            "created_at": q.created_at,
            "category": q.category,
            "question": q.question_text
        })

    tmp_questions = []
    while True:
        """
        Получать вопросы и сравнивать их с теми, на которые уже ответили в бд 
        Если айди вопроса уже есть в бд то получить новый вопрос
        """
        request = requests.get(f"https://jservice.io/api/random?count={1}")
        question = request.json()[0]

        check = Db_answer.select().where(
            Db_answer.question_id == question['id']
        ).count()

        if check < 1:
            tmp_questions.append(question)

        if len(tmp_questions) < num:
            continue
        else:
            break

    for question in tmp_questions:

        new_question = Db_quesion.create(
            question_id = question['id'],
            created_at = question['created_at'],
            category = question['category']['title'],
            question_text = question['question'],
        )

    return {"questions": return_questions}


#Записать ответ
@app.post("/set_answer", status_code=201)
async def write_answers(answers: List[Answer], response: Response):
    for answer in answers:
        try:
            new_answer = Db_answer.create(
                question_id = answer.question_id,
                created_at = answer.created_at,
                category = answer.category,
                question_text = answer.question_text,
                answer = answer.answer
            )
        except Exception as err:
            response.status_code = status.HTTP_409_CONFLICT

    return 