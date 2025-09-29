def extract_result_text(data):
  """Extract just the board text from MCP results"""
  if not data:
    return None
  
  if isinstance(data, list):
    for item in data:
      if hasattr(item, 'text'):
        return item.text
  
  return str(data)