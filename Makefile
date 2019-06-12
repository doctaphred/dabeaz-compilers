project := wabbit

# Default action: run the full build.
build: venv lint test

stash:
	git stash
	make build
	git stash pop

# Run the project's main module.
run: venv
	venv/bin/python -m $(project)

# Create a virtualenv ready to run a build.
venv:
	python3 -m venv venv
	venv/bin/pip install --upgrade pip==19.1.1  # TODO: is this fine?
	venv/bin/pip install -r requirements/base.txt -r requirements/build.txt
	venv/bin/pip install --editable .

lint: venv
	venv/bin/flake8 *.py src tests

test: venv
	venv/bin/pytest --doctest-modules src tests --doctest-glob='*.md'

# Open an IPython shell and import all top-level attributes.
shell: venv/bin/ipython
	venv/bin/ipython -i -c 'from $(project) import *'

# If a rule depends on a specific binary, assume it's a dev requirement.
dev venv/bin/%: venv
	venv/bin/pip install -r requirements/dev.txt

# Remove Python cruft.
pyclean:
	bin/pyclean

# Remove the virtualenv and any Python cruft.
clean: pyclean refresh
	-rm -r venv

# Remove cruft from runs of this project.
refresh:
	-rm errors.txt
	-rm hello.ll
	-rm hello.out

llvm:
	python -m wabbit.hellollvm
	clang main.c hello.ll -o hello.out
	./hello.out

wasm:
	python -m wabbit.wasm.generate

# Update all pinned requirements to their latest versions.
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
.PHONY: build run lint test shell dev pyclean clean refresh pin-requirements
