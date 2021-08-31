MODULE = $(notdir $(CURDIR))

PY  = bin/python3
PIP = bin/pip3
PEP = bin/autopep8
PYT = bin/pytest

all: $(PY) $(MODULE).py
	$(MAKE) test format
	$^

test: $(PYT) test_$(MODULE).py
	$^

meta: $(MODULE).py
	$(PY) $^ $@
	$(MAKE) format

format: $(MODULE).py test_$(MODULE).py
	$(PEP) --ignore=E26,E302,E305,E401,E402,E701,E702 --in-place $?

install:
	python3 -m venv .
	bin/pip3 install -U autopep8 pytest
	bin/pip3 install -U -r requirements.txt
