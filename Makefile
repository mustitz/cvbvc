CC=gcc
CFLAGS=-Wall -Wextra
PYTHON_FILES=$(wildcard *.py)

all: build check lint

build: demo

demo: demo.c
	$(CC) $(CFLAGS) demo.c -o demo

check:
	pytest

lint:
	pylint $(PYTHON_FILES)

clean:
	rm -f demo

.PHONY: all build check lint clean
