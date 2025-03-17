#!/usr/bin/env python3
import os
import sys
from typing import List, Optional, Type
from dotenv import load_dotenv
from llm_providers import BaseLLMProvider, OpenAIProvider, AnthropicProvider
from utils.logger import ChatLogger

# Load environment variables from .env file
load_dotenv()

class ChatInterface:
    def __init__(self, llm_provider_class: Type[BaseLLMProvider], **provider_kwargs):
        """Initialize chat interface with specified LLM provider.
        
        Args:
            llm_provider_class: Class of the LLM provider to use
            **provider_kwargs: Arguments to pass to the provider constructor
        """
        self.chat_history: List[dict] = []
        self.llm_provider = llm_provider_class(**provider_kwargs)
        self.logger = ChatLogger()
        self.clear_screen()
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_message(self, role: str, content: str):
        """Print a message with appropriate formatting."""
        if role == "user":
            print(f"\n👤 You: {content}")
        else:
            print(f"\n🤖 Assistant: {content}")
            
    def get_user_input(self) -> Optional[str]:
        """Get input from the user."""
        try:
            return input("\n👤 You: ").strip()
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            sys.exit(0)
            
    def chat(self):
        """Main chat loop."""
        print(f"Welcome to the CLI Chat Interface!")
        print(f"Using model: {self.llm_provider.get_model_name()}")
        print("Type 'exit' to quit or 'clear' to clear the chat history.")
        print("-" * 50)
        
        while True:
            user_input = self.get_user_input()
            
            if user_input.lower() == 'exit':
                print("\nGoodbye!")
                # Log the final chat history before exiting
                self.logger.log_chat(self.chat_history, self.llm_provider.get_model_name())
                break
                
            if user_input.lower() == 'clear':
                self.chat_history = []
                self.clear_screen()
                print("Chat history cleared!")
                continue
                
            if not user_input:
                continue
                
            # Add user message to history
            self.chat_history.append({"role": "user", "content": user_input})
            
            # Generate response using LLM
            response = self.llm_provider.generate_response(self.chat_history)
            
            # Add assistant response to history
            self.chat_history.append({"role": "assistant", "content": response})
            self.print_message("assistant", response)

if __name__ == "__main__":
    # Example usage with OpenAI provider
    chat = ChatInterface(
        OpenAIProvider,
        api_key=os.getenv("OPENAI_API_KEY"),  # Get API key from environment variable
        model="gpt-3.5-turbo"
    )
    chat.chat() 