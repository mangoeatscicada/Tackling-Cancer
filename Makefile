init:
	pip install -e . --user

test:
	python -m tests.test

run:
	export FLASK_APP=tackling_cancer; export FLASK_DEBUG=true; python -m flask run

clean:
	find . -name '*.pyc' -delete
	find . -name '*tmp' -delete
	find . -name '*temp' -delete