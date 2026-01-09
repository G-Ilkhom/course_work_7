# Трекер полезных привычек
REST API-приложение, предназначенное для поддержки пользователей в достижении целей и формировании полезных привычек.
Пользователи могут создавать цели и привычки, отслеживать их выполнение и получать награды за регулярность.
Для повышения вовлечённости пользователей используется интеграция с Telegram Bot API, через который отправляются уведомления и напоминания.

### Стек технологий

- **Python**
- **Django**
- **Redis**
- **Celery**
- **Poetry**
- **Postgres**
- **Docker**

## Установка и настройка

### 1. Клонируйте репозиторий:
```sh
git clone https://github.com/G-Ilkhom/goal_tracking.git
cd goal_tracking
```

### 2. Настройте переменные окружения:
В корне проекта создайте файл .env и укажите необходимые переменные окружения:
```sh
DEBUG=True
SECRET_KEY=your_secret_key

POSTGRES_DB=app_db
POSTGRES_USER=app_user
POSTGRES_PASSWORD=app_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 3. Соберите Docker-образы и запустите проекта:
```sh
docker-compose up -d --build
```

### 4. Проверьте работу приложения
После успешного запуска:

- API доступно по адресу:
```sh
http://localhost:8000
```
- Административная панель Django:
```sh
http://localhost:8000/admin
```
### 5. Создайте суперпользователя (опционально)
Для доступа к административной панели выполните:
```sh
docker-compose exec app python manage.py createsuperuser
```
