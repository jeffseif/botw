.SECONDARY:

JSON_TO_MOD = $(shell basename $@ .json)
PYTHON = $(shell which python3)
mkdir = mkdir -p $(dir $@)

DAT = dat
JSON_TO_STDOUT = ./botw/json_to_stdout.sh
JSON_TO_MARKDOWN = ./botw/json_to_markdown.sh
VENV = venv/

.PHONY: all
all: armors.stdout weapons.stdout armors.md weapons.md

%.stdout: $(DAT)/%.json
	@cat $< | $(JSON_TO_STDOUT)

%.md: $(DAT)/%.json
	@cat $< | $(JSON_TO_MARKDOWN) > $@

$(DAT)/%.json: $(VENV) $(DAT)/ botw/main.py
	@$</bin/python \
		-m botw.main $(JSON_TO_MOD) > $@

$(DAT)/: gz/$(DAT).tar.gz
	@$(mkdir)
	@tar \
		--touch \
		--extract \
		--gunzip \
		--file $< \
		--directory $@

$(VENV): requirements.txt
	@virtualenv \
        	--no-site-packages \
		--python=$(PYTHON) \
		$@
	@$@/bin/pip install \
		--requirement $<
	@$@/bin/pip install \
		--upgrade pip
	@touch $@

.PHONY: clean
clean:
	@rm -rf $(DAT)/
	@rm -rf $(VENV)
	@find . -name '*.pyc' -delete
	@find . -name '__pycache__' -type d -delete
