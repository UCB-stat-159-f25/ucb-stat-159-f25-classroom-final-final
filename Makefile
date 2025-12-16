SHELL := /bin/bash

# Conda env
ENV_NAME := final-group25

# Output
EXEC_DIR := executed_notebooks
PDF_DIR := pdf_builds

.PHONY: help env run_notebooks test pdfs all clean

help:
	@echo "Targets:"
	@echo "  make env           Create/update conda env from environment.yml"
	@echo "  make run_notebooks Execute all .ipynb notebooks (writes to $(EXEC_DIR)/)"
	@echo "  make test          Run pytest"
	@echo "  make pdfs          Build MyST PDFs and copy into $(PDF_DIR)/"
	@echo "  make all           Run notebooks + tests + PDFs"
	@echo "  make clean         Remove generated artifacts"

env:
	@echo ">>> Creating/updating conda env: $(ENV_NAME)"
	@if conda env list | awk '{print $$1}' | grep -qx "$(ENV_NAME)"; then \
		echo "Env exists. Updating..."; \
		conda env update -n $(ENV_NAME) -f environment.yml --prune; \
	else \
		echo "Env does not exist. Creating..."; \
		conda env create -n $(ENV_NAME) -f environment.yml; \
	fi
	@echo ">>> Done."
	@echo ">>> Activate with: conda activate $(ENV_NAME)"

run_notebooks:
	@echo ">>> Executing notebooks in repo root with nbconvert..."
	@mkdir -p "$(EXEC_DIR)"
	@set -e; \
	while IFS= read -r -d '' nb; do \
		base=$$(basename "$$nb"); \
		echo "Running $$nb"; \
		jupyter nbconvert --to notebook --execute "$$nb" \
			--output "$$base" \
			--output-dir "$(EXEC_DIR)" \
			--ExecutePreprocessor.timeout=600; \
	done < <(find . -maxdepth 1 -name "*.ipynb" -not -path "*\.ipynb_checkpoints*" -print0)
	@echo ">>> Notebook execution complete. Outputs in $(EXEC_DIR)/"

test:
	@echo ">>> Running tests..."
	pytest -q
	@echo ">>> Tests complete."

pdfs:
	@echo ">>> Building MyST PDFs..."
	@mkdir -p "$(PDF_DIR)"
	@# Build PDFs (uses myst.yml in repo root)
	myst build --pdf
	@# Copy any PDFs produced by MyST into pdf_builds/
	@find _build -name "*.pdf" -maxdepth 6 -print -exec cp -f {} "$(PDF_DIR)/" \;
	@echo ">>> PDFs copied into $(PDF_DIR)/"

all: run_notebooks test pdfs
	@echo ">>> ALL DONE."

clean:
	@echo ">>> Cleaning generated files..."
	@rm -rf "$(EXEC_DIR)"
	@rm -rf _build
	@rm -rf "$(PDF_DIR)"
	@echo ">>> Clean complete."
