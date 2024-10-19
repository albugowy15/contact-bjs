env_setup:
	python3 -m venv .venv

env_activate:
	. .venv/bin/activate

install:
	pip install -r requirements.txt

run:
	flask --app main run --debug

start:
	gunicorn -w 4 'main:app'

.PHONY: env_setup env_activate install run
