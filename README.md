# MCP Context Exchange Examples

This directory contains working examples for the blog post "How MCP Handles Context Exchange Between AI Models".

## Overview

This example demonstrates how to use the Model Context Protocol (MCP) to share context between three different AI models:
- **Claude**: Analyzes code structure and architecture
- **GPT-4**: Suggests improvements and optimizations
- **Gemini**: Double-checks for bugs and edge cases

Each model builds on the previous one's analysis without requiring manual copy-paste of context.

## Prerequisites

- Python 3.8 or higher
- API keys for:
  - Anthropic (Claude)
  - OpenAI (GPT-4)
  - Google AI (Gemini)

## Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
run_example.bat
```

**Mac/Linux:**
```bash
chmod +x run_example.sh
./run_example.sh
```

The scripts handle everything automatically - checking Python version, installing dependencies, verifying your API keys, and running the example.

### Option 2: Manual Setup

1. **Clone or download this example directory**

2. **Install dependencies:**

   Using UV (faster, recommended):
   ```bash
   # Install uv first if you don't have it
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install dependencies
   uv pip install --system anthropic openai google-generativeai python-dotenv aiohttp tenacity
   ```

   Using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API keys:
   - `ANTHROPIC_API_KEY` - [Get from Anthropic Console](https://console.anthropic.com/)
   - `OPENAI_API_KEY` - [Get from OpenAI Platform](https://platform.openai.com/api-keys)
   - `GOOGLE_API_KEY` - [Get from Google AI Studio](https://makersuite.google.com/app/apikey)

## Running the Example

### Basic Usage

```bash
python research_assistant.py
```

This will analyze the included `sample.py` file using all three AI models.

### Analyzing Your Own Code

```bash
python research_assistant.py your_file.py
```

### Interactive Jupyter Notebook

For a more interactive experience with visualizations:
```bash
jupyter notebook mcp-context-exchange-demo.ipynb
```

## What Happens

1. **Claude** analyzes the code structure, counting classes, functions, and understanding the architecture
2. **GPT-4** receives Claude's analysis and suggests improvements based on that context
3. **Gemini** gets both previous analyses and looks for bugs or edge cases they might have missed

The key point: each model automatically receives the context from previous models through the MCP context server.

## Example Output

```
Claude: Analyzing code structure...
Claude: Found 1 classes and 3 functions

GPT-4: Suggesting improvements...
GPT-4: Identified optimization opportunities based on code structure

Gemini: Checking for potential issues...
Gemini: Completed comprehensive review incorporating all previous analyses

==================================================
FULL ANALYSIS RESULTS:
==================================================

Context sharing enabled: True

Each model built on previous findings:
- Claude identified: {'classes': 1, 'functions': 3, 'imports': 0}
- GPT-4 suggested: 3 improvements
- Gemini found: 2 potential issues
```

## Files in This Example

### Core Python Files
- `context_server.py` - The MCP server that manages context between models
- `research_assistant.py` - The main application that orchestrates the three AI models
- `sample.py` - A sample Python file to analyze (with intentional issues)
- `pyproject.toml` - Project configuration and dependencies
- `.env.example` - Template for environment variables

### Multi-Language Code Examples
The MCP system can analyze code written in ANY language. We include examples in:
- `PlayerController.cs` - Unity C# code with performance issues
- `MainActivity.kt` - Android Kotlin code with coroutine and null safety issues
- `UserService.java` - Enterprise Java code with concurrency issues

To analyze these files:
```python
# Analyze C# Unity code
python research_assistant.py PlayerController.cs

# Analyze Kotlin Android code
python research_assistant.py MainActivity.kt

# Analyze Java Enterprise code
python research_assistant.py UserService.java
```

## Customization

You can modify the example to:
- Add more AI models
- Change what each model focuses on
- Store context in a database instead of memory
- Add a web interface

## Troubleshooting

### Import Errors
Make sure you've installed all dependencies:
```bash
# Using UV
uv pip install anthropic openai google-generativeai python-dotenv aiohttp tenacity

# Using pip
pip install -r requirements.txt
```

### API Key Errors
- Ensure your `.env` file exists and contains valid API keys
- Check that the API keys have the necessary permissions
- Verify you have credits/quota for each service

### Rate Limiting
The example includes basic retry logic, but you may hit rate limits with frequent use. Consider adding delays between API calls if needed.

### Gemini Model Errors
If you see "models/gemini-pro is not found" or similar:
- Google updates their model names periodically
- Current working models: `gemini-1.5-flash` (free) or `gemini-1.5-pro` (paid)
- Check available models at: https://ai.google.dev/gemini-api/docs/models/gemini
- Update the model name in `research_assistant.py` line 39

## Learn More

For a detailed explanation of how this works, read the full blog post:
[How MCP Handles Context Exchange Between AI Models](https://angry-shark-studio.com/blog/mcp-context-exchange-ai-models)

## Contributing

Found an issue or want to contribute? Visit our GitHub repository:
[github.com/angrysharkstudio/mcp-context-exchange-examples](https://github.com/angrysharkstudio/mcp-context-exchange-examples)

## License

MIT License - see the LICENSE file for details.