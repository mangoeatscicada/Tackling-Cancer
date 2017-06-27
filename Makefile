init:
	pip install -r requirements.txt

test:
	python -m tests.test

run:
	python tackling-cancer.py

clean:
	find . -name '*.pyc' -delete
	find . -name '*tmp' -delete
	find . -name '*temp' -delete

run_test:
	python -m tackling_cancer.tackling_cancer