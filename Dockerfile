FROM python:3.13-slim

# Системные зависимости: компиляторы, PostgreSQL client, Redis, supervisor
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    redis-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt /app/requirements.txt

# Виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Обновляем pip и ставим зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект и supervisord.conf
COPY . /app
COPY supervisord.conf /app/supervisord.conf

# Создаём папку для логов
RUN mkdir -p /app/logs

# Экспонируем порты FastAPI и Redis
EXPOSE 8000 6379

# Запуск через supervisord
CMD ["supervisord", "-c", "/app/supervisord.conf"]
