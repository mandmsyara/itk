Backend приложение на FastAPI для работы с кошельками - списания и начисления средств.

Так же можно проверить текущий баланс и создать новый кошелек.

Запуск приложения:

    docker compose up --build

Доступ по адерсу:

    http://localhost:8000

Документация OpenAPI:

    http://localhost:8000/docs

Запуск тестов:

    docker compose exec app pytest -v

Стек: 

Python

FastAPI

PostgreSQL

SQLAlchemy

pytest

Docker / docker-compose

Базы данных: 

wallet_db - основная база приложения, для нее созданы миграции через Alembic

wallet_test_db - база данных postgres без миграций, заполняется при проведении 
тестов, потом вся информация с нее удаляется
