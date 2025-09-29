## MCP Tic-Tac-Toe Project
In this project you will develop a Model Context Protocol (MCP) server that lets an LLM interact with a simple Tic‑Tac‑Toe game. The assignment is broken into parts; complete each part in order and ensure the result behaves sensibly before moving on.

Learn about MCP here: [Model Context Protocol](https://github.com/modelcontextprotocol). Focus on the Python SDK only.

## Prerequisites
- **Python**: Use Python 3.11 or newer.
- **Anthropic API key**: You will receive an API key for the Anthropic API.
- **Virtual environment (optional)**: Recommended for local development.

## Setup
Install the sources in editable mode and the helper tool:

```bash
pip install -e . mcp-use
```

## Assignment Parts

### Part 1: MCP stdio server
Implement an MCP stdio server that manages Tic‑Tac‑Toe state in `main.py`. It must support:
- **New game**
- **Show board** (include who plays next; or, if over, the winner if any)
- **Play move**

You should be able to test by piping JSON to the server:

```bash
echo '<JSON request>' | python main.py
```

Important: implement this as an MCP stdio server (not HTTP).

### Part 2: Test script
Create a script that simulates a full interaction sequence with your server, exercising all functions:
- **Play a complete game** through to the end
- **Print** all interactions
- **Assert** the final state matches expectations

Provide an executable script `run_test.sh` to run the tests. If you implement tests in `test.py`, the script can be as simple as:

```bash
python test.py
```

### Part 3: MCP client to play
Use your MCP server with an LLM so a user can play the game against the LLM. Start with the provided chat script:

```bash
ANTHROPIC_API_KEY=<key> python python/chat.py
```

Modify `chat.py` so the user can play the game against the LLM. The script is set up to use Claude Haiku. Update the implementation and system prompt so it plays exactly **one turn** with the user. It should either play its own turn or apply the user's move for that turn and display the result. Commit an example invocation script `send_messages.sh`.

### Part 4: Server persistence
Currently, state resets each time the client runs. Add persistence so game state survives across invocations:
- **Save state** to a file after each operation
- **Play through to the end** against the LLM
- Commit a script `play_game.sh` showing a full sequence of turns

## Document your work
To help evaluate your work, include the following in the repository:
- **What you used**: documentation and tools referenced during development
- **How you tested**: command lines and scripts used for debugging and tests
- **Evidence**: logs or outputs that show things working
- **Commit history**: multiple commits that capture incremental progress

You may add Markdown files, temporary scripts, and logs to the repo. Keep the implementation in Python. Shell scripts are fine to document Python invocations.

## Expected outcome
All work should be committed to the provided repository. Include a `SOLUTION.md` with:
- **Test details** and how to run them (and any scripts created)
- **How AI tools were used**, and which code was AI‑assisted
- Ideally, commit messages that note when a substantial portion was AI‑generated

## Evaluation criteria
| Criteria | Description |
| --- | --- |
| Working scripts | Scripts that can run the implemented code |
| Use of AI | Effective use of AI to achieve the goal |
| Quality of code | Subjective assessment of implementation quality |
| Documentation | Clear explanation of the problem and a step‑by‑step solution |