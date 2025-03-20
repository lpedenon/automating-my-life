import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import asdict
from enum import Enum

class ChatLogger:
    def __init__(self, log_dir: str = "chat_logs"):
        """Initialize chat logger.
        
        Args:
            log_dir: Directory to store chat logs
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
    def _serialize_dataclass(self, obj):
        """Helper method to serialize dataclass objects with enum handling.
        
        Args:
            obj: The dataclass object to serialize
        
        Returns:
            Dict with serialized data
        """
        if obj is None:
            return None
            
        data = asdict(obj)
        # Handle enum values in the dictionary
        for key, value in data.items():
            if isinstance(value, Enum):
                data[key] = value.value
        return data
    
    def log_chat(self, messages: List[Dict[str, str]], model: str, nlu_data: Optional[Dict] = None):
        """Log chat messages and NLU data to a JSON file.
        
        Args:
            messages: List of message dictionaries
            model: Name of the model used
            nlu_data: Optional dictionary containing NLU processing results
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_data = {
            "timestamp": timestamp,
            "model": model,
            "messages": messages,
            "nlu_data": nlu_data
        }
        
        filename = f"chat_{timestamp}.json"
        filepath = os.path.join(self.log_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
            
    def format_nlu_data(self, intent, entities, function_call):
        """Format NLU data for logging.
        
        Args:
            intent: Intent object from NLU pipeline
            entities: List of Entity objects
            function_call: FunctionCall object
        
        Returns:
            Dictionary containing formatted NLU data
        """
        return {
            "intent": self._serialize_dataclass(intent),
            "entities": [self._serialize_dataclass(e) for e in entities] if entities else [],
            "function_call": self._serialize_dataclass(function_call) if function_call else None
        } 