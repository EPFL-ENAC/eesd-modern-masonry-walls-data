# Data tools. Run from the repository root: the workflows call these targets.
UV := uv run --project tools python -m

.PHONY: help install test lint check ingest withdraw

help:      ## Show the targets
	@grep -E '^[a-z]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "%-10s %s\n", $$1, $$2}'

install:   ## Install the tools (uv sync)
	cd tools && uv sync

test:      ## Run the tests
	cd tools && uv run pytest

lint:      ## Check the style (ruff)
	cd tools && uv run ruff check . && uv run ruff format --check .

check:     ## Check a submission: make check SUBMISSION=submissions/<id>
	$(UV) mmw_data.validate "$(SUBMISSION)"

ingest:    ## Ingest a submission: make ingest SUBMISSION=submissions/<id>
	$(UV) mmw_data.ingest "$(SUBMISSION)"

withdraw:  ## Withdraw numbers: make withdraw N="238 239"
	$(UV) mmw_data.withdraw $(N)
