# Test Automation Framework

A comprehensive, production-ready test automation framework built with Python, Behave (BDD), Playwright for UI testing, and Requests for API testing.

## 🚀 Features

- **BDD Testing**: Behavior-driven development using Behave
- **UI Testing**: Cross-browser testing with Playwright (Chrome, Firefox, Safari)
- **API Testing**: RESTful API testing with Requests library
- **Page Object Model**: Clean, maintainable page object architecture
- **Parallel Execution**: Run tests in parallel for faster execution
- **Multiple Environments**: Support for dev, qa, and staging environments
- **Comprehensive Reporting**: HTML and JSON reports with screenshots
- **Flexible Configuration**: YAML-based configuration management
- **Logging**: Detailed logging with file and console output
- **Data-Driven Testing**: Support for JSON, YAML, CSV, and Excel test data
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📁 Project Structure

```
test-automation-framework/
├── features/                   # Feature files (BDD scenarios)
│   ├── ui/                    # UI test features
│   │   └── login.feature
│   └── api/                   # API test features
│       └── user_management.feature
├── steps/                     # Step definitions
│   ├── ui/                    # UI step definitions
│   │   └── login_steps.py
│   └── api/                   # API step definitions
│       └── user_api_steps.py
├── pages/                     # Page object models
│   └── ui/                    # UI page objects
│       ├── base_page.py
│       ├── login_page.py
│       └── dashboard_page.py
├── api/                       # API client modules
│   ├── base_api.py
│   └── user_api.py
├── utility/                   # Utility modules
│   ├── common/                # Common utilities
│   │   ├── logger.py
│   │   ├── config_reader.py
│   │   ├── screenshot_helper.py
│   │   └── wait_helper.py
│   └── data_loaders/          # Data loading utilities
│       └── test_data_loader.py
├── configs/                   # Configuration files
│   └── environments/
│       └── config.yaml
├── testdata/                  # Test data files
│   ├── ui/
│   │   └── login_data.yaml
│   └── api/
│       └── user_data.json
├── reports/                   # Test reports (auto-generated)
│   ├── html/
│   ├── json/
│   ├── logs/
│   └── screenshots/
├── environment.py             # Behave environment hooks
├── requirements.txt           # Python dependencies
├── Makefile                   # Make commands for easy execution
├── run.sh                     # Shell script runner (Unix/Linux/macOS)
├── run.bat                    # Batch script runner (Windows)
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Setup

1. **Clone or download the framework**
2. **Navigate to the project directory**
   ```bash
   cd test-automation-framework
   ```

3. **Run setup command**
   
   **Using Makefile (Unix/Linux/macOS):**
   ```bash
   make setup
   ```
   
   **Using shell script:**
   ```bash
   ./run.sh setup
   ```
   
   **Using batch script (Windows):**
   ```cmd
   run.bat setup
   ```
   
   **Manual setup:**
   ```bash
   pip install -r requirements.txt
   playwright install
   mkdir -p reports/logs reports/screenshots reports/html reports/json
   ```

## 🏃‍♂️ Running Tests

### Using Makefile (Recommended for Unix/Linux/macOS)

```bash
# Run all tests
make test-all

# Run UI tests only
make test-ui

# Run API tests only
make test-api

# Run smoke tests
make test-smoke

# Run tests with specific environment
make test-all TEST_ENV=qa

# Run tests with specific browser
make test-ui BROWSER=firefox

# Run tests in headless mode
make test-headless

# Run tests in parallel
make test-parallel WORKERS=8

# Run tests with specific tags
make test-all TAGS=@login
```

### Using Shell Scripts

**Unix/Linux/macOS:**
```bash
# Run all tests
./run.sh all

# Run UI tests with specific options
./run.sh ui --env=qa --browser=firefox --headless

# Run API tests
./run.sh api --env=stage

# Run smoke tests
./run.sh smoke --tags=@login

# Run tests in parallel
./run.sh all --parallel --workers=8
```

**Windows:**
```cmd
# Run all tests
run.bat all

# Run UI tests with specific options
run.bat ui --env=qa --browser=firefox --headless

# Run API tests
run.bat api --env=stage

# Run smoke tests
run.bat smoke --tags=@login
```

### Using Behave Directly

```bash
# Set environment variables
export TEST_ENV=dev
export BROWSER=chrome
export HEADLESS=false

# Run specific feature
behave features/ui/login.feature

# Run with tags
behave features/ --tags=@smoke

