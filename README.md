# HabitTracker — API для веб-приложения по отслеживанию привычек

## Обзор

1. **auth_service** - Отвечает за аутентификацию и авторизацию:
   - Регистрация и вход пользователей.
   - Работа с профилем.
   - Выдача токенов для доступа к другим сервисам.

2. **habit_tracker_service** - Отвечает за работу с привычками:
   - Создание, редактирование и удаление привычек.
   - Выполнение привычек.

3. **user_analytics_service** - Для пользовательской аналитики:
   - Выводит список активностей.

Микросервисы взаимодействуют между собой через RabbitMQ.

## Стек технологий

- **Backend-фреймворк**: FastAPI
- **База данных**: SQLite
- **Брокеры сообщений**: RabbitMQ
- **Прокси**: Nginx
- **Контейнеризация**: Docker

## Установка и запуск

### Требования

- [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта

Для запуска всех сервисов и необходимых зависимостей используйте следующую команду в корневой директории проекта:

```bash
docker-compose down
docker-compose up --build -d
```

Это позволит:
- Собрать и запустить все микросервисы вместе с зависимостями, такими как RabbitMQ.