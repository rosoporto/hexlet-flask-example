start:
	poetry run flask --app hexlet_flask_example.app --debug run --port 5000

server:
	poetry run gunicorn --workers=4 --bind=0.0.0.0:5000 hexlet_flask_example.app:app
