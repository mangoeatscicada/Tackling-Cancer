init:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m tests.test

run:
	python -m flask run

clean:
	find . -name '*.pyc' -delete
	find . -name '*tmp' -delete
	find . -name '*temp' -delete