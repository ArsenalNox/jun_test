# jun_test

## Порядок запуска 

- Клонировать этот репозиторий ```https://github.com/ArsenalNox/jun_test``` или скачать архивом
- Убедиться что установленны ```docker``` и ```docker-compose```
- Перейти в директорию с файлами ```docker``` и ```docker-compose.yml```
- Выполнить ```docker-compose build```
- Выполнить ```docker-compose up```

После чего на <http://127.0.0.1:8000/> станет доступна веб страница с вопросами.
При отсутсвии записанных вопросов в бд страница перезагрузится, будет необходимо заного нажать кнопку "Получить вопросы".

База данных доступна на 127.0.0.1:5432

## Пример запроса POST API сервиса

- Получение двух вопросов
```bash
curl --location 'http://127.0.0.1:8000/load_questions' \
--header 'Content-Type: application/json' \
--data '{
    "questions_num": 2
}'
```
- Получение вопроса без указание кол-ва
```bash
curl --location --request POST 'http://127.0.0.1:8000/load_questions' \
--data ''
```

Примеры доступны в ввиде Postman коллекции ```Jun-test.postman_collection.json```

## Подключение к бд c хоста проекта

### pgAdmin 

во вкладке Dashboard нажать на кнопку "Add New Server", указать имя сервера и в Connection указать "Host name/address" localhost или 127.0.0.1. Порт - 5433. имя пользователя совпадает со стандартным, пароль - "admin"

### psql 
Выполнить в консоли команду
```bash
psql --host localhost -U postgres --port 5433
```
Ввести пароль "admin" и подключится к бд my_app с помощью команды ```\c my_app```

## Траблшутинг

1. При запуске с linux систем необходимо добавить текущего пользователя в группу ```docker``` для запуска контейнера без root-прав
2. При подключении через psql с windows возможно некоректное отображение символов
3. Для запуска вне контейнера в файле ```.env``` следует указать ```environment=dev```
4. При неуспешному байнду к портам 8000 или 5433 убедится что они не заняты другими процессами и запустить прокет снова.
