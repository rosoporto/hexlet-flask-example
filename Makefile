start:
	poetry run flask --app hexlet-flask-example.app --debug run --port 8080

server:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 hexlet-flask-example.app:app
