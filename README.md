# jun_test

## Порядок запуска 

- Убедиться что установленны ```docker``` и ```docker-compose```
- Выполнить ```docker-compose build```
- Выполнить ```docker-compose up```

После чего на <http://127.0.0.1:8000/> станет доступна веб страница с вопросами

База данных доступна на 127.0.0.1:5432

# Пример запроса POST API сервиса

```bash
curl --location 'http://127.0.0.1:8000/get/' \
--header 'Content-Type: application/json' \
--data '{
    "questions_num": 2
}'
```

Примеры доступны в ввиде Postman коллекции
