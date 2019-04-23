.PHONY: deploy remove pip-install create-credentials

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  deploy          to deploy lambda app."
	@echo "  remove          to remove lambda app."
	@echo "  test            to exeute all tests."
	@echo "  pip-install     to install python packages requirements.txt."
	@echo "  help            to show this help messages."

deploy:
	./node_modules/serverless/bin/serverless deploy
	
remove:
	./node_modules/serverless/bin/serverless remove

pip-install:
	pip install -r requirements.txt

create-credentials:
	python ./src/utils/google_api.py

test:
	python -m unittest discover -v
