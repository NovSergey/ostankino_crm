# Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8080"]
