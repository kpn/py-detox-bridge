# This Makefile requires the following commands to be available:
# * python3.7
# * rubygems

SRC:=detox_bridge tests setup.py
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DETOX=$(ROOT_DIR)/node_modules/.bin/detox

.PHONY: pyclean
pyclean:
	-find . -name "*.pyc" -delete
	-rm -rf *.egg-info build
	-rm -rf coverage*.xml .coverage

.PHONY: clean
clean: pyclean clean_example_app
	-rm -rf venv
	-rm -rf .tox

venv: PYTHON?=python3.7
venv:
	$(PYTHON) -m venv venv
	# FIXME: unpin when https://github.com/pypa/pip/issues/9215 is fixed
	venv/bin/pip install -U "pip==20.2" -q
	venv/bin/pip install -r requirements.txt

## Code style
.PHONY: lint
lint: lint/black lint/flake8 lint/isort lint/mypy

.PHONY: lint/black
lint/black: venv
	venv/bin/black --diff --check $(SRC)

.PHONY: lint/flake8
lint/flake8: venv
	venv/bin/flake8 $(SRC)

.PHONY: lint/isort
lint/isort: venv
	venv/bin/isort --diff --check $(SRC)

.PHONY: lint/mypy
lint/mypy: venv
	venv/bin/mypy $(SRC)

.PHONY: format
format: format/isort format/black

.PHONY: format/isort
format/isort: venv
	venv/bin/isort $(SRC)

.PHONY: format/black
format/black: venv
	venv/bin/black $(SRC)

## Tests
.PHONY: unittests
unittests: TOX_ENV?=ALL
unittests: TOX_EXTRA_PARAMS?=""
unittests: venv
	venv/bin/tox -e $(TOX_ENV) $(TOX_EXTRA_PARAMS)

.PHONY: test
test: pyclean unittests

## Distribution
.PHONY: changelog
changelog:
	venv/bin/gitchangelog

.PHONY: build
build: venv
	-rm -rf dist build
	venv/bin/python setup.py sdist bdist_wheel
	venv/bin/twine check dist/*

.PHONY: upload
upload: venv
	-rm -rf dist build
	venv/bin/python setup.py sdist bdist_wheel upload -r local

.PHONY: nvm_install
nvm_install:
	source "${NVM_DIR}/nvm.sh" && nvm install 15.2.1

.PHONY: app_github_requirements
app_github_requirements: nvm_install
	gem install xcpretty
	gem install xcpretty-travis-formatter

.PHONY: app_local_requirements
app_local_requirements: nvm_install
	sudo gem install xcpretty -n /usr/local/bin
	sudo gem install xcpretty-travis-formatter -n /usr/local/bin

## JS app related stuff
$(DETOX): package.json
	npm install

.PHONY: example_app_node_modules
example_app_node_modules: ./example/package.json
	pushd example && source "${NVM_DIR}/nvm.sh" && nvm use && npm install && popd

.PHONY: example_app_pods
example_app_pods: example_app_node_modules ./example/ios/Podfile
	pushd example/ios && pod install && popd

.PHONY: example_app_binary
example_app_binary: example_app_node_modules example_app_pods $(DETOX)
	pushd example && source "${NVM_DIR}/nvm.sh" && nvm use && $(DETOX) build --configuration ios.sim.release --logLevel trace && popd

.PHONY: jsdriventest
jsdriventest:
	pushd example && $(DETOX) test --configuration ios.sim.release --cleanup && popd

.PHONY: clean_example_app
clean_example_app: clean_example_app_build clean_example_app_node_modules clean_example_app_pods

.PHONY: clean_example_app_build
clean_example_app_build:
	rm -rf ./example/ios/build

.PHONY: clean_example_app_pods
clean_example_app_pods:
	rm -rf ./example/ios/Pods

.PHONY: clean_example_app_node_modules
clean_example_app_node_modules:
	rm -rf ./example/node_modules

.PHONY: docs
docs: venv
	sphinx-build -W -b html docs /docs/_build/html
