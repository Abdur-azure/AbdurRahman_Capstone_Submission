# CloudServe Capstone – Intelligent Customer Support System

Forward Deployed AI Engineering Capstone Project  
An intelligent support system for CloudServe Solutions.

## Overview
This project builds a production-style customer support automation system that classifies tickets, retrieves relevant documentation, generates grounded answers with citations, applies guardrails, and logs every decision.

## Prerequisites
- Python 3.10 or higher
- Git

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
    ```bash
   python -m venv .venv
   # Windows
   .venv\\Scripts\\activate
   # macOS / Linux
   source .venv/bin/activate
    ```
3. Install dependencies:
    ```Bash
    pip install -r requirements.txt
    ```
4. Create a .env file in the root and add your API key:
    ```text
    GROQ_API_KEY=your_key_here(or OPENROUTER_API_KEY=...)
    ```
## Running the System(Commands will be added as the system is built)

## Evaluation Harness
    (The single unattended command that processes the full validation set will be documented here – required for Acceptance Criterion A9/A10)
    
## Project Structure
    ```text
    src/          # Main application code
    data/         # Tickets and documentation
    tests/        # Test suite
    scripts/      # Utility and evaluation scripts
    ```

## Notes
- Embeddings use the local model all-MiniLM-L6-v2
- LLM access is configured via environment variables (free-tier providers only)
- No credentials are stored in the repository