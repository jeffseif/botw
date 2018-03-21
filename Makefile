.SECONDARY:

DAT = dat
PRETTY = ./botw/pretty
PYTHON = $(which python3)
JSON_TO_MOD = $(shell basename $@ .json)
mkdir = mkdir -p $(dir $@)

.PHONY: all
all: armors.stdout weapons.stdout

%.stdout: $(DAT)/%.json
	@cat $^ | $(PRETTY)

$(DAT)/%.json: venv $(DAT)/ botw/main.py
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

venv: requirements.txt
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
	@rm -rf venv/
