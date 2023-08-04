FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app
ENV SQLALCHEMY_DATABASE_URL="postgresql+asyncpg://ylab:no_secure_password@db/resto"

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
