@echo off
REM Test Automation Framework Runner Script for Windows
REM This script provides easy commands to run tests with different configurations

setlocal enabledelayedexpansion

REM Default values
if "%TEST_ENV%"=="" set TEST_ENV=dev
if "%BROWSER%"=="" set BROWSER=chrome
if "%HEADLESS%"=="" set HEADLESS=false
if "%PARALLEL%"=="" set PARALLEL=false
if "%WORKERS%"=="" set WORKERS=4
set TAGS=

REM Colors (limited support in Windows CMD)
set GREEN=[92m
set YELLOW=[93m
set RED=[91m
set BLUE=[94m
set NC=[0m

goto :parse_args

:print_info
echo %BLUE%[INFO]%NC% %~1
goto :eof

:print_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

:show_help
echo %GREEN%Test Automation Framework Runner%NC%
echo.
echo Usage: run.bat [COMMAND] [OPTIONS]
echo.
echo %YELLOW%Commands:%NC%
echo   setup           Setup the framework (install dependencies)
echo   ui              Run UI tests
echo   api             Run API tests
echo   all             Run all tests
echo   smoke           Run smoke tests
echo   regression      Run regression tests
echo   clean           Clean up reports and cache
echo   report          Open latest HTML report
echo   help            Show this help message
echo.
echo %YELLOW%Options:%NC%
echo   --env=ENV       Set test environment (dev^|qa^|stage) [default: dev]
echo   --browser=BR    Set browser (chrome^|firefox^|safari) [default: chrome]
echo   --headless      Run in headless mode
echo   --parallel      Run tests in parallel
echo   --workers=N     Number of parallel workers [default: 4]
echo   --tags=TAGS     Run tests with specific tags
echo.
echo %YELLOW%Examples:%NC%
echo   run.bat setup
echo   run.bat ui --env=qa --browser=firefox
echo   run.bat all --headless --parallel --workers=8
echo   run.bat smoke --tags=@login
echo   run.bat api --env=stage
goto :eof

:setup_framework
call :print_info "Setting up Test Automation Framework..."

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Python is not installed. Please install Python 3.8 or higher."
    exit /b 1
)

REM Install dependencies
call :print_info "Installing Python dependencies..."
pip install -r requirements.txt
if errorlevel 1 (
    call :print_error "Failed to install dependencies"
    exit /b 1
)

REM Install Playwright browsers
call :print_info "Installing Playwright browsers..."
playwright install
if errorlevel 1 (
    call :print_error "Failed to install Playwright browsers"
    exit /b 1
)

REM Create necessary directories
call :print_info "Creating report directories..."
if not exist "reports" mkdir reports
if not exist "reports\logs" mkdir reports\logs
if not exist "reports\screenshots" mkdir reports\screenshots
if not exist "reports\html" mkdir reports\html
if not exist "reports\json" mkdir reports\json

call :print_success "Framework setup completed successfully!"
goto :eof

:clean_up
call :print_info "Cleaning up generated files..."

REM Remove reports
if exist "reports\logs\*" del /q "reports\logs\*" 2>nul
if exist "reports\screenshots\*" del /q "reports\screenshots\*" 2>nul
if exist "reports\html\*" del /q "reports\html\*" 2>nul
if exist "reports\json\*" del /q "reports\json\*" 2>nul

REM Remove Python cache
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul

call :print_success "Cleanup completed!"
goto :eof

:run_tests
set test_type=%~1
set feature_path=
set report_name=

if "%test_type%"=="ui" (
    set feature_path=features/ui/
    set report_name=ui_report
    set TAGS=%TAGS% @ui
) else if "%test_type%"=="api" (
    set feature_path=features/api/
    set report_name=api_report
    set TAGS=%TAGS% @api
) else if "%test_type%"=="all" (
    set feature_path=features/
    set report_name=full_report
) else if "%test_type%"=="smoke" (
    set feature_path=features/
    set report_name=smoke_report
    set TAGS=%TAGS% @smoke
) else if "%test_type%"=="regression" (
    set feature_path=features/
    set report_name=regression_report
    set TAGS=%TAGS% @regression
)

call :print_info "Running %test_type% tests..."
call :print_info "Environment: %TEST_ENV%"
call :print_info "Browser: %BROWSER%"
call :print_info "Headless: %HEADLESS%"
call :print_info "Parallel: %PARALLEL%"
if not "%TAGS%"=="" call :print_info "Tags: %TAGS%"

REM Set environment variables
set TEST_ENV=%TEST_ENV%
set BROWSER=%BROWSER%
set HEADLESS=%HEADLESS%

REM Build behave command
set behave_cmd=behave %feature_path%

REM Add tags if specified
if not "%TAGS%"=="" set behave_cmd=%behave_cmd% --tags="%TAGS%"

REM Add output formats
set behave_cmd=%behave_cmd% --format=html --outfile=reports/html/%report_name%.html
set behave_cmd=%behave_cmd% --format=json --outfile=reports/json/%report_name%.json

REM Add parallel execution if enabled
if "%PARALLEL%"=="true" set behave_cmd=%behave_cmd% --processes=%WORKERS%

REM Execute tests
call :print_info "Executing: %behave_cmd%"
%behave_cmd%

if errorlevel 1 (
    call :print_error "%test_type% tests failed!"
    exit /b 1
) else (
    call :print_success "%test_type% tests completed successfully!"
    call :print_info "Report generated: reports/html/%report_name%.html"
)
goto :eof

:open_report
set report_file=reports\html\full_report.html

REM Check for specific report files
if exist "reports\html\ui_report.html" set report_file=reports\html\ui_report.html
if exist "reports\html\api_report.html" set report_file=reports\html\api_report.html
if exist "reports\html\smoke_report.html" set report_file=reports\html\smoke_report.html

if exist "%report_file%" (
    call :print_info "Opening report: %report_file%"
    start "" "%report_file%"
) else (
    call :print_error "No report found. Run tests first."
    exit /b 1
)
goto :eof

:parse_args
if "%~1"=="" goto :show_help

:parse_loop
if "%~1"=="" goto :execute_command

if "%~1"=="setup" (
    set COMMAND=setup
) else if "%~1"=="ui" (
    set COMMAND=ui
) else if "%~1"=="api" (
    set COMMAND=api
) else if "%~1"=="all" (
    set COMMAND=all
) else if "%~1"=="smoke" (
    set COMMAND=smoke
) else if "%~1"=="regression" (
    set COMMAND=regression
) else if "%~1"=="clean" (
    set COMMAND=clean
) else if "%~1"=="report" (
    set COMMAND=report
) else if "%~1"=="help" (
    set COMMAND=help
) else if "%~1"=="--headless" (
    set HEADLESS=true
) else if "%~1"=="--parallel" (
    set PARALLEL=true
) else (
    REM Handle --key=value format
    set arg=%~1
    if "!arg:~0,6!"=="--env=" (
        set TEST_ENV=!arg:~6!
    ) else if "!arg:~0,10!"=="--browser=" (
        set BROWSER=!arg:~10!
    ) else if "!arg:~0,10!"=="--workers=" (
        set WORKERS=!arg:~10!
    ) else if "!arg:~0,7!"=="--tags=" (
        set TAGS=!arg:~7!
    ) else (
        call :print_error "Unknown option: %~1"
        goto :show_help
    )
)

shift
goto :parse_loop

:execute_command
if "%COMMAND%"=="setup" (
    call :setup_framework
) else if "%COMMAND%"=="ui" (
    call :run_tests ui
) else if "%COMMAND%"=="api" (
    call :run_tests api
) else if "%COMMAND%"=="all" (
    call :run_tests all
) else if "%COMMAND%"=="smoke" (
    call :run_tests smoke
) else if "%COMMAND%"=="regression" (
    call :run_tests regression
) else if "%COMMAND%"=="clean" (
    call :clean_up
) else if "%COMMAND%"=="report" (
    call :open_report
) else if "%COMMAND%"=="help" (
    call :show_help
) else (
    call :print_error "Unknown command: %COMMAND%"
    call :show_help
    exit /b 1
)

goto :eof