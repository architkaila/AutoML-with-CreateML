setup:
	pip install --upgrade pip
	pip install -r requirements.txt

format:
	black scripts/*.py

lint:
	pylint --disable=R,C scripts/data_prep.py

create_dataset:
	python scripts/data_prep.py --source ./data/raw_data --dest_train ./data/train --dest_test ./data/test

all: setup format lint create_dataset