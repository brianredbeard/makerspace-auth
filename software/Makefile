PYTHON?=python
NOSE?=$(PYTHON) -m nose

.PHONY: test
test:
	$(NOSE)

.PHONY: test_coverage
test_coverage:
	$(NOSE) --with-coverage --cover-package=authbox,two_button --cover-tests --cover-html

