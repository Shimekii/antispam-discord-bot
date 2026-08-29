FROM python:3.14-slim

WORKDIR /app

RUN python -m venv venv

COPY requirements.txt .

RUN venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["venv/bin/python", "main.py"]