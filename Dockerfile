FROM python:3.9

# Установка системных зависимостей (включая postgresql-client)
RUN apt-get update && apt-get install -y \
    graphviz \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем entrypoint и даём права на выполнение
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Устанавливаем entrypoint (CMD больше не нужен)
ENTRYPOINT ["/entrypoint.sh"]