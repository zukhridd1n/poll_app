migrate:
	python manage.py makemigrations
	python manage.py migrate

user:
	python manage.py createsuperuser --username=zuxriddin --email=zuxriddinsharobiddinov2004@gmaill.com


sort:
	black .
	isort .