.PHONY: deploy remove test_app test create_credentials black flake8

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  deploy             to deploy lambda service."
	@echo "  remove             to remove lambda service."
	@echo "  test_app           to exeute lambda application tests"
	@echo "  test               to exeute all tests."
	@echo "  create_credentials to create credentials.pickle."
	@echo "  black              to exeute auto format python codes by black."
	@echo "  flake8             to exeute flake8 to python codes."
	@echo "  help               to show this help messages."

set_env:
	export $(cat .env |grep -v '#')

deploy:
	./node_modules/serverless/bin/serverless deploy
	
remove:
	@echo "Remove the deployed service? [y/N] " && read ans && [ $${ans:-N} = y ]
	./node_modules/serverless/bin/serverless remove

test_app:
	tox -e py37

test: test_app flake8
	@echo '----------------------------'
	@echo 'Complete all testing.'
	@echo '----------------------------'

create_credentials:
	python ./src/utils/google_api.py

isort:
	isort -rc src

black: isort
	black src --config black/pyproject.toml

flake8:
	tox -e flake8
