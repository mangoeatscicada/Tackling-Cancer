init:
	pip install -e . --user

test:
	python -m tests.test

run:
	export FLASK_APP="Tackling Cancer"; export FLASK_DEBUG=true; python run.py

clean:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name 'tmp' -type d -exec rm -r "{}" \;
	find . -name 'temp' -type d -exec rm -r "{}" \;