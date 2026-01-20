# Deribit Client App

Асинхронное приложение для получения и хранения котировок криптовалют (BTC, ETH и других) с API Deribit.  
Используется FastAPI для REST API, SQLAlchemy для работы с PostgreSQL и Celery + Redis для асинхронного сбора данных.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running](#running)
- [API Endpoints](#api-endpoints)
- [Design Decisions](#design-decisions)

---

## Features

- Асинхронный сбор котировок криптовалют через Deribit API
- Сохранение данных в PostgreSQL
- REST API для получения:
  - всех котировок по тикеру
  - последней котировки
  - котировок за определённую дату
- Автоматический планировщик задач с Celery Beat
- Лёгкая расширяемость (новые тикеры, новые API источники)

---

## Tech Stack

- **Python 3.13**
- **FastAPI** – web framework
- **SQLAlchemy (async)** – ORM для работы с PostgreSQL
- **PostgreSQL** – база данных
- **Redis** – брокер сообщений для Celery
- **Celery** – асинхронные задачи и планировщик
- **aiohttp** – асинхронные HTTP-запросы к внешнему API

---

## Installation and Running

1. Создаём .env файл в корне проекта, как в .env.example

# 2. Clone repository
git clone <your-repo-url>
cd crypto-prices

# 3. Install dependencies
python -m venv .venv

# Linux / Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt

# 4. Поднимаем Docker-контейнеры
docker-compose up -d

---

## Design Decisions

## Запуск
- В условиях задачи указано деплоить приложение и базу данных в 2 контейнера. Поэтому было принято решение запускать Redis и Celery в том же контейнере, что и приложение, с использованием Linux-сервиса **supervisord**.
- Для тестового задания такой подход приемлем. Однако в продакшене лучше разделить приложение, Redis и Celery по отдельным контейнерам для масштабируемости и надежности.


### Асинхронность
- FastAPI позволяет не блокировать event loop при многократных запросах.
- SQLAlchemy async сессии позволяют одновременно работать с базой и получать данные.

### Celery + Redis
- Celery вынесен в отдельный процесс, чтобы задачи не блокировали FastAPI.
- Redis используется как брокер для задач.

### PriceService + Factory
- Сервис инкапсулирует бизнес-логику работы с котировками.
- Фабрика позволяет централизованно создавать сервис и в будущем легко менять реализацию.

### Модульная архитектура
- `services`, `repositories`, `factories`, `clients`, `db`, `api` – каждая часть проекта отвечает за отдельную задачу.
- Проект легко расширять и поддерживать.

### Сессии SQLAlchemy
- Каждое обращение к бд использует отдельную `AsyncSession`.
- Таблицы создаются один раз при старте через метод `init_tables()`.

### Обработка ошибок
- Ошибки получения котировок логируются в файл, чтобы задачи Celery не падали полностью из-за одного тикера.
