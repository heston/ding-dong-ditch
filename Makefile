.PHONY: setup
setup:
	virtualenv venv -p python3
	source venv/bin/activate; \
	pip install -r requirements.txt

.PHONY: run
run:
	source venv/bin/activate; \
	python run.py
