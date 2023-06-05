# получаем официальный образ python
FROM python:3.8.3-alpine

# устанавливаем рабочий каталог
WORKDIR /usr/src/app

# устанавливаем переменные среды:
# отключаем создание файлов .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# отключаем буферизацию и выводим все в терминал
ENV PYTHONUNBUFFERED 1

# установка зависимостей psycopg2 (для работы адаптера PostgreSQL для Python)
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
# установка зависимостей
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# копирование проекта в рабочий каталог
COPY . .


