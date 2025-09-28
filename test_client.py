from client import MCPClient
import time

MCP_SERVER_CMD = ["uv", "run", "python", "main.py", "--mcp"]

# Test the MCPClient
def test_mcp_client():
    """
    Simple test of MCPClient functionality
    """
    print("🧪 Testing MCPClient...")
    
    # Create client
    client = MCPClient(MCP_SERVER_CMD)
    
    try:
        # Test 1: Start server
        print("\n1️⃣ Testing server startup...")
        if not client.start_server():
            print("❌ Server startup failed")
            return False
        
        # Give server time to initialize
        time.sleep(2)
        
        # Test 2: Reset game
        print("\n2️⃣ Testing reset_game...")
        result = client.reset_game()
        print(f"Reset result: {result}")
        
        # # Test 3: Show board
        # print("\n3️⃣ Testing show_board...")
        # board = client.show_board()
        # print(f"Board: {board}")
        
        # # Test 4: Get state
        # print("\n4️⃣ Testing get_state...")
        # state = client.get_state()
        # print(f"State: {state}")
        
        # # Test 5: Make a move
        # print("\n5️⃣ Testing play_move...")
        # move_result = client.play_move(1, 1)  # Center
        # print(f"Move result: {move_result}")
        
        # # Test 6: Show board after move
        # print("\n6️⃣ Testing board after move...")
        # updated_board = client.show_board()
        # print(f"Updated board: {updated_board}")
        
        # print("\n✅ All tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
        
    finally:
        # Always cleanup
        client.stop_server()

if __name__ == "__main__":
    test_mcp_client()