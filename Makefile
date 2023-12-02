#!make

# define the name of the virtual environment directory
VENV := .venv
CMD_PYTHON = ./$(VENV)/bin/python3

# default target, when make executed without arguments
all: venv run lint

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/python3 -m pip install --upgrade pip
	./$(VENV)/bin/pip3 install -r requirements.txt

# venv is a shortcut target
venv: $(VENV)/bin/activate

run:
	$(CMD_PYTHON) main.py

test:
	./$(VENV)/bin/pytest test.py

lint:
	./$(VENV)/bin/black .
	./$(VENV)/bin/yamllint .github/workflows/ci.yml
	./$(VENV)/bin/yamllint .github/workflows/stale.yml
	./$(VENV)/bin/yamllint assistants.yml -d "{extends: default, rules: {line-length: {max: 120}}}"

clean:
	rm -rf $(VENV)
	rm -rf .pytest_cache
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run lint clean
