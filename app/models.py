from peewee import * 

pg_db = PostgresqlDatabase('my_app', user='postgres', password='admin', host='project_db', port=5432)

class BaseModel(Model):
    class Meta:
        database = pg_db

class Answer(BaseModel):
    question_id = IntegerField(unique=True)
    created_at = DateTimeField()
    category = CharField()
    question_text = CharField()
    answer = CharField()

    class Meta:
        db_table = 'answers'


class Questions(BaseModel):
    question_id = IntegerField(unique=True)
    created_at = DateTimeField()
    category = CharField()
    question_text = CharField()
    answer = CharField()
    used = BooleanField(default=False)

    class Meta:
        db_table = 'questions'