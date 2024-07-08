# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменную окружения для отключения вывода буфера Python
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей проекта
COPY pyproject.toml poetry.lock /app/

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости проекта
RUN poetry install --no-dev

# Копируем остальные файлы проекта
COPY hexlet-flask-example/app.py /app

# Указываем порт, который будет открыт для взаимодействия с приложением
EXPOSE 5000

# Указываем команду, которая будет выполняться при запуске контейнера
# CMD ["poetry", "run", "gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "app:app"]

CMD ["poetry", "run", "python", "app.py"]