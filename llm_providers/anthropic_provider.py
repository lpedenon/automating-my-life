from typing import List, Dict, Optional
import anthropic
from .base import BaseLLMProvider

class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key
            model: Model to use (default: claude-3-sonnet-20240229)
        """
        self.model = model
        self.client = anthropic.Anthropic(api_key=api_key)
            
    def generate_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate response using Anthropic API."""
        try:
            # Convert messages to Anthropic format
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "user":
                    anthropic_messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    anthropic_messages.append({"role": "assistant", "content": msg["content"]})
            
            response = self.client.messages.create(
                model=self.model,
                messages=anthropic_messages,
                **kwargs
            )
            return response.content[0].text
        except Exception as e:
            return f"Error generating response: {str(e)}"
            
    def get_model_name(self) -> str:
        """Get the name of the model being used."""
        return self.model 