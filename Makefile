.PHONY: all
all: armors weapons

.PHONY: armors
armors: dat/armors.json
	@cat $^ | ./botw/pretty

.PHONY: weapons
weapons: dat/weapons.json
	@cat $^ | ./botw/pretty

dat/armors.json: venv dat botw/main.py
	@$</bin/python \
		-m botw.armors > $@

dat/weapons.json: venv dat botw/main.py
	@$</bin/python \
		-m botw.weapons > $@

dat: gz/dat.tar.gz
	@mkdir dat
	@tar \
		--touch \
		--extract \
		--gunzip \
		--file $^ \
		--directory $@

venv: requirements.txt
	@virtualenv \
        	--no-site-packages \
		--python=$(which python3) \
		$@
	@$@/bin/pip install \
		--requirement $<
	@$@/bin/pip install \
		--upgrade pip
	@touch $@

.PHONY: clean
clean:
	@rm -rf dat/
	@rm -rf venv/
