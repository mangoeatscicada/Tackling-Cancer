init:
	pip install -r requirements.txt

test:
	python -m tests.test

run:
	python tackling-cancer.py