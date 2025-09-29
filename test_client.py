import asyncio
from client import MCPClient

from utils import extract_result_text

async def test_mcp_client():
  """Test the MCPClient class"""
  print("🧪 Testing MCPClient...")
  
  client = MCPClient()
  
  try:
      # Start the client
    if not await client.start():
      print("❌ Client startup failed")
      return False
  
    # Test 1: Reset game
    print("\n1️⃣ Testing reset_game...")
    result = await client.reset_game()
    resutl_str = extract_result_text(result)
    print(f"\n{resutl_str}")
    
    # Test 2: Show board
    print("\n2️⃣ Testing show_board...")
    board = await client.show_board()
    board_text = extract_result_text(board)
    print(f"\n{board_text}")
    
    # Test 3: Make a move
    print("\n3️⃣ Testing play_move...")
    move_result = await client.play_move(1, 1)
    move_result_text = extract_result_text(move_result)
    print(f"\n{move_result_text}")
    
    # Test 4: Show updated board
    print("\n4️⃣ Testing updated board...")
    updated_board = await client.show_board()
    updated_board_text = extract_result_text(updated_board)
    print(f"\n{updated_board_text}")
    
    print("\n✅ All tests completed!")
    return True
      
  except Exception as e:
    print(f"❌ Test failed with error: {e}")
    import traceback
    traceback.print_exc()
    return False
      
  finally:
    # Always cleanup
    await client.close()

if __name__ == "__main__":
    asyncio.run(test_mcp_client())