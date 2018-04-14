.SECONDARY:

DAT = dat
PRETTY = ./botw/pretty
PYTHON = $(shell which python3)
JSON_TO_MOD = $(shell basename $@ .json)
VENV = venv/
mkdir = mkdir -p $(dir $@)

.PHONY: all
all: armors.stdout weapons.stdout

%.stdout: $(DAT)/%.json
	@cat $^ | $(PRETTY)

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
