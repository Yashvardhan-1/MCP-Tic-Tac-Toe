import asyncio, json
from client import MCPClient

def pretty_print(label, data):
  """Extract and display clean content from MCP results"""
  print(f"\n🔍 {label}:")
    
  if not data:
    print("  None")
    return
  
  # Handle MCP result format - data.content is a list of TextContent objects
  if hasattr(data, 'content') and data.content:
    for item in data.content:
      if hasattr(item, 'text'):
        try:
          # Try to parse as JSON for pretty formatting
          parsed = json.loads(item.text)
          print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
          # If not JSON, print the text directly (like board display)
          print(item.text)
      else:
        print(f"  {item}")
  else:
      print(f"  {data}")

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
    pretty_print("Reset Result", result)
    
    # Test 2: Show board
    print("\n2️⃣ Testing show_board...")
    board = await client.show_board()
    pretty_print("Board", board)
    
    # Test 3: Make a move
    print("\n3️⃣ Testing play_move...")
    move_result = await client.play_move(1, 1)  # Center
    pretty_print("Move result", move_result)
    
    # Test 4: Show updated board
    print("\n4️⃣ Testing updated board...")
    updated_board = await client.show_board()
    pretty_print("Updated board", updated_board)
    
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