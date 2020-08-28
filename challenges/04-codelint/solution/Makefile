.PHONY: black flake8 yamllint ansible-lint

default:
	echo "Please choose a task: black flake8 yamllint ansible-lint"

# Set up the virtual environment with dependencies
venv: venv/bin/activate

venv/bin/activate: requirements.txt
	test -d venv || python3 -m venv venv
	. venv/bin/activate; pip3 install -Ur requirements.txt
	touch venv/bin/activate

# The testing targets

all: black flake8 yamllint ansible-lint

# Lint and format Python files
black:
	black --check --diff code

flake8:
	flake8 --ignore E501 code

# Lint YAML files
yamllint:
	yamllint -s code/*.yml

# Lint Ansible Playbooks
ansible-lint:
	ansible-lint -Rr code/custom_rules code/pb*.yml
