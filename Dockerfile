# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменную окружения для отключения вывода буфера Python
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /hexlet_flask_example

# Копируем файлы зависимостей проекта
COPY pyproject.toml poetry.lock /hexlet_flask_example/

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости проекта
RUN poetry install --no-dev

# Копируем остальные файлы проекта
COPY hexlet_flask_example/scripts /hexlet_flask_example/scripts
COPY hexlet_flask_example/templates /hexlet_flask_example/templates
COPY hexlet_flask_example/app.py /hexlet_flask_example

# Указываем порт, который будет открыт для взаимодействия с приложением
EXPOSE 8080

# Указываем команду, которая будет выполняться при запуске контейнера
# CMD ["poetry", "run", "python", "app.py"]
# CMD ["poetry", "run", "gunicorn", "--workers=4", "--bind=0.0.0.0:8080", "app:app"]
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8080", "hexlet_flask_example:app"]