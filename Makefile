.PHONY: env all

env:
	conda env update -f environment.yml --prune

NOTEBOOKS := $(filter-out 1-intro_exploration.ipynb,$(wildcard *.ipynb))

all:
	jupyter nbconvert \
		--execute \
		--to notebook \
		--inplace \
		--ExecutePreprocessor.timeout=5 \
		1-intro_exploration.ipynb

	jupyter nbconvert \
		--execute \
		--to notebook \
		--inplace \
		$(NOTEBOOKS)


