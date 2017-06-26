init:
	pip install -r requirements.txt

test-blood:
	python tackling-cancer/watson.py tests/test-blood.jpg

test-cancer:
	python tackling-cancer/watson.py tests/test-cancer.jpg

test-other:
	python tackling-cancer/watson.py tests/test-other.jpg

test-zip:
	python tackling-cancer/watson.py tests/test-zip.zip

test:
	python tackling-cancer/watson.py tests/test.jpg

create: 
	python tackling-cancer/watsonCreateClassifier.py

run:
	python tackling-cancer.py