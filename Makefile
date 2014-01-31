.PHONY: docs

init:
	pip install -r requirements.txt

test:
	python runtests.py

publish:
	python setup.py register
	python setup.py sdist upload
	python setup.py bdist_wheel upload
	@echo "\033[95m\n\nRelease published. You should tag this version now.\n\033[0m"

docs-init:
	pip install -r docs/requirements.txt

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
	open docs/_build/html/index.html
