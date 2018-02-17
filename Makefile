run:
	python manage.py runserver --settings=transcendence.settings --configuration=Dev

run-global:
	python manage.py runserver 0:8000 --settings=transcendence.settings --configuration=Dev

run-prod:
	python manage.py runserver 0:8000 --settings=transcendence.settings --configuration=Production

mkmigrations:
	python manage.py mkmigrations --settings=transcendence.settings --configuration=Dev

migrate:
	python manage.py migrate --settings=transcendence.settings --configuration=Dev

test:
	python manage.py test --settings=transcendence.settings --configuration=Dev

shell:
	python manage.py shell_plus --settings=transcendence.settings --configuration=Dev

inspect:
	prospector --strictness medium || :
