#!/bin/bash
# Run the MCP Context Exchange Example on Unix/Linux/Mac

echo "MCP Context Exchange Example"
echo "============================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python $python_version is installed, but version $required_version or higher is required"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Please copy .env.example to .env and add your API keys"
    echo
    echo "Example:"
    echo "  cp .env.example .env"
    echo "  nano .env  # or use your preferred editor"
    exit 1
fi

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "Using uv for dependency management..."
    
    # Check if dependencies are installed
    if ! python3 -c "import anthropic" &> /dev/null; then
        echo "Installing dependencies with uv..."
        uv pip install --system anthropic openai google-generativeai python-dotenv aiohttp tenacity
        echo
    fi
else
    # Fall back to regular pip with venv
    echo "uv not found, using standard pip..."
    
    # Check if virtual environment exists, create if not
    if [ ! -d venv ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Check if dependencies are installed
    if ! python -c "import anthropic" &> /dev/null; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
        echo
    fi
fi

# Run the example
echo "Running the example..."
echo

if [ -z "$1" ]; then
    python research_assistant.py
else
    python research_assistant.py "$1"
fi

echo
echo "Example completed!"