# Stage 1: Development
FROM python:3.11-slim AS development

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8088
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8088", "--reload"]
