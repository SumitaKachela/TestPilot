# Test Automation Framework Makefile

# Variables
PYTHON = python
PIP = pip
BEHAVE = behave
TEST_ENV ?= dev
BROWSER ?= chrome
HEADLESS ?= false
TAGS ?= 
PARALLEL ?= false
WORKERS ?= 4

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help install setup clean test-ui test-api test-all report lint format

help: ## Show this help message
	@echo "$(GREEN)Test Automation Framework - Available Commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install all dependencies
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	playwright install

setup: install ## Setup the framework (install dependencies and create directories)
	@echo "$(GREEN)Setting up framework...$(NC)"
	@mkdir -p reports/logs reports/screenshots reports/html
	@echo "$(GREEN)Framework setup complete!$(NC)"

clean: ## Clean up generated files and reports
	@echo "$(YELLOW)Cleaning up...$(NC)"
	@rm -rf reports/logs/* reports/screenshots/* reports/html/*
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

test-ui: ## Run UI tests
	@echo "$(GREEN)Running UI tests...$(NC)"
	@export TEST_ENV=$(TEST_ENV) && \
	export BROWSER=$(BROWSER) && \
	export HEADLESS=$(HEADLESS) && \
	$(BEHAVE) features/ui/ --tags=@ui $(if $(TAGS),--tags=$(TAGS)) \
	--format=html --outfile=reports/html/ui_report.html \
	--format=json --outfile=reports/json/ui_results.json \
	$(if $(filter true,$(PARALLEL)),--processes=$(WORKERS))

test-api: ## Run API tests
	@echo "$(GREEN)Running API tests...$(NC)"
	@export TEST_ENV=$(TEST_ENV) && \
	$(BEHAVE) features/api/ --tags=@api $(if $(TAGS),--tags=$(TAGS)) \
	--format=html --outfile=reports/html/api_report.html \
	--format=json --outfile=reports/json/api_results.json \
	$(if $(filter true,$(PARALLEL)),--processes=$(WORKERS))

test-smoke: ## Run smoke tests
	@echo "$(GREEN)Running smoke tests...$(NC)"
	@export TEST_ENV=$(TEST_ENV) && \
	export BROWSER=$(BROWSER) && \
	export HEADLESS=$(HEADLESS) && \
	$(BEHAVE) features/ --tags=@smoke \
	--format=html --outfile=reports/html/smoke_report.html

test-regression: ## Run regression tests
	@echo "$(GREEN)Running regression tests...$(NC)"
	@export TEST_ENV=$(TEST_ENV) && \
	export BROWSER=$(BROWSER) && \
	export HEADLESS=$(HEADLESS) && \
	$(BEHAVE) features/ --tags=@regression \
	--format=html --outfile=reports/html/regression_report.html

test-all: ## Run all tests
	@echo "$(GREEN)Running all tests...$(NC)"
	@export TEST_ENV=$(TEST_ENV) && \
	export BROWSER=$(BROWSER) && \
	export HEADLESS=$(HEADLESS) && \
	$(BEHAVE) features/ $(if $(TAGS),--tags=$(TAGS)) \
	--format=html --outfile=reports/html/full_report.html \
	--format=json --outfile=reports/json/full_results.json \
	$(if $(filter true,$(PARALLEL)),--processes=$(WORKERS))

test-headless: ## Run tests in headless mode
	@$(MAKE) test-all HEADLESS=true

test-parallel: ## Run tests in parallel
	@$(MAKE) test-all PARALLEL=true WORKERS=$(WORKERS)

test-dev: ## Run tests against dev environment
	@$(MAKE) test-all TEST_ENV=dev

test-qa: ## Run tests against QA environment
	@$(MAKE) test-all TEST_ENV=qa

test-stage: ## Run tests against staging environment
	@$(MAKE) test-all TEST_ENV=stage

report: ## Generate and open HTML report
	@echo "$(GREEN)Opening test report...$(NC)"
	@if [ -f "reports/html/full_report.html" ]; then \
		open reports/html/full_report.html || xdg-open reports/html/full_report.html || start reports/html/full_report.html; \
	else \
		echo "$(RED)No report found. Run tests first.$(NC)"; \
	fi

lint: ## Run code linting
	@echo "$(GREEN)Running linting...$(NC)"
	@$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@$(PYTHON) -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format: ## Format code using black
	@echo "$(GREEN)Formatting code...$(NC)"
	@$(PYTHON) -m black . --line-length=127

# Environment-specific shortcuts
dev: ## Set environment to dev and run tests
	@$(MAKE) test-all TEST_ENV=dev

qa: ## Set environment to qa and run tests
	@$(MAKE) test-all TEST_ENV=qa

stage: ## Set environment to stage and run tests
	@$(MAKE) test-all TEST_ENV=stage

# Browser-specific shortcuts
chrome: ## Run tests with Chrome browser
	@$(MAKE) test-ui BROWSER=chrome

firefox: ## Run tests with Firefox browser
	@$(MAKE) test-ui BROWSER=firefox

safari: ## Run tests with Safari browser
	@$(MAKE) test-ui BROWSER=safari

# Tag-specific shortcuts
login: ## Run login-related tests
	@$(MAKE) test-all TAGS=@login

user: ## Run user-related tests
	@$(MAKE) test-all TAGS=@user

negative: ## Run negative test cases
	@$(MAKE) test-all TAGS=@negative

# Example usage commands
examples: ## Show example usage commands
	@echo "$(GREEN)Example Usage Commands:$(NC)"
	@echo ""
	@echo "$(YELLOW)Basic Commands:$(NC)"
	@echo "  make setup                    # Setup framework"
	@echo "  make test-ui                  # Run UI tests"
	@echo "  make test-api                 # Run API tests"
	@echo "  make test-all                 # Run all tests"
	@echo ""
	@echo "$(YELLOW)Environment-specific:$(NC)"
	@echo "  make test-all TEST_ENV=qa     # Run tests against QA"
	@echo "  make qa                       # Shortcut for QA tests"
	@echo ""
	@echo "$(YELLOW)Browser-specific:$(NC)"
	@echo "  make test-ui BROWSER=firefox  # Run UI tests with Firefox"
	@echo "  make firefox                  # Shortcut for Firefox tests"
	@echo ""
	@echo "$(YELLOW)Tag-specific:$(NC)"
	@echo "  make test-all TAGS=@smoke     # Run smoke tests"
	@echo "  make login                    # Run login tests"
	@echo ""
	@echo "$(YELLOW)Advanced:$(NC)"
	@echo "  make test-headless            # Run tests headless"
	@echo "  make test-parallel WORKERS=8  # Run tests in parallel"