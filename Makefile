.PHONY: deploy remove test create-credentials

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  deploy             to deploy lambda app."
	@echo "  remove             to remove lambda app."
	@echo "  test               to exeute all tests."
	@echo "  create-credentials to create credentials.pickle."
	@echo "  help               to show this help messages."

deploy:
	./node_modules/serverless/bin/serverless deploy
	
remove:
	./node_modules/serverless/bin/serverless remove

create-credentials:
	python ./src/utils/google_api.py

test:
	python -m unittest discover -v