# Run with HTML report
behave features/ --format=html --outfile=reports/html/report.html
```

## 🔧 Configuration

### Environment Configuration

Edit `configs/environments/config.yaml` to configure:

- **Environments**: URLs and settings for dev, qa, staging
- **Browser Settings**: Default browser, headless mode, window size
- **Timeouts**: Page load, element wait, API request timeouts
- **Credentials**: Test user credentials (use environment variables in production)
- **Reporting**: Report formats and options

### Environment Variables

Set these environment variables to override configuration:

```bash
export TEST_ENV=qa          # Test environment (dev|qa|stage)
export BROWSER=firefox      # Browser (chrome|firefox|safari)
export HEADLESS=true        # Headless mode (true|false)
```

## 📊 Reports

### HTML Reports
- Generated in `reports/html/` directory
- Include test results, screenshots, and execution details
- Open with: `make report` or manually open the HTML file

### JSON Reports
- Generated in `reports/json/` directory
- Machine-readable format for CI/CD integration

### Logs
- Detailed execution logs in `reports/logs/`
- Separate log files for each test run

### Screenshots
- Automatic screenshots on test failures
- Stored in `reports/screenshots/`

## 🏷️ Test Tags

Use tags to organize and run specific test subsets:

- `@ui` - UI tests
- `@api` - API tests
- `@smoke` - Smoke tests
- `@regression` - Regression tests
- `@login` - Login-related tests
- `@user` - User management tests
- `@negative` - Negative test cases
- `@crud` - CRUD operation tests

### Running Tests by Tags

```bash
# Run smoke tests
make test-all TAGS=@smoke

# Run login tests
./run.sh all --tags=@login

# Run negative test cases
behave features/ --tags=@negative

# Combine tags (AND)
behave features/ --tags=@ui,@smoke

# Exclude tags
behave features/ --tags=~@slow
```

## 📝 Writing Tests

### Creating Feature Files

Create `.feature` files in the `features/` directory:

```gherkin
Feature: User Registration
  As a new user
  I want to register an account
  So that I can access the application

  @ui @registration @smoke
  Scenario: Successful user registration
    Given I am on the registration page
    When I fill in valid registration details
    And I click the register button
    Then I should see a success message
    And I should receive a confirmation email
```

### Creating Step Definitions

Create step definition files in the `steps/` directory:

```python
from behave import given, when, then
from pages.ui.registration_page import RegistrationPage

@given('I am on the registration page')
def step_navigate_to_registration(context):
    context.registration_page = RegistrationPage(context.page)
    context.registration_page.navigate_to('/register')

@when('I fill in valid registration details')
def step_fill_registration_form(context):
    context.registration_page.fill_registration_form(
        name="John Doe",
        email="john@example.com",
        password="securePassword123"
    )
```

### Creating Page Objects

Create page object classes in the `pages/ui/` directory:

```python
from pages.ui.base_page import BasePage

class RegistrationPage(BasePage):
    # Locators
    NAME_INPUT = "#name"
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    REGISTER_BUTTON = "#register-btn"
    
    def fill_registration_form(self, name, email, password):
        self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click_element(self.REGISTER_BUTTON)
```

### Creating API Clients

Create API client classes in the `api/` directory:

```python
from api.base_api import BaseAPI

class ProductAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.products_endpoint = "/api/v1/products"
    
    def create_product(self, product_data):
        response = self.post(self.products_endpoint, json_data=product_data)
        return {
            'response': response,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 201 else None
        }
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install
    
    - name: Run smoke tests
      run: make test-smoke TEST_ENV=qa HEADLESS=true
    
    - name: Upload test reports
      uses: actions/upload-artifact@v2
      if: always()
      with:
        name: test-reports
        path: reports/
```

### Jenkins Pipeline Example

```groovy
pipeline {
    agent any
    
    environment {
        TEST_ENV = 'qa'
        HEADLESS = 'true'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'make setup'
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('UI Tests') {
                    steps {
                        sh 'make test-ui'
                    }
                }
                stage('API Tests') {
                    steps {
                        sh 'make test-api'
                    }
                }
            }
        }
    }
    
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/html',
                reportFiles: '*.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Playwright browsers not installed**
   ```bash
   playwright install
   ```

2. **Permission denied on shell scripts**
   ```bash
   chmod +x run.sh
   ```

3. **Python module not found**
   ```bash
   pip install -r requirements.txt
   ```

4. **Tests failing due to timeouts**
   - Increase timeout values in `configs/environments/config.yaml`
   - Check network connectivity
   - Verify application availability

### Debug Mode

Run tests with verbose logging:

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
behave features/ --logging-level=DEBUG
```

## 🤝 Contributing

1. Follow the existing code structure and naming conventions
2. Add appropriate tags to new test scenarios
3. Update documentation for new features
4. Ensure all tests pass before submitting changes
5. Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
1. Check the troubleshooting section
2. Review the example test files
3. Check the configuration files for proper setup
4. Ensure all dependencies are installed correctly

## 🔄 Framework Architecture

### Design Principles

1. **Separation of Concerns**: Clear separation between test logic, page objects, and utilities
2. **DRY (Don't Repeat Yourself)**: Reusable components and utilities
3. **Maintainability**: Easy to update and extend
4. **Scalability**: Supports parallel execution and large test suites
5. **Flexibility**: Configurable for different environments and browsers

### Key Components

- **Environment Hooks**: Setup and teardown logic in `environment.py`
- **Base Classes**: Common functionality in `BasePage` and `BaseAPI`
- **Utilities**: Reusable helpers for logging, configuration, and data loading
- **Configuration Management**: Centralized configuration with environment support
- **Reporting**: Multiple report formats with screenshots and detailed logs

This framework provides a solid foundation for enterprise-grade test automation with best practices and production-ready features.