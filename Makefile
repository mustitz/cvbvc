CC=gcc
CFLAGS=-Wall -Wextra
PYTHON_FILES=$(wildcard *.py)

all: build lint

build: demo

demo: demo.c
	$(CC) $(CFLAGS) demo.c -o demo

lint:
	pylint $(PYTHON_FILES)

clean:
	rm -f demo

.PHONY: all build lint clean
