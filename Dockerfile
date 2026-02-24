FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

COPY database.sql .

RUN pip install gunicorn

EXPOSE 5555

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5555", "app:app"]