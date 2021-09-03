.PHONY: docs clean

COMMAND = docker-compose run --rm djangoapp /bin/bash -c

all: build test

build:
	docker-compose build

run:
	docker-compose up

migrations:
	docker-compose run --rm djangoapp main/manage.py makemigrations

user:
	docker-compose run --rm djangoapp main/manage.py shell -c "from core.models import User; User.objects.create_superuser('xkito@bonch.dev', 'O22QTk4PtQC916r')"

reset:
	docker-compose run --rm djangoapp main/manage.py reset_db

migrate:
	$(COMMAND) 'cd main; for db in default; do ./manage.py migrate --database=$${db}; done'

collectstatic:
	docker-compose run --rm djangoapp main/manage.py collectstatic --no-input

check: checksafety checkstyle

test:
	$(COMMAND) "pip install tox && tox -e test"

checksafety:
	$(COMMAND) "pip install tox && tox -e checksafety"

checkstyle:
	$(COMMAND) "pip install tox && tox -e checkstyle"

coverage:
	$(COMMAND) "pip install tox && tox -e coverage"

clean:
	rm -rf build
	rm -rf main.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm -rf .tox
	rm -rf .cache
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -rf $(find . -type d -name __pycache__)
	rm -rf .coverage

dockerclean:
	docker system prune -f
	docker system prune -f --volumes
