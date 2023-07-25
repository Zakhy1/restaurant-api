#### Что понадобится:

1. Docker
2. Виртуальное окружение

#### Порядок действий:

1. git clone https://github.com/Zakhy1/restaurant-api.git
2. cd restaurant-api 
3. pip install -r requirements.txt
4. docker-compose up
5. python create_tables.py
6. uvicorn main:app --reload