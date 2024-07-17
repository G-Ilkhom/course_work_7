# Курсовая работа №8
## Инструкция по запуску
### Клонируйте репозиторий
```sh
git clone https://github.com/G-Ilkhom/course_work_7.git
```
### Выполните команду
```sh
docker-compose up -d --build
```

## Курсовая работа №7
### Проект представляет собой трекер полезных привычек, вдохновленный книгой "Атомные привычки" Джеймса Клира.

### Стек технологий

- **Python**
- **Django**
- **Redis**
- **Celery**
- **Poetry**
- **Postgres**

## Установка и настройка

Для установки проекта выполните следующие шаги:

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/G-Ilkhom/course_work_7.git
    ```

2. Перейдите в директорию проекта и создайте виртуальное окружение:
    ```sh
    cd course_work_7
    python -m venv venv
    ```

3. Активируйте виртуальное окружение:
    - На Windows:
      ```sh
      venv\Scripts\activate
      ```
    - На Unix или MacOS:
      ```sh
      source venv/bin/activate
      ```

4. Установите зависимости с помощью Poetry:
    ```sh
    poetry install
    ```

5. Создайте файл `.env` по образцу `.env.sample` и заполните необходимыми значениями.

6. Выполните миграции базы данных:
    ```sh
    python manage.py migrate
    ```

7. Запустите сервер разработки:
    ```sh
    python manage.py runserver
    ```
8. Запустите Redis локально(на Windows):
   ```sh
   celery -A config worker -l INFO -P eventlet
   ```