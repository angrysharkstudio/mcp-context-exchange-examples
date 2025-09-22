@echo off
REM Run the MCP Context Exchange Example on Windows

echo MCP Context Exchange Example
echo ============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found
    echo Please copy .env.example to .env and add your API keys
    echo.
    echo Example:
    echo   copy .env.example .env
    echo   notepad .env
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import anthropic" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    
    REM Check if uv is available
    where uv >nul 2>&1
    if errorlevel 1 (
        echo uv not found, using pip...
        pip install -r requirements.txt
    ) else (
        echo Using uv to install dependencies...
        uv pip install --system anthropic openai google-generativeai python-dotenv aiohttp tenacity
    )
    echo.
)

REM Run the example
echo Running the example...
echo.
python research_assistant.py %1

echo.
echo Example completed!
pause