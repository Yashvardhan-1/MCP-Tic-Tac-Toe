# 🎮 AI Tic-Tac-Toe with MCP & Claude

> Play Tic-Tac-Toe against Claude AI using the Model Context Protocol (MCP)

An intelligent Tic-Tac-Toe game where you battle against Anthropic's Claude AI. Built with FastMCP for seamless AI-to-game communication and strategic gameplay.

## ✨ Features

- 🤖 **AI Opponent**: Play against Claude Sonnet with strategic thinking
- 🎯 **MCP Architecture**: Clean separation between game logic and AI
- 🔄 **Real-time Updates**: Live board state management
- 🛡️ **Type Safety**: Pydantic models for data validation
- 🎨 **Clean UI**: Beautiful terminal interface with emojis
- 🔐 **Secure**: Environment-based API key management

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   chat.py   │ ◄─────► │  client.py   │ ◄─────► │  main.py    │
│  (Game)     │         │ (MCP Client) │         │ (MCP Server)│
└─────────────┘         └──────────────┘         └─────────────┘
       │                                                  │
       │                                                  │
       ▼                                                  ▼
┌─────────────┐                                  ┌─────────────┐
│ Anthropic   │                                  │ Game Logic  │
│   Claude    │                                  │ (TicTacToe) │
└─────────────┘                                  └─────────────┘
```

## 📋 Prerequisites

- **Python 3.11+**
- **uv** (Python package manager)
- **Anthropic API Key** ([Get one here](https://console.anthropic.com/))

## 🚀 Setup

### 1. Install Dependencies

```bash
cd mcp-ttt

# Install all dependencies using uv
uv sync
```

### 2. Configure API Key

Create a `.env` file in the `mcp-ttt` directory:

```bash
# Create .env file
touch .env

# Add your API key (replace with your actual key)
export 'ANTHROPIC_API_KEY=sk-ant-api03-your-actual-api-key-here'
```

## 🧪 Testing

### Test 1: MCP Server (Game Logic)

Test the MCP server independently to verify game logic:

```bash
# Run the MCP server in test mode
uv run python main.py --mcp

# In another terminal, you can test with JSON inputs
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python main.py --mcp
```

### Test 2: MCP Client Connection

Test the client-server connection:

```bash
# Run the client test suite
uv run python test_client.py
```

**Expected Output:**
```
🧪 Testing MCP Client...
✅ Connected!

1️⃣ Testing reset_game...
🔍 Reset Result:
{
  "board": [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
  ],
  "current_player": "X",
  "winner": null,
  "game_over": false
}

2️⃣ Testing show_board...
🔍 Board:
Current board:
0:   |   |  
1:   |   |  
2:   |   |  
Current player: X

✅ All tests completed!
```

### Test 3: Utility Functions

Test the helper utilities:

```bash
# Test JSON parsing and extraction
uv run python -c "from utils import extract_result_text; print(extract_result_text({'text': '{\"test\": true}'}))"
```

## 🎮 Playing the Game

### Start a New Game

```bash
uv run python chat.py
```

### Gameplay

1. **Board Display**: The board shows rows (0-2) and columns (0-2)
   ```
   Current board:
   0:   |   |  
   1:   | X |  
   2:   |   |  
   Current player: O
   ```

2. **Your Turn** (You play as 'X'):
   ```
   👤 Your turn!
   Enter the row (0-2): 1
   Enter the column (0-2): 1
   ```

3. **AI Turn** (Claude plays as 'O'):
   ```
   🤖 AI's turn!
   🤖 O is thinking...
   🤖 Claude says: 0,0
   🎯 O chooses position (0,0)
   ```

4. **Game End**: The game ends when someone wins or it's a draw
   ```
   Player X wins!
   🏁 Game over!
   ```

### Game Controls

- **Input Format**: Enter row and column as numbers 0-2
- **Board Positions**:
  ```
  (0,0) | (0,1) | (0,2)
  ------+-------+------
  (1,0) | (1,1) | (1,2)
  ------+-------+------
  (2,0) | (2,1) | (2,2)
  ```
- **Exit**: Press `Ctrl+C` to quit at any time

## 🔧 Development

### Project Structure

```
mcp-ttt/
├── chat.py              # Main game interface & AI integration
├── client.py            # MCP client for server communication
├── main.py              # MCP server & game logic
├── utils.py             # Helper functions (JSON parsing, etc.)
├── test_client.py       # Client integration tests
├── .env                 # API keys (DO NOT COMMIT)
├── .gitignore           # Git ignore rules
├── pyproject.toml       # Project dependencies
└── README.md            # This file
```

### Key Components

#### `main.py` - MCP Server
- **TicTacToe Class**: Core game logic
- **FastMCP Tools**: Exposed game operations
  - `play_move`: Make a move on the board
  - `show_board`: Display current board
  - `get_state`: Get full game state
  - `reset_game`: Start new game

#### `client.py` - MCP Client
- **MCPClient Class**: Manages server connection
- **Async Operations**: Non-blocking communication
- **Type-Safe**: Returns validated data structures

#### `chat.py` - Game Interface
- **Game Class**: Main game orchestration
- **AI Integration**: Claude strategic gameplay
- **User Interface**: Terminal-based interaction

## 🎯 AI Strategy

Claude's decision-making priorities:

1. **🏆 Win**: Take winning move if available
2. **🛡️ Block**: Prevent opponent from winning
3. **🎯 Center**: Control the center (1,1)
4. **📐 Corners**: Secure corner positions
5. **➡️ Edges**: Fill remaining edge positions

## 🐛 Troubleshooting

### Issue: `Import "mcp" could not be resolved`

**Solution**: Ensure you're in the correct directory and dependencies are installed
```bash
cd mcp-ttt
uv sync
```

### Issue: `ANTHROPIC_API_KEY not found`

**Solution**: Create and configure your `.env` file
```bash
echo 'ANTHROPIC_API_KEY=your-key-here' > .env
```

### Issue: `Connection to MCP server failed`

**Solution**: Verify the server can start independently
```bash
uv run python main.py --mcp
```

### Issue: `Game state validation errors`

**Solution**: Ensure all dependencies are up to date
```bash
uv sync --upgrade
```

## 📊 Example Game Session

```bash
$ uv run python chat.py

✅ Connected!
Current board:
0:   |   |  
1:   |   |  
2:   |   |  
Current player: X

👤 Your turn!
Enter the row (0-2): 1
Enter the column (0-2): 1

🤖 AI's turn!
🤖 O is thinking...
🤖 Claude says: 0,0
🎯 O chooses position (0,0)

Current board:
0: O |   |  
1:   | X |  
2:   |   |  
Current player: X

👤 Your turn!
Enter the row (0-2): 0
Enter the column (0-2): 2

🤖 AI's turn!
🤖 O is thinking...
🤖 Claude says: 0,1
🎯 O chooses position (0,1)

Current board:
0: O | O | X
1:   | X |  
2:   |   |  
Current player: X

👤 Your turn!
Enter the row (0-2): 2
Enter the column (0-2): 1

Player X wins!
🏁 Game over!
🔌 MCP client connection closed.
🧹 Cleanup complete.
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Submit pull requests
- 📖 Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Anthropic** - Claude AI model
- **FastMCP** - Model Context Protocol framework
- **Python Community** - Amazing tools and libraries

## 🔗 Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)

---

**Built with ❤️ using MCP and Claude**

*Have fun playing against AI! May the best player win!* 🎮✨

