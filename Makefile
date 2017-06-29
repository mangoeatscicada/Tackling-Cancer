init:
	pip install -r requirements.txt
	export FLASK_APP=tackling_cancer
	export FLASK_DEBUG=true
	pip install -e . --user

test:
	python -m tests.test

run:
	python tackling-cancer.py

run2:
	python -m flask run

clean:
	find . -name '*.pyc' -delete
	find . -name '*tmp' -delete
	find . -name '*temp' -delete