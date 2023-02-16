# Запуск бэкэнда

1. Установить docker и docker-compose
2. Клонировать репозиторий
3. Выполнить команду `docker-compose up -d --build`
4. Выполнить команду `docker-compose exec web python manage.py migrate --noinput`
