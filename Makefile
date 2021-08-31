# \ var
# detect module/project name by current directory
MODULE  = $(notdir $(CURDIR))
# detect OS name (only Linux in view)
OS      = $(shell uname -s)
# current date in the `ddmmyy` format
NOW     = $(shell date +%d%m%y)
# release hash: four hex digits (for snapshots)
REL     = $(shell git rev-parse --short=4 HEAD)
# current branch
BRANCH  = $(shell git rev-parse --abbrev-ref HEAD)
# number of CPU cores (for parallel builds)
CORES   = $(shell grep processor /proc/cpuinfo| wc -l)
# / var

# \ dir
# current (project) directory
CWD     = $(CURDIR)
# compiled/executable files (target dir)
BIN     = $(CWD)/bin
# documentation & external manuals downloads
DOC     = $(CWD)/doc
# libraries / scripts
LIB     = $(CWD)/lib
# source code (not for all languages, Rust/C included)
SRC     = $(CWD)/src
# temporary/generated files
TMP     = $(CWD)/tmp
# CArgo/Rust compiler binaries
CAR     = $(HOME)/.cargo/bin
# / dir

# \ tool
# \ tool
# http/ftp download tool
CURL    = curl -L -o
# Rust toolchain installer/updater
RUSTUP  = $(CAR)/rustup
# Rust Project Manager (most used)
CARGO   = $(CAR)/cargo
# build & restart on code changes
CWATCH  = $(CAR)/cargo-watch
# Rust Compiler
RUSTC   = $(CAR)/rustc

# Sometime Python can be used
PY      = $(BIN)/python3
PIP     = $(BIN)/pip3
PEP     = $(BIN)/autopep8
PYT     = $(BIN)/pytest
# / tool

# \ src
# C/C++
C += $(shell find src -type f -regex ".+.c(pp)?$$")
# Python
P += $(MODULE).py test_$(MODULE).py
# Rust
R += $(shell find src -type f -regex ".+.rs$$")
# all source code included into MERGE (public code)
S += $(F) $(C) $(P) $(R) Cargo.toml
# / src

# \ all
all: $(PY) $(MODULE).py
	$(MAKE) test format
	$^

rust: $(CWATCH)
	$< -w Cargo.toml -w src -x test -x fmt -x run

test: $(TMP)/test_py $(TMP)/test_rs
$(TMP)/test_py:
	$(PYT) test_$(MODULE).py && touch $@
$(TMP)/test_rs:
	$(CARGO) test && touch $@

meta: $(MODULE).py
	$(PY) $^ $@
	$(MAKE) format

format: $(TMP)/format_py $(TMP)/format_rs
$(TMP)/format_py: $(P)
	$(PEP) --ignore=E26,E302,E305,E401,E402,E701,E702 --in-place $?
	touch $@
$(TMP)/format_rs: $(R)
	$(CARGO) test && $(CARGO) fmt
	touch $@
# / all

# \ doc
doc: doc/Frames.pdf
doc/Frames.pdf:
	curl -L -o $@ https://courses.media.mit.edu/2004spring/mas966/Minsky%201974%20Framework%20for%20knowledge.pdf
# / doc

# \ install
install: $(OS)_install doc $(PIP) $(RUSTUP) update
update: $(OS)_update
	$(PIP) install -U    autopep8 pytest
	$(PIP) install -U -r requirements.txt
	$(RUSTUP) update ; $(CARGO) update

Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt apt.dev`

$(PY) $(PIP):
	python3 -m venv .

$(RUSTUP) $(CARGO):
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
	$(RUSTUP) toolchain install nightly
	$(RUSTUP) default nightly
$(CWATCH): $(CARGO)
	$< install cargo-watch

# / install

# \ merge
MERGE  = Makefile README.md .gitignore apt.* $(S)
MERGE += .vscode bin doc lib src tmp

.PHONY: dev
dev:
	git push -v
	git checkout $@
	git pull -v
	git checkout ponymuck -- $(MERGE)

.PHONY: ponymuck
ponymuck:
	git push -v
	git checkout $@
	git pull -v
# / merge
