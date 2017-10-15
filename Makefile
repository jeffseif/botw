.PHONY: all
all: armors weapons

.PHONY: armors
armors: armors.json
	@cat $^ | ./botw/pretty

.PHONY: weapons
weapons: weapons.json
	@cat $^ | ./botw/pretty

armors.json: venv dat
	@$</bin/python \
		-m botw.armors > $@

weapons.json: venv dat
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
	@rm -f dat.json
