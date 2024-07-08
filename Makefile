start:
	poetry run flask --app hexlet-flask-example.app --debug run --port 5000

server:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:5000 hexlet-flask-example.app:app
