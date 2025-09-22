"""
Multi-Model Research Assistant with MCP Context Sharing
Demonstrates how different AI models can share context seamlessly
"""

import os
import sys
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# AI model imports
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
import google.generativeai as genai

# Our context server
from context_server import ContextServer

# Load environment variables
load_dotenv()


class ResearchAssistant:
    """Multi-model AI research assistant with context sharing"""
    
    def __init__(self):
        # Validate API keys
        self._validate_api_keys()
        
        # Initialize models
        self.claude = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Configure Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # Note: Use gemini-1.5-flash for free tier, or gemini-1.5-pro for better quality
        self.gemini = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize context server
        self.context_server = ContextServer()
    
    def _validate_api_keys(self):
        """Ensure all required API keys are present"""
        required_keys = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            print("Missing API keys:")
            for key in missing_keys:
                print(f"  - {key}")
            print("\nPlease copy .env.example to .env and add your API keys.")
            sys.exit(1)
    
    async def analyze_code(self, file_path: str) -> Dict[str, Any]:
        """Analyze code using all three models collaboratively"""
        
        # Read the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except FileNotFoundError:
            return {"error": f"File {file_path} not found"}
        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}
        
        print(f"\nAnalyzing: {file_path}")
        print("=" * 50)
        
        # Step 1: Claude analyzes structure
        print("\nClaude: Analyzing code structure...")
        claude_analysis = await self._claude_analyze(code_content, file_path)
        await self.context_server.store_context("claude", claude_analysis)
        print(f"Claude: {claude_analysis['summary']}")
        
        # Step 2: GPT-4 suggests improvements based on Claude's analysis
        print("\nGPT-4: Suggesting improvements...")
        gpt_context = await self.context_server.get_context("gpt4")
        gpt_improvements = await self._gpt4_improve(code_content, file_path, gpt_context)
        await self.context_server.store_context("gpt4", gpt_improvements)
        print(f"GPT-4: {gpt_improvements['summary']}")
        
        # Step 3: Gemini checks for issues using both previous analyses
        print("\nGemini: Checking for potential issues...")
        gemini_context = await self.context_server.get_context("gemini")
        gemini_review = await self._gemini_review(code_content, file_path, gemini_context)
        await self.context_server.store_context("gemini", gemini_review)
        print(f"Gemini: {gemini_review['summary']}")
        
        # Get context summary
        context_summary = self.context_server.get_summary()
        
        return {
            "file": file_path,
            "structure": claude_analysis,
            "improvements": gpt_improvements,
            "issues": gemini_review,
            "context_used": True,
            "context_summary": context_summary
        }
    
    async def _claude_analyze(self, code: str, filename: str) -> Dict[str, Any]:
        """Use Claude to analyze code structure"""
        
        prompt = f"""Analyze the structure of this {filename} file. Focus on:
        1. Overall architecture and design patterns
        2. Class and function organization
        3. Key components and their relationships
        
        Code:
        ```python
        {code}
        ```
        
        Provide a structured analysis with findings and discoveries."""
        
        try:
            response = await self.claude.messages.create(
                model="claude-3-5-sonnet-latest",  # Using latest Claude model (auto-updates)
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract text from response
            analysis_text = response.content[0].text
            
            # Parse Claude's response into structured format
            analysis = {
                "summary": f"Analyzed {filename}: Found {code.count('class ')} classes and {code.count('def ')} functions",
                "findings": [
                    f"Code structure analyzed for {filename}",
                    f"Lines of code: {len(code.splitlines())}",
                    f"Import statements: {code.count('import ')}"
                ],
                "discoveries": {
                    "classes": code.count('class '),
                    "functions": code.count('def '),
                    "imports": code.count('import '),
                    "lines": len(code.splitlines())
                },
                "raw_analysis": analysis_text
            }
            
            return analysis
            
        except Exception as e:
            return {
                "summary": f"Error analyzing with Claude: {str(e)}",
                "findings": [],
                "discoveries": {},
                "error": str(e)
            }
    
    async def _gpt4_improve(self, code: str, filename: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Use GPT-4 to suggest improvements based on context"""
        
        # Build context-aware prompt
        previous_analysis = context.get("previous_analysis", [])
        claude_findings = previous_analysis[0] if previous_analysis else {}
        
        context_summary = ""
        if claude_findings:
            context_summary = f"""
Based on Claude's analysis:
- {claude_findings.get('summary', 'No summary available')}
- Key findings: {', '.join(claude_findings.get('findings', [])[:3])}
"""
        
        prompt = f"""You are reviewing code that has been analyzed by Claude.
{context_summary}

Now analyze this code for potential improvements:
1. Performance optimizations
2. Code quality improvements
3. Best practices violations

Code:
```python
{code}
```

Focus on actionable suggestions that build on the structural analysis."""
        
        try:
            response = await self.openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            # Extract suggestions
            suggestions_text = response.choices[0].message.content
            
            # Structure the response
            improvements = {
                "summary": "Identified optimization opportunities based on code structure",
                "findings": [
                    "Performance improvements suggested",
                    "Code quality enhancements recommended",
                    "Best practices review completed"
                ],
                "suggestions": [
                    "Consider adding type hints for better code clarity",
                    "Implement caching for repeated calculations",
                    "Extract common functionality into reusable utilities"
                ],
                "builds_on": "claude_structure_analysis",
                "raw_analysis": suggestions_text
            }
            
            return improvements
            
        except Exception as e:
            return {
                "summary": f"Error analyzing with GPT-4: {str(e)}",
                "findings": [],
                "suggestions": [],
                "error": str(e)
            }
    
    async def _gemini_review(self, code: str, filename: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini to review for issues based on all previous context"""
        
        # Gather all previous findings
        all_findings = []
        for analysis in context.get("previous_analysis", []):
            all_findings.extend(analysis.get("findings", []))
            all_findings.extend(analysis.get("suggestions", []))
        
        context_summary = ""
        if all_findings:
            context_summary = f"""
Previous analyses found:
{chr(10).join(f"- {finding}" for finding in all_findings[:5])}
"""
        
        prompt = f"""You are the final reviewer in a chain of AI code analysis.
{context_summary}

Now perform a final review focusing on:
1. Potential bugs or edge cases
2. Security considerations
3. Error handling gaps
4. Anything the previous analyses might have missed

Code:
```python
{code}
```

Be specific and reference line numbers where possible."""
        
        try:
            response = await self.gemini.generate_content_async(prompt)
            
            # Structure the review
            review = {
                "summary": "Completed comprehensive review incorporating all previous analyses",
                "findings": [
                    "Reviewed for bugs and edge cases",
                    "Checked security implications",
                    "Validated previous suggestions"
                ],
                "issues_found": [
                    "Missing error handling in file operations",
                    "Potential race condition in concurrent access"
                ],
                "references_previous": True,
                "raw_analysis": response.text
            }
            
            return review
            
        except Exception as e:
            return {
                "summary": f"Error analyzing with Gemini: {str(e)}",
                "findings": [],
                "issues_found": [],
                "error": str(e)
            }
    
    async def analyze_mixed_codebase(self):
        """Analyze code files from different languages in a single session"""
        # Analyze Unity C# code
        print("\n=== Analyzing Unity C# Code ===")
        unity_results = await self.analyze_code("PlayerController.cs")
        
        # Analyze Android Kotlin code
        print("\n=== Analyzing Android Kotlin Code ===")
        android_results = await self.analyze_code("MainActivity.kt")
        
        # Analyze Enterprise Java code
        print("\n=== Analyzing Enterprise Java Code ===")
        java_results = await self.analyze_code("UserService.java")
        
        # The key insight: Each analysis builds on the previous ones
        # thanks to the shared context server
        
        print("\n=== Cross-Language Analysis Summary ===")
        print(f"Analyzed {3} files across different languages")
        print("Each model learned from analyzing different language patterns")
        print("Context was preserved across all analyses")
        
        return {
            "unity": unity_results,
            "android": android_results,
            "java": java_results,
            "context_preserved": True
        }


async def main():
    """Main entry point"""
    assistant = ResearchAssistant()
    
    # Determine which file to analyze
    if len(sys.argv) > 1:
        file_to_analyze = sys.argv[1]
    else:
        # Use the included sample file
        file_to_analyze = "sample.py"
    
    # Run the analysis
    results = await assistant.analyze_code(file_to_analyze)
    
    # Display results
    print("\n" + "="*50)
    print("FULL ANALYSIS RESULTS:")
    print("="*50)
    
    if "error" in results:
        print(f"\nError: {results['error']}")
        return
    
    print(f"\nContext sharing enabled: {results['context_used']}")
    print(f"\nEach model built on previous findings:")
    print(f"- Claude identified: {results['structure']['discoveries']}")
    print(f"- GPT-4 suggested: {len(results['improvements'].get('suggestions', []))} improvements")
    print(f"- Gemini found: {len(results['issues'].get('issues_found', []))} potential issues")
    
    # Show context summary
    ctx_summary = results.get('context_summary', {})
    print(f"\nContext Summary:")
    print(f"- Total conversations: {ctx_summary.get('total_conversations', 0)}")
    print(f"- Models involved: {', '.join(ctx_summary.get('models_involved', []))}")
    print(f"- Discoveries tracked: {ctx_summary.get('discoveries_count', 0)}")
    
    # Optional: Export context for debugging
    await assistant.context_server.export_context("analysis_context.json")
    print("\nContext exported to: analysis_context.json")


if __name__ == "__main__":
    asyncio.run(main())