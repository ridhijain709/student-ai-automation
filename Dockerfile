FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app/backend
COPY app /app/app

EXPOSE 3000

# Production-ish default. For local dev, override command.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]

