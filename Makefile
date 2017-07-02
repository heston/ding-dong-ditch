SHELL := /bin/bash

.PHONY: setup
setup:
	stat venv/bin/activate &> /dev/null || \
	virtualenv venv -p python3.6
	source venv/bin/activate; \
	pip install -r requirements.txt

.PHONY: setup_test
setup_test:
	source venv/bin/activate; \
	pip install -r requirements.txt; \
	pip install -r requirements_test.txt
	cd server/functions; \
	npm install

.PHONY: setup_ci
setup_ci:
	pip install -r requirements.txt
	pip install -r requirements_test.txt
	cd server/functions; \
	npm install

.PHONY: install
install:
	sudo cp dingdongditch.service /lib/systemd/system/dingdongditch.service
	sudo chmod 644 /lib/systemd/system/dingdongditch.service
	sudo systemctl daemon-reload
	sudo systemctl enable dingdongditch.service
	sudo systemctl start dingdongditch
	sudo systemctl status dingdongditch

.PHONY: uninstall
uninstall:
	sudo systemctl stop dingdongditch
	sudo systemctl disable dingdongditch.service
	sudo rm /lib/systemd/system/dingdongditch.service
	sudo systemctl daemon-reload

.PHONY: run
run:
	source venv/bin/activate; \
	source env.sh; \
	python run.py

.PHONY: shell
shell:
	source venv/bin/activate; \
	source env.sh; \
	python

.PHONY: test_client
test_client:
	source venv/bin/activate; \
	PYTHONPATH=.:./tests/mocks py.test tests

.PHONY: lint_client
lint_client:
	source venv/bin/activate; \
	flake8 dingdongditch

.PHONY: test_server
test_server:
	cd server/functions; \
	npm test

.PHONY: test
test: test_server test_client

.PHONY: test_ci
test_ci: test_server
	PYTHONPATH=.:./tests/mocks py.test tests

.PHONY: lint_ci
lint_ci:
	flake8 dingdongditch
