Это приложение на FastAPI для ресторана. В данной реализации оно содержит меню, подменю и блюда. В приложении использовались:
* ##### Python-фреймворки:
  * FastAPI
  * SQLAlchemy
* ##### Pre-commit хуки:
  * isort
  * pyupgrade
  * autopep8
  * flake8
  * mypy
* ##### Тесты:
  * Pytest
* ##### Базы данных:
  * PostgresSQL
  * Redis
* ##### Контейнеризация и оркестрация
  * Docker
#### Запуск приложения
docker-compose up

#### Запуск приложения + тестов
docker-compose -f docker-compose-test.yml up
