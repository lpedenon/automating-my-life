import os
import json
from datetime import datetime
from typing import List, Dict

class ChatLogger:
    def __init__(self, log_dir: str = "chat_logs"):
        """Initialize chat logger.
        
        Args:
            log_dir: Directory to store chat logs
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
    def log_chat(self, messages: List[Dict[str, str]], model: str):
        """Log chat messages to a JSON file.
        
        Args:
            messages: List of message dictionaries
            model: Name of the model used
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_data = {
            "timestamp": timestamp,
            "model": model,
            "messages": messages
        }
        
        filename = f"chat_{timestamp}.json"
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False) 