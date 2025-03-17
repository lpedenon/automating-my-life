# Multi-Agent Life Automation System

A modular system for automating life tasks using multiple AI agents. The system consists of a main orchestrator agent that delegates tasks to specialized agents for specific functions like scheduling meetings, managing emails, and more.

## Project Goals

- Create a flexible, modular system for life automation
- Implement a main orchestrator agent that can understand and delegate tasks
- Develop specialized agents for specific tasks (email, calendar, etc.)
- Provide a unified interface for interacting with all agents
- Ensure secure handling of sensitive data and API keys

## Current Features

### Core Infrastructure
- Modular LLM provider system supporting multiple AI services
  - OpenAI integration
  - Anthropic integration
  - Extensible architecture for adding more providers
- Secure API key management using environment variables
- Chat logging system for tracking conversations and task execution

### Chat Interface
- Clean command-line interface
- Support for multiple LLM providers
- Chat history management
- Persistent logging of conversations
- Clear screen functionality

## Project Structure

```
.
├── llm_providers/           # LLM provider implementations
│   ├── base.py             # Base provider interface
│   ├── openai_provider.py  # OpenAI implementation
│   ├── anthropic_provider.py # Anthropic implementation
│   └── __init__.py
├── utils/                  # Utility modules
│   └── logger.py          # Chat logging functionality
├── cli_chat.py            # Main chat interface
├── requirements.txt       # Project dependencies
├── .env.example          # Environment variables template
└── .gitignore           # Git ignore rules
```

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys:
```
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
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

## Todo

### Phase 1: Core Agent System
- [ ] Implement main orchestrator agent
- [ ] Create task parsing and delegation system
- [ ] Develop agent communication protocol
- [ ] Add basic task queue management

### Phase 2: Specialized Agents
- [ ] Email management agent
- [ ] Calendar/scheduling agent
- [ ] Task management agent
- [ ] Note-taking agent

### Phase 3: Integration & Enhancement
- [ ] Add web interface
- [ ] Implement agent memory system
- [ ] Add task prioritization
- [ ] Create agent performance monitoring
- [ ] Add support for custom agent plugins

### Phase 4: Security & Reliability
- [ ] Implement robust error handling
- [ ] Add rate limiting and API usage monitoring
- [ ] Create backup and recovery systems
- [ ] Add audit logging for sensitive operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 