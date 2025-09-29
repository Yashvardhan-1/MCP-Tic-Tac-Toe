import asyncio
import json
import os
from anthropic import Anthropic
from client import MCPClient
from utils import extract_result_text

# Game configuration
ANTHROPIC_MODEL = "claude-3-5-sonnet-latest"
HUMAN_PLAYS = "X" 
AI_PLAYS = "O"

class Game:
  def __init__(self):
      """Initialize the game with Anthropic client and MCP client"""
      self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
      self.mcp_client = MCPClient()
      self.current_player = HUMAN_PLAYS
      self.game_history = []  # Store conversation history
      
  async def start_game(self):
      """Start a new game session"""
      await self.mcp_client.start()
      await self.mcp_client.reset_game()
  
  async def get_ai_move(self, current_board, game_state):
    """
    Get AI's next move using Anthropic model
    
    Args:
        current_board: Current board display string
        game_state: Current game state dict
        
    Returns:
        tuple: (row, col) coordinates for AI's move
    """
    try:
      # Create the strategic prompt for Claude
      prompt = self.format_claude_prompt(current_board, game_state, self.game_history)
      print(f"🤖 {AI_PLAYS} is thinking...")
      
      # Send request to Anthropic API
      response = await asyncio.to_thread(
        self.anthropic.messages.create,
        model=ANTHROPIC_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,  # Short response - just need coordinates
        temperature=0.7  # Some creativity but not too random
      )
      
      # Extract text from response
      if response.content and len(response.content) > 0:
        response_text = response.content[0].text
        print(f"🤖 Claude says: {response_text}")
        
        # Parse Claude's response to get coordinates
        coordinates = self.parse_ai_response(response_text)
        
        if coordinates:
            row, col = coordinates
            print(f"🎯 {AI_PLAYS} chooses position ({row},{col})")
            return coordinates
        else:
            print("⚠️ Could not understand Claude's response, trying random fallback...")
            return await self._get_random_move(game_state)
      else:
          print("⚠️ No response from Claude, trying random fallback...")
          return await self._get_random_move(game_state)
            
    except Exception as e:
      print(f"❌ Error getting AI move: {e}")
      print("🎲 Using random fallback...")
      return await self._get_random_move(game_state)
  
  async def _get_random_move(self, game_state):
    """
    Fallback: Get a random valid move when Claude fails
    
    Args:
        game_state: Current game state dict
        
    Returns:
        tuple: (row, col) coordinates for a random valid move
    """
    import random
      
    # Get available positions from the board
    board_array = game_state.get('board', [])
    available_moves = []
    
    for row in range(3):
      for col in range(3):
        if row < len(board_array) and col < len(board_array[row]):
          if board_array[row][col] == ' ':  # Empty space
            available_moves.append((row, col))

    if available_moves:
      move = random.choice(available_moves)
      print(f"🎲 Random move: ({move[0]},{move[1]})")
      return move
    else:
      print("❌ No available moves found!")
      return None
  
  async def make_human_move(self):
      """
      Get human player's move from input
      
      Returns:
          tuple: (row, col) coordinates for human's move
      """
      # Get user input for row and column
      # Validate the input (0-2 range, position available)
      # Return coordinates
      row = int(input("Enter the row (0-2): "))
      col = int(input("Enter the column (0-2): "))
      return await self.make_move(row, col)
  
  async def make_move(self, row, col):
      """
      Execute a move on the board via MCP server
      
      Args:
          row: Row index (0-2)
          col: Column index (0-2)
          
      Returns:
          dict: Updated game state or None if invalid move
      """
      # Call MCP server play_move tool
      # Handle any errors
      # Return updated state
      pass
  
  async def display_board(self):
      """Display current board state"""
      # Get board from MCP server
      # Format and print the board nicely
      board = await self.mcp_client.show_board()
      print(extract_result_text(board))
  
  async def check_game_over(self, game_state):
    """
    Check if game is over and handle end conditions
    
    Args:
        game_state: Current game state dict
        
    Returns:
        bool: True if game is over, False otherwise
    """
    game_state = await self.mcp_client.get_state()
    if game_state.get("winner"):
      print(f"Player {game_state['winner']} wins!")
      return True
    elif game_state.get("game_over"):
      print("Game over! It's a draw.")
      return True
    pass
  
  def format_claude_prompt(self, board, game_state, move_history):
    """
    Format the current game state into a prompt for Claude
    
    Args:
      board: Board display string
      game_state: Game state dict  
      move_history: List of previous moves
        
    Returns:
      str: Formatted prompt for Claude
    """
    # Extract key info from game state
    current_player = game_state.get('current_player', 'O')
    winner = game_state.get('winner')
    game_over = game_state.get('game_over', False)
    
    prompt = f"""You are playing Tic-Tac-Toe against a human opponent.
      GAME STATUS:
      {board}

      GAME RULES:
      - You are playing as '{AI_PLAYS}' (AI)
      - Human is playing as '{HUMAN_PLAYS}' 
      - Current turn: {current_player}
      - Positions are specified as row,col (both 0-2)
      - Top-left is 0,0, bottom-right is 2,2

      CURRENT BOARD STATE:
    """
    
    # Add formatted board with coordinates for clarity
    board_array = game_state.get('board', [])
    if board_array:
      prompt += "    0   1   2\n"
      for i, row in enumerate(board_array):
          prompt += f"{i} | {' | '.join(row)} |\n"
    
    # Add move history context
    if move_history:
      prompt += f"\nMOVE HISTORY:\n"
      for i, (player, row, col) in enumerate(move_history[-5:]):  # Last 5 moves
          prompt += f"{i+1}. {player} played at ({row},{col})\n"
    
    # Add strategy context based on game state
    if current_player == AI_PLAYS:
      prompt += f"""
        YOUR TURN: You need to choose your next move as '{AI_PLAYS}'.

        STRATEGY PRIORITIES:
        1. WIN: If you can win in one move, do it
        2. BLOCK: If human can win next turn, block them  
        3. CENTER: Control the center (1,1) if available
        4. CORNERS: Take corners (0,0), (0,2), (2,0), (2,2) over edges
        5. EDGES: Take remaining edge positions

        RESPONSE FORMAT:
        Reply with ONLY the coordinates in this exact format: "row,col"
        Examples: "0,1" or "2,2" or "1,0"

        Do not include any explanation, just the coordinates.

      Your move:"""
    
    else:
      prompt += f"\nIt's the human's turn ('{HUMAN_PLAYS}'). Waiting for their move..."
    
    return prompt
  
  def parse_ai_response(self, response_text):
      """
      Parse Claude's response to extract move coordinates
      
      Args:
          response_text: Claude's response string
          
      Returns:
          tuple: (row, col) or None if parsing failed
      """
      import re
      
      # Clean the response text
      text = response_text.strip().lower()
      
      # Pattern 1: Simple "row,col" format (preferred)
      pattern1 = r'(\d)\s*,\s*(\d)'
      match = re.search(pattern1, text)
      if match:
          row, col = int(match.group(1)), int(match.group(2))
          if 0 <= row <= 2 and 0 <= col <= 2:
              return (row, col)
      
      # Pattern 2: "row X, col Y" format
      pattern2 = r'row\s*(\d).*?col\s*(\d)'
      match = re.search(pattern2, text)
      if match:
          row, col = int(match.group(1)), int(match.group(2))
          if 0 <= row <= 2 and 0 <= col <= 2:
              return (row, col)
      
      # Pattern 3: "(X,Y)" format with parentheses
      pattern3 = r'\(\s*(\d)\s*,\s*(\d)\s*\)'
      match = re.search(pattern3, text)
      if match:
          row, col = int(match.group(1)), int(match.group(2))
          if 0 <= row <= 2 and 0 <= col <= 2:
              return (row, col)
      
      # Pattern 4: Just two digits anywhere in the text
      digits = re.findall(r'\d', text)
      if len(digits) >= 2:
          row, col = int(digits[0]), int(digits[1])
          if 0 <= row <= 2 and 0 <= col <= 2:
              return (row, col)
      
      # Pattern 5: Position names (e.g., "center", "top-left")
      position_map = {
          'center': (1, 1),
          'middle': (1, 1),
          'top-left': (0, 0), 'top left': (0, 0), 'topleft': (0, 0),
          'top-center': (0, 1), 'top center': (0, 1), 'top-middle': (0, 1),
          'top-right': (0, 2), 'top right': (0, 2), 'topright': (0, 2),
          'middle-left': (1, 0), 'middle left': (1, 0), 'left': (1, 0),
          'middle-right': (1, 2), 'middle right': (1, 2), 'right': (1, 2),
          'bottom-left': (2, 0), 'bottom left': (2, 0), 'bottomleft': (2, 0),
          'bottom-center': (2, 1), 'bottom center': (2, 1), 'bottom-middle': (2, 1),
          'bottom-right': (2, 2), 'bottom right': (2, 2), 'bottomright': (2, 2)
      }
      
      for position, coords in position_map.items():
          if position in text:
              return coords
      
      # If all parsing attempts fail
      print(f"⚠️ Could not parse AI response: '{response_text}'")
      return None
  
  async def game_loop(self):
      """Main game loop"""
      # 1. Display current board
      # 2. If human turn: get human move, execute it
      # 3. If AI turn: get AI move, execute it  
      # 4. Check for game over
      # 5. Switch turns and repeat
      pass
  
  async def close(self):
      """Clean up connections"""
      # Close MCP client connection
      pass

# Main game function
async def play_tic_tac_toe():
    """Start and run a tic-tac-toe game"""
    game = Game()
    try:
        await game.start_game()
        await game.game_loop()
    finally:
        await game.close()

# Entry point
if __name__ == "__main__":
    asyncio.run(play_tic_tac_toe())