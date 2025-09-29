from anthropic import Anthropic

ANTHROPIC_MODEL = "claude-3-5-sonnet-latest"  
HUMAN_PLAYS = "X"
MODEL_PLAYS = "O" if HUMAN_PLAYS == "X" else "X"

import asyncio, os
from mcp import StdioServerParameters, stdio_client, ClientSession

MCP_SERVER_CMD = "uv"
MCP_SERVER_ARGS = ["run", "python", "main.py", "--mcp"]

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class MCPClient:
  def __init__(self, command=MCP_SERVER_CMD, args=MCP_SERVER_ARGS):
    self.server_params = StdioServerParameters(
      command=command, 
      args=args, 
      env={**os.environ, "PYTHONUNBUFFERED": "0", "MCP_LOG_LEVEL": "ERROR"})
    self._ctx = None
    self.session = None

  async def start(self):
    try: 
      # Store context managers for later cleanup
      self._ctx = stdio_client(self.server_params)
      read, write = await self._ctx.__aenter__()
      
      self.session = ClientSession(read, write) 
      await self.session.__aenter__()
      
      await self.session.initialize()
      print("✅ Connected!")
      return True
    except Exception as e:
      print(f"❌ Connection failed: {e}")
      return False

  async def list_tools(self):
    if not self.session:
      print("No session found")
      return None
    try:
      tools = await self.session.list_tools()
      print(f"Tools: {tools}")
      return tools
    except Exception as e:
      print(f"Error listing tools: {e}")
      return None
    
  async def call_tool(self, tool_name, args):
    if not self.session:
      print("No session found")
      return None
    try:
      result = await self.session.call_tool(name=tool_name, arguments=args or {})
      return result
    except Exception as e:
      print(f"Error calling tool: {e}")
      return None
  
  async def close(self):
    try:
      if self.session:
        await self.session.__aexit__(None, None, None)
      if self._ctx:
        await self._ctx.__aexit__(None, None, None)
    except Exception as e:
      print(f"Error closing client: {e}")
      return None
  
   # Game-specific convenience methods (now async)
  async def play_move(self, row, col):
    """Make a move on the board"""
    result = await self.call_tool("play_move", {"input": {"row": row, "col": col}})
    return result.content if result else None
  
  async def show_board(self):
    """Get board display"""
    result = await self.call_tool("show_board", {})
    return result.content if result else None
  
  async def get_state(self):
    """Get game state"""
    result = await self.call_tool("get_state", {})
    return result.content if result else None

  async def reset_game(self):
    """Reset the game"""
    result = await self.call_tool("reset_game", {})
    return result.content if result else None
