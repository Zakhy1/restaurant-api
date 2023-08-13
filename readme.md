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
При клонировании репозитория будет необходимо создать свой файл .env согласно примеру _example.env_
`docker-compose up`

#### Запуск приложения + тестов
`docker-compose -f docker-compose-test.yml up`
