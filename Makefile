# This Makefile requires the following commands to be available:
# * virtualenv
# * python3.5
# * docker
# * docker-compose
SHELL:=/bin/bash

.SUFFIXES:


DEPS:=requirements.txt
DOCKER_COMPOSE=$(shell which docker-compose)

PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
TOX=$(shell "$(CMD_FROM_VENV)" "tox")
PYTHON=$(shell "$(CMD_FROM_VENV)" "python")
TOX_PY_LIST="$(shell $(TOX) -l | grep ^py | xargs | sed -e 's/ /,/g')"
DETOX=./node_modules/.bin/detox
EXAMPLE_APP=./example
EXAMPLE_APP_NODE_MODULES=$(EXAMPLE_APP)/node_modules
EXAMPLE_APP_PODS=$(EXAMPLE_APP)/ios/Pods
EXAMPLE_APP_BINARY=$(EXAMPLE_APP)/ios/build/Build/Products/Release-iphonesimulator/example.app/example

.PHONY: clean docsclean pyclean test lint isort docs docker setup.py

tox: venv setup.py example_app
	env
	$(TOX)

pyclean:
	@find . -name *.pyc -delete
	@rm -rf *.egg-info build
	@rm -rf coverage.xml .coverage

docsclean:
	@rm -fr docs/_build/

clean: pyclean docsclean
	@rm -rf venv

venv:
	@python3.6 -m venv venv
	# pinning setuptools fixes: https://github.com/pypa/setuptools/issues/885
	# pinning pip, this version is required by pkgtools
	@$(PIP) install -U "pip==19.3.1" "setuptools==34.3.3"
	@$(PIP) install -r $(DEPS)


test: clean tox

test/%: venv pyclean
	$(TOX) -e $(TOX_PY_LIST) -- $*

lint: venv
	@$(TOX) -e lint
	@$(TOX) -e isort-check

isort: venv
	@$(TOX) -e isort-fix

docs: venv
	@$(TOX) -e docs

docker:
	$(DOCKER_COMPOSE) run --rm app bash

docker/%:
	$(DOCKER_COMPOSE) run --rm app make $*

setup.py: venv
	$(PYTHON) setup_gen.py
	@$(PYTHON) setup.py check --restructuredtext

build: clean tox

travis_build: venv setup.py example_app_build_rn_app
	env
	$(TOX)

$(DETOX): package.json
	npm install

$(EXAMPLE_APP_NODE_MODULES): $(EXAMPLE_APP)/package.json
	pushd example && npm install && popd

$(EXAMPLE_APP_BINARY): $(EXAMPLE_APP_NODE_MODULES) $(EXAMPLE_APP_PODS) $(DETOX)
	pushd example && $(DETOX) build --configuration ios.sim.release && popd

$(EXAMPLE_APP_PODS): $(EXAMPLE_APP)/ios/Podfile
	pushd example/ios && pod install && popd

jsdriventest:
	pushd example && $(DETOX) test --configuration ios.sim.release --cleanup && popd

example_app: $(EXAMPLE_APP_BINARY)

example_app_pods: $(EXAMPLE_APP_NODE_MODULES) $(EXAMPLE_APP_PODS)

example_app_node_modules: $(EXAMPLE_APP_NODE_MODULES)

example_app_build_rn_app:
	export RCT_NO_LAUNCH_PACKAGER=true && xcodebuild -workspace example/ios/example.xcworkspace -scheme example -configuration Release -sdk iphonesimulator -derivedDataPath example/ios/build | xcpretty -f `xcpretty-travis-formatter`

clean_example_app: clean_example_app_build clean_example_app_node_modules

clean_example_app_build:
	rm -rf $(EXAMPLE_APP)/ios/build

clean_example_app_node_modules:
	rm -rf $(EXAMPLE_APP_NODE_MODULES)
