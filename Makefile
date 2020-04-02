.PHONY: requirements
requirements:
	pipenv lock -r >> requirements/common.txt && pipenv lock -r --dev >> requirements/dev.txt

