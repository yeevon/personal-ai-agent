# AI Agent

A terminal-based agentic AI assistant powered by Google Gemini, capable of autonomously exploring codebases, reading and writing files, and running commands to complete user-defined tasks.

### Warning this is practice project, use at your own risk

---

## What It Does

The agent accepts a natural language prompt from the command line and enters an autonomous loop, using a set of tools to fulfill the request. It continues calling tools and reasoning over results until it can provide a final answer.

## Current Features

### Agentic Loop

    - Runs up to 20 iterations autonomously to complete a task
    - Stops when no more function calls are needed and returns a final response
    - Gracefully handles empty or null candidate responses from the model

### Tool / Function Calling

    - get_files_info — lists files in a directory with size and type metadata
    - get_file_content — reads and returns the contents of a file
    - write_file — writes or overwrites a file with given content
    - run_python — executes a Python script and returns stdout/stderr

### CLI Interface

    - Accepts a user prompt as a positional argument
    - --verbose flag to display token usage and function call results

### Model

    - Powered by gemini-2.5-flash
    - Temperature set to 0 for deterministic, reliable tool use
    - System prompt configurable via system_prompt.py

---

## Usage

```bash
uv run main.py "Explain how the calculator renders the result to the console."

uv run main.py "Write hello to main.txt" --verbose
```

---

## Known Issues

- **`main.py:43`** — `response.function_calls` accessed without null check; can cause a runtime crash if candidates exist but no function calls are returned
- **`calculator/pkg/calculator.py:9`** — division by zero is unhandled; crashes instead of returning a graceful error message
- **`functions/get_file_content.py:24`** / **`functions/write_to_file.py:18`** — `open()` calls missing `encoding='utf-8'`; may break on non-UTF-8 systems
- **`functions/run_python_files.py:14`** — `.py` extension check uses `[-3:]` string slice instead of `.endswith('.py')`
- **`main.py:72`** — model name `'gemini-2.5-flash'` hardcoded; should live in `config.py`
- **`main.py:26`** — agent loop limit (20) hardcoded; should live in `config.py`
- **Multiple function files** — broad `except Exception` used throughout; masks specific errors and makes debugging harder

---

## Roadmap

### 1. Local Ollama Support

Replace the Google Gemini backend with a locally running Ollama instance, enabling fully offline operation with self-hosted models.

    - Swap google-genai client for Ollama’s OpenAI-compatible API
    - Configurable model selection (e.g. llama3, mistral, deepseek)
    - No API key required, runs entirely on your machine

### 2. Agent Memory via SQL

Give the agent a persistent “brain” by logging all conversations to a local SQL database, allowing it to reference past interactions and build context over time.

    - Store prompts, responses, and tool calls per session
    - Inject relevant past context into new requests
    - Query history by date, topic, or session ID
    - Enables learning from previous mistakes and decisions

### 3. Conversational UI

Build a proper interface for continuous back-and-forth conversation with the agent, replacing the single-prompt CLI model.

    - Web-based chat UI or terminal TUI (e.g. Textual)
    - Persistent conversation thread with scroll history
    - Real-time streaming of agent responses and tool calls
    - Session management — start, resume, and name conversations
