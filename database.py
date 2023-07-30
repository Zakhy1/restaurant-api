import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Получение данных для подключения к БД
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)

# DB_USER = os.environ.get("POSTGRES_USER")
# DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
# DB_NAME = os.environ.get("POSTGRES_DB")
# DB_HOST = os.environ.get("POSTGRES_HOST")
# Подключение к БД
SQLALCHEMY_DATABASE_URL = f"postgresql://restaurant_manager:b24de59f8c8fe841be3b@postgres-rest:5432/restaurant_api"

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    echo=True  # Turn off when send
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = Session()
