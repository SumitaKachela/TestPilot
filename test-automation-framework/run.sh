#!/bin/bash

# Test Automation Framework Runner Script
# This script provides easy commands to run tests with different configurations

set -e  # Exit on any error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
TEST_ENV=${TEST_ENV:-dev}
BROWSER=${BROWSER:-chrome}
HEADLESS=${HEADLESS:-false}
PARALLEL=${PARALLEL:-false}
WORKERS=${WORKERS:-4}
TAGS=""

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show help
show_help() {
    echo -e "${GREEN}Test Automation Framework Runner${NC}"
    echo ""
    echo "Usage: ./run.sh [COMMAND] [OPTIONS]"
    echo ""
    echo -e "${YELLOW}Commands:${NC}"
    echo "  setup           Setup the framework (install dependencies)"
    echo "  ui              Run UI tests"
    echo "  api             Run API tests"
    echo "  all             Run all tests"
    echo "  smoke           Run smoke tests"
    echo "  regression      Run regression tests"
    echo "  clean           Clean up reports and cache"
    echo "  report          Open latest HTML report"
    echo "  help            Show this help message"
    echo ""
    echo -e "${YELLOW}Options:${NC}"
    echo "  --env=ENV       Set test environment (dev|qa|stage) [default: dev]"
    echo "  --browser=BR    Set browser (chrome|firefox|safari) [default: chrome]"
    echo "  --headless      Run in headless mode"
    echo "  --parallel      Run tests in parallel"
    echo "  --workers=N     Number of parallel workers [default: 4]"
    echo "  --tags=TAGS     Run tests with specific tags"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  ./run.sh setup"
    echo "  ./run.sh ui --env=qa --browser=firefox"
    echo "  ./run.sh all --headless --parallel --workers=8"
    echo "  ./run.sh smoke --tags=@login"
    echo "  ./run.sh api --env=stage"
}

# Function to setup framework
setup_framework() {
    print_info "Setting up Test Automation Framework..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Install dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Install Playwright browsers
    print_info "Installing Playwright browsers..."
    playwright install
    
    # Create necessary directories
    print_info "Creating report directories..."
    mkdir -p reports/logs reports/screenshots reports/html reports/json
    
    print_success "Framework setup completed successfully!"
}

# Function to clean up
clean_up() {
    print_info "Cleaning up generated files..."
    
    # Remove reports
    rm -rf reports/logs/* reports/screenshots/* reports/html/* reports/json/* 2>/dev/null || true
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "Cleanup completed!"
}

# Function to run tests
run_tests() {
    local test_type=$1
    local feature_path=""
    local report_name=""
    
    case $test_type in
        "ui")
            feature_path="features/ui/"
            report_name="ui_report"
            TAGS="${TAGS} @ui"
            ;;
        "api")
            feature_path="features/api/"
            report_name="api_report"
            TAGS="${TAGS} @api"
            ;;
        "all")
            feature_path="features/"
            report_name="full_report"
            ;;
        "smoke")
            feature_path="features/"
            report_name="smoke_report"
            TAGS="${TAGS} @smoke"
            ;;
        "regression")
            feature_path="features/"
            report_name="regression_report"
            TAGS="${TAGS} @regression"
            ;;
    esac
    
    print_info "Running $test_type tests..."
    print_info "Environment: $TEST_ENV"
    print_info "Browser: $BROWSER"
    print_info "Headless: $HEADLESS"
    print_info "Parallel: $PARALLEL"
    if [ -n "$TAGS" ]; then
        print_info "Tags: $TAGS"
    fi
    
    # Set environment variables
    export TEST_ENV=$TEST_ENV
    export BROWSER=$BROWSER
    export HEADLESS=$HEADLESS
    
    # Build behave command
    local behave_cmd="behave $feature_path"
    
    # Add tags if specified
    if [ -n "$TAGS" ]; then
        behave_cmd="$behave_cmd --tags=\"$TAGS\""
    fi
    
    # Add output formats
    behave_cmd="$behave_cmd --format=html --outfile=reports/html/${report_name}.html"
    behave_cmd="$behave_cmd --format=json --outfile=reports/json/${report_name}.json"
    
    # Add parallel execution if enabled
    if [ "$PARALLEL" = "true" ]; then
        behave_cmd="$behave_cmd --processes=$WORKERS"
    fi
    
    # Execute tests
    print_info "Executing: $behave_cmd"
    eval $behave_cmd
    
    if [ $? -eq 0 ]; then
        print_success "$test_type tests completed successfully!"
        print_info "Report generated: reports/html/${report_name}.html"
    else
        print_error "$test_type tests failed!"
        exit 1
    fi
}

# Function to open report
open_report() {
    local report_file="reports/html/full_report.html"
    
    # Check for specific report files
    if [ -f "reports/html/ui_report.html" ]; then
        report_file="reports/html/ui_report.html"
    elif [ -f "reports/html/api_report.html" ]; then
        report_file="reports/html/api_report.html"
    elif [ -f "reports/html/smoke_report.html" ]; then
        report_file="reports/html/smoke_report.html"
    fi
    
    if [ -f "$report_file" ]; then
        print_info "Opening report: $report_file"
        
        # Try different commands based on OS
        if command -v open &> /dev/null; then
            open "$report_file"  # macOS
        elif command -v xdg-open &> /dev/null; then
            xdg-open "$report_file"  # Linux
        elif command -v start &> /dev/null; then
            start "$report_file"  # Windows
        else
            print_warning "Cannot open report automatically. Please open: $report_file"
        fi
    else
        print_error "No report found. Run tests first."
        exit 1
    fi
}

# Parse command line arguments
COMMAND=""
while [[ $# -gt 0 ]]; do
    case $1 in
        setup|ui|api|all|smoke|regression|clean|report|help)
            COMMAND=$1
            shift
            ;;
        --env=*)
            TEST_ENV="${1#*=}"
            shift
            ;;
        --browser=*)
            BROWSER="${1#*=}"
            shift
            ;;
        --headless)
            HEADLESS=true
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        --workers=*)
            WORKERS="${1#*=}"
            shift
            ;;
        --tags=*)
            TAGS="${1#*=}"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Execute command
case $COMMAND in
    "setup")
        setup_framework
        ;;
    "ui"|"api"|"all"|"smoke"|"regression")
        run_tests $COMMAND
        ;;
    "clean")
        clean_up
        ;;
    "report")
        open_report
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac