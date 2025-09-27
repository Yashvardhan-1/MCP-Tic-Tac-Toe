#!/usr/bin/env python3

import json
import subprocess
import os

def run_json_command(json_data):
    """Run main.py with JSON input"""
    try:
        process = subprocess.run(
            ['uv', 'run', 'python', 'main.py'],
            input=json.dumps(json_data),
            text=True,
            capture_output=True,
            cwd='/Users/yuktabagdi/Documents/Yash/tic tac toe/mcp-ttt'
        )
        return process.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def test_tic_tac_toe_game():
    """Test a complete tic-tac-toe game"""
    print("🎮 Testing Complete Tic-Tac-Toe Game")
    print("=" * 50)
    
    # Reset game
    print("\n1. Resetting game...")
    result = run_json_command({"tool": "reset_game", "args": {}})
    print(result)
    
    # Show initial board
    print("\n2. Showing initial board...")
    result = run_json_command({"tool": "show_board", "args": {}})
    print(result)
    
    # Play some moves
    moves = [
        {"row": 0, "col": 0, "desc": "X plays top-left"},
        {"row": 1, "col": 1, "desc": "O plays center"},
        {"row": 0, "col": 1, "desc": "X plays top-middle"},
        {"row": 2, "col": 2, "desc": "O plays bottom-right"},
        {"row": 0, "col": 2, "desc": "X plays top-right (wins!)"}
    ]
    
    for i, move in enumerate(moves, 3):
        print(f"\n{i}. {move['desc']}")
        result = run_json_command({
            "tool": "play_move",
            "args": {"row": move["row"], "col": move["col"]}
        })
        print(result)
        
        # Show board after each move
        board_result = run_json_command({"tool": "show_board", "args": {}})
        print("Board:", board_result)
        
        # Check if game is over
        state_result = run_json_command({"tool": "get_state", "args": {}})
        state_data = json.loads(state_result)
        if state_data.get("game_over"):
            print("🎉 Game Over!")
            break

def test_all_tools():
    """Test all available tools"""
    print("\n🔧 Testing All Tools")
    print("=" * 50)
    
    tests = [
        {
            "name": "Reset Game",
            "request": {"tool": "reset_game", "args": {}}
        },
        {
            "name": "Get State", 
            "request": {"tool": "get_state", "args": {}}
        },
        {
            "name": "Play Move (1,1)",
            "request": {"tool": "play_move", "args": {"row": 1, "col": 1}}
        },
        {
            "name": "Show Board",
            "request": {"tool": "show_board", "args": {}}
        },
        {
            "name": "Friendly Greeting",
            "request": {"tool": "greet_user", "args": {"name": "Alice", "style": "friendly"}}
        },
        {
            "name": "Formal Greeting", 
            "request": {"tool": "greet_user", "args": {"name": "Dr. Smith", "style": "formal"}}
        }
    ]
    
    for test in tests:
        print(f"\n🧪 {test['name']}:")
        print(f"Request: {json.dumps(test['request'], indent=2)}")
        result = run_json_command(test['request'])
        print(f"Response: {result}")

def main():
    print("📋 JSON CLI Testing for Tic-Tac-Toe MCP")
    print("=" * 60)
    
    test_all_tools()
    test_tic_tac_toe_game()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\n💡 Usage examples:")
    print("echo '{\"tool\": \"show_board\", \"args\": {}}' | uv run python main.py")
    print("echo '{\"tool\": \"play_move\", \"args\": {\"row\": 1, \"col\": 1}}' | uv run python main.py")

if __name__ == "__main__":
    main()