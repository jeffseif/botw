.PHONY: all
all: run

.PHONY: run
run: dat.json
	@jq -S '.' $<

dat.json: venv dat
	@$</bin/python \
		-m botw.main > $@

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
