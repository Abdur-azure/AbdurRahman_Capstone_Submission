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
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
    ```

3. Install dependencies:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. Create a .env file in the root and add your API key:

    ```bash
    # Windows
    copy .env.example .env
    # macOS / Linux
    cp .env.example .env

    GROQ_API_KEY=your_key_here(or OPENROUTER_API_KEY=...)
    ```

## Running the System

1. Place ticket and documentation JSON files in `data/`.
2. Build the retrieval index (first run only):

   ```bash
   python -c "from src.retriever import DocumentRetriever; DocumentRetriever().build_index()"
   ```
3. Process tickets via the evaluation harness (see below).


## Evaluation Harness

1. Single unattended command (Acceptance Criteria A9/A10):

    ```bash
    python -m scripts.run_evaluation --input data/validation_tickets.json --output outputs/validation_report.json 
    --threshold 0.65 ##optional
    ```

- Writes a metrics report to the given output path
- Appends one decision record per ticket to logs/decisions.jsonl
- Log entry count must match the number of tickets processed
    
## Kill Switch

- Set in .env (or environment):

    ```text
    AUTO_RESPOND=false
    ```

## Project Structure

    ```text
    src/           # Application code (pipeline, classifier, retriever, generator, guardrails, logger)
    scripts/       # Evaluation harness and test helpers
    data/          # Tickets and documentation JSON
    logs/          # Decision log (JSONL)
    outputs/       # Evaluation reports
    tests/         # Tests
    ```

## Notes

- Embeddings use the local model all-MiniLM-L6-v2
- LLM access is configured via environment variables (free-tier providers only)
- No credentials are stored in the repository