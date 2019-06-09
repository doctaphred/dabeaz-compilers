project := compilers

build: venv lint test

run: venv
	venv/bin/python -m $(project)

venv:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip==19.1.1  # TODO: is this fine?
	venv/bin/pip install -r requirements/base.txt -r requirements/build.txt
	venv/bin/pip install --editable .

lint: venv
	venv/bin/flake8 *.py src tests

test: venv
	venv/bin/pytest tests

shell: venv/bin/ipython
	venv/bin/ipython -i -c 'from $(project) import *'

dev venv/bin/%: venv
	venv/bin/pip install -r requirements/dev.txt

pyclean:
	bin/pyclean

clean: pyclean
	-rm -r venv

pin-requirements: venv
	# TODO (maybe): Figure out how to do this via make dependencies.
	venv/bin/pip-compile --generate-hashes requirements/base.in
	venv/bin/pip-compile --generate-hashes requirements/build.in
	# ipython depends on setuptools, which is not safe to include in
	# requirements files: so we can't generate hashes for this one, or
	# else we'd have to install it with --allow-unsafe ಠ_ಠ
	venv/bin/pip-compile requirements/dev.in

# "Phony" targets do not reflect actual files. (It's not necessary to
# list them here unless they clash with actual file paths.)
.PHONY: build run lint test shell dev pyclean clean pin-requirements
