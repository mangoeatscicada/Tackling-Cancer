init:
	pip install -r requirements.txt

test:
	python tackling-cancer/watson.py tests/test-zip.zip

create: 
	python tackling-cancer/watsonCreateClassifier.py