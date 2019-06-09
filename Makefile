project := compilers

build: venv lint test

run: venv
	venv/bin/python -m $(project)

venv $(addprefix venv/bin/,python pip):
	python3 -m venv venv
	venv/bin/pip install --upgrade pip==19.1.1  # TODO: is this fine?
	venv/bin/pip install --editable .

lint: venv/bin/flake8
	venv/bin/flake8 *.py src tests

test: venv/bin/pytest
	venv/bin/pytest tests

shell: venv/bin/ipython
	venv/bin/ipython -i -c 'from $(project) import *'

$(addprefix venv/bin/,flake8 pytest pycodestyle pyflakes): venv
	venv/bin/pip install --editable .[dev]

dev venv/bin/%: venv
	venv/bin/pip install ipython pdbpp pp-ez

pyclean:
	bin/pyclean

clean: pyclean
	-rm -r venv

pin-requirements: venv/bin/pip-compile
	# TODO (maybe): Figure out how to do this via make dependencies.
	venv/bin/pip-compile requirements/base.in
	venv/bin/pip-compile requirements/build.in
	venv/bin/pip-compile requirements/dev.in

# "Phony" targets do not reflect actual files. (It's not necessary to
# list them here unless they clash with actual file paths.)
.PHONY: build run lint test shell dev pyclean clean pin-requirements
