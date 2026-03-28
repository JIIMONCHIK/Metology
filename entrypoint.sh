#!/bin/bash
set -e

# Ожидание готовности PostgreSQL
echo "Waiting for PostgreSQL..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is ready."

# Инициализация базы данных
echo "Initializing database..."
python init_db.py

# Запуск приложения
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000