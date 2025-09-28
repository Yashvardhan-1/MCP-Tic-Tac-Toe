from cgitb import reset
from math import fabs
from anthropic import Anthropic
import os
import json, subprocess, threading, time, queue

MCP_SERVER_CMD = ["uv", "run", "python", "main.py", "--mcp"]
ANTHROPIC_MODEL = "claude-3-5-sonnet-latest"  
HUMAN_PLAYS = "X"
MODEL_PLAYS = "O" if HUMAN_PLAYS == "X" else "X"

anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class MCPClient:
  def __init__(self, server_cmd):
    self.server_cmd = server_cmd
    self.process = None
    self.request_id = 0
    self.response_queue = queue.Queue()
    self.running = False
  
  def start_server(self):
    try:
      self.process = subprocess.Popen(
        self.server_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
      )
      print(f"🔢 Process ID: {self.process.pid}")
      self.running = True
      self.reader_thread = threading.Thread(target=self._read_response)
      self.reader_thread.daemon = True
      self.reader_thread.start()
    except Exception as e:
      print(f"Error starting server: {e}")
      import traceback
      traceback.print_exc()
      self.running = False

    return self.running
  
  def _read_response(self):
    while self.running:
      try:
        # this blocks but in a different thread
        line = self.process.stdout.readline()
        if line:
          response = json.loads(line.strip())
          self.response_queue.put(response)
      except json.JSONDecodeError:
        print(f"Error decoding JSON: {line}")
        continue
      except Exception as e:
        print(f"Error reading response: {e}")
        break

  def _send_request(self, method, args):
    self.request_id += 1
    request = {
      "jsonrpc": "2.0",
      "id": self.request_id,
      "method": method,
      "params": args
    }

    print(f"🔍 Sending request: {json.dumps(request, indent=2)}")

    try: 
      self.process.stdin.write(json.dumps(request) + "\n")
      self.process.stdin.flush()
      return self.request_id
    except Exception as e:
      print(f"Error sending request: {e}")
      return None

  def _wait_for_response(self, request_id, timeout=10):
    start_time = time.time()

    while time.time() - start_time < timeout:
      try:
        response = self.response_queue.get(timeout=timeout)
        if response["id"] == request_id:
          return response
        else:
          self.response_queue.put(response)
      except queue.Empty:
        continue
  
  def call_tool(self, tool_name, args = None):

    if not self.process or self.process.poll() is not None:
      print("Server is not running")
      return None
    
    request_id = self._send_request(tool_name, args or {})

    if request_id is None:
      print("Error sending request")
      return None
    
    response = self._wait_for_response(request_id)
    if response is None:
      print("Timeout waiting for response")
      return None
    
    if "result" in response:
      return response["result"]
    elif "error" in response:
      print(f"❌ Tool call error: {response['error']}")
      return None
    else:
      print(f"❌ Unexpected response format: {response}")
      return None
  
  def stop_server(self):
    self.running = False
    if self.process:
      try: 
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=5)
        self.process = None
      except subprocess.TimeoutExpired:
        # If server doesn't shut down gracefully, force kill
        self.process.kill()
        self.process.wait()
      except Exception as e:
        print(f"Error stopping server: {e}")
        self.process = None
  
  def play_move(self, row, col):      
    return self.call_tool("play_move", {"row": row, "col": col})

  def show_board(self):
    return self.call_tool("show_board")

  def get_state(self):
    return self.call_tool("get_state")

  def reset_game(self):
    return self.call_tool("reset_game")
  
def play_game():
    messages = [
        {"role": "system", "content": "You are playing a game of Tic Tac Toe."},
        {"role": "user", "content": "Play a game of Tic Tac Toe."}
    ]

play_game()