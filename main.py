from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

class TicTacToe:
  def __init__(self):
    self.board = [[" " for _ in range(3)] for _ in range(3)]
    self.current_player = "X"
    self.winner = None
    self.game_over = False
  
  def show_board(self):
    self.winner = self.check_winner()
    self.game_over = self.is_game_over()

    board_str = "Current board:\n"
    for i, row in enumerate(self.board):
      board_str += f"{i}: {' | '.join(row)}\n"
    
    if self.game_over:
      if self.winner != None:
        board_str += f"Winner: {self.winner}"
      else: 
        board_str += "Draw"
      return board_str

    board_str += f"Current player: {self.current_player}"
    return board_str

  def reset_game(self):
    self.board = [[" " for _ in range(3)] for _ in range(3)]
    self.current_player = "X"
    self.winner = None
    self.game_over = False
    return self.get_state()
  
  def check_winner(self):
    for row in self.board:
      if row.count(row[0]) == 3 and row[0] != " ":
        return row[0]
    for col in range(3):
      if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
        return self.board[0][col]
    if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
      return self.board[0][0]
    if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
      return self.board[0][2]
    return None
  
  def check_draw(self):
    return all(cell != " " for row in self.board for cell in row)
  
  def is_game_over(self):
    return self.winner is not None or self.check_draw()
  
  def get_state(self):
    return {
      "board": self.board,
      "current_player": self.current_player,
      "winner": self.winner,
      "game_over": self.game_over
    }
  
  def play_move(self, row, col):
    self.board[row][col] = self.current_player
    self.current_player = "O" if self.current_player == "X" else "X"
    self.winner = self.check_winner()
    self.game_over = self.is_game_over()
    return self.get_state()

class PlayMoveInput(BaseModel):
  row: int
  col: int

# Create an MCP server
mcp = FastMCP("Tic-Tac-Toe")
ttt = TicTacToe()

@mcp.tool("reset_game")
def reset_game():
  return ttt.reset_game()

@mcp.tool("show_board")
def show_board():
  return ttt.show_board()

@mcp.tool("get_state")
def get_state():
  return ttt.get_state()

@mcp.tool("play_move")
def play_move(input: PlayMoveInput):
  return ttt.play_move(input.row, input.col)

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

def handle_json_request():
  """Handle JSON requests from stdin"""
  import json
  import sys
  
  try:
    # Read JSON from stdin
    input_data = json.loads(sys.stdin.read())
    tool_name = input_data.get("tool")
    args = input_data.get("args", {})
    
    # Route to appropriate function
    if tool_name == "play_move":
      result = ttt.play_move(args["row"], args["col"])
    elif tool_name == "show_board":
      result = ttt.show_board()
    elif tool_name == "get_state":
      result = ttt.get_state()
    elif tool_name == "reset_game":
      result = ttt.reset_game()
    elif tool_name == "greet_user":
      result = greet_user(args.get("name", "User"), args.get("style", "friendly"))
    else:
      result = {"error": f"Unknown tool: {tool_name}"}
    
    # Return JSON response
    print(json.dumps(result, indent=2))
    
  except json.JSONDecodeError:
    print(json.dumps({"error": "Invalid JSON input"}, indent=2))
  except KeyError as e:
    print(json.dumps({"error": f"Missing required parameter: {e}"}, indent=2))
  except Exception as e:
    print(json.dumps({"error": f"Error: {str(e)}"}, indent=2))

if __name__ == "__main__":
  import sys
  
  # Check if we're running as MCP server or JSON CLI
  if len(sys.argv) > 1 and sys.argv[1] == "--mcp":
    print("Starting Tic-Tac-Toe MCP server...")
    mcp.run_stdio()
  else:
    # Handle JSON request from stdin
    handle_json_request()