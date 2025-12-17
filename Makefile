.PHONY : env all

env:
	conda env update -f environment.yml --prune

all: