override SHELL := /bin/bash


.PHONY: init_db
init_db:
	-python3 manage.py db init
	-python3 manage.py db migrate
	-python3 manage.py db upgrade


.PHONY: delete_db
delete_db:
	-rm pizza.sqlite


.PHONY: populate_db
populate_db:
	-python3 populate.py


.PHONY: run
run:
	python3 manage.py run


.PHONY: test
test:
	python3 manage.py test