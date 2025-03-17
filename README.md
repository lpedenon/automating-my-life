# CLI Chat Interface

A minimal command-line interface for chatting with an LLM.

## Features

- Clean and simple command-line interface
- Chat history management
- Clear screen functionality
- Easy-to-use commands
- Modular LLM provider system
- OpenAI integration included

## Requirements

- Python 3.6 or higher
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

### OpenAI Integration

To use the OpenAI provider, you need to set up your API key. You can do this in two ways:

1. Set it as an environment variable:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

2. Or create a `.env` file in the project root:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the chat interface:
```bash
python cli_chat.py
```

### Commands

- Type your message and press Enter to send
- Type `exit` to quit the chat
- Type `clear` to clear the chat history
- Press Ctrl+C to exit at any time

## Adding New LLM Providers

The chat interface is designed to be modular and can work with any LLM provider that implements the `BaseLLMProvider` interface. To add a new provider:

1. Create a new class in the `llm_providers` directory that inherits from `BaseLLMProvider`
2. Implement the required methods:
   - `__init__`: Initialize the provider with necessary credentials
   - `generate_response`: Generate responses from the LLM
   - `get_model_name`: Return the name of the model being used
3. Import and use your new provider in `cli_chat.py`

Example of using a different provider:
```python
from llm_providers import YourCustomProvider

chat = ChatInterface(
    YourCustomProvider,
    api_key="your-api-key",
    model="your-model"
)
```

## Note

This is a basic implementation that simulates AI responses. To integrate with an actual LLM, you'll need to modify the `chat` method in the `ChatInterface` class to connect to your preferred LLM service. 