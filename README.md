# Multi-Agent Life Automation System

A modular system for automating life tasks using multiple AI agents. The system consists of a main orchestrator agent that delegates tasks to specialized agents for specific functions like scheduling meetings, managing emails, and more.

## Project Goals

- Create a flexible, modular system for life automation
- Implement a main orchestrator agent that can understand and delegate tasks
- Develop specialized agents for specific tasks (email, calendar, etc.)
- Provide a unified interface for interacting with all agents
- Ensure secure handling of sensitive data and API keys
- create a notification functionality where the application can send the user notifications

## Current Features

### Core Infrastructure
- Modular LLM provider system supporting multiple AI services
  - OpenAI integration
  - Anthropic integration
  - Extensible architecture for adding more providers
- Secure API key management using environment variables
- Chat logging system for tracking conversations and task execution

### Natural Language Understanding (NLU) Pipeline
- Intent recognition system for common tasks:
  - Schedule meetings
    - using keyword "meetings"
  - Send emails
    - using keyword "emails"
  - Create tasks
    - using keyword "tasks"
  - Take notes
    - using keyword "notes"

- Entity extraction for: NOT COMPLETE (Should be with AI)
  - Datetime information
  - People/contacts
  - Subjects/topics
  - Priority levels
- Function mapping system to convert intents into actionable commands
- Confidence scoring for intent and entity recognition
- Interactive test interface for pipeline debugging and development

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
├── nlu/                    # Natural Language Understanding
│   ├── pipeline.py        # Core NLU pipeline implementation
│   └── __init__.py        # NLU module exports
├── tests/                  # Test suite
│   ├── nlu/               # NLU-specific tests
│   │   ├── test_pipeline.py  # Pipeline unit tests
│   │   └── test_cli.py       # Interactive test interface
│   └── conftest.py        # Shared test configuration
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

### Main Chat Interface
Run the chat interface:
```bash
python cli_chat.py
```

### NLU Test Interface
Run the interactive NLU test interface:
```bash
python -m tests.nlu.test_cli
```

The test interface provides detailed information about the NLU pipeline process:
- Input text analysis
- Intent recognition details
- Entity extraction results
- Function call mapping

Example usage:
```
=== NLU Pipeline Test Interface ===
Type 'exit' to quit
Type 'help' to see available commands

Enter text to process: schedule a meeting with John tomorrow at 2pm

=== Input Text ===
'schedule a meeting with John tomorrow at 2pm'

=== Intent Information ===
Type: schedule_meeting
Confidence: 0.50
Raw Text: schedule a meeting with john tomorrow at 2pm
Number of Entities: 2

=== Entity Information ===
  Entity Type: datetime
  Value: tomorrow
  Confidence: 0.80
  Position: 4 to 5

  Entity Type: person
  Value: john
  Confidence: 0.80
  Position: 3 to 4

=== Function Call Information ===
Function Name: schedule_meeting
Confidence: 0.50

Parameters:
  datetime: tomorrow
  person: john
```

### Commands
- Type your message and press Enter to send
- Type `exit` to quit the chat
- Type `clear` to clear the chat history
- Press Ctrl+C to exit at any time

## Testing

Run the test suite:
```bash
pytest tests/
```

Run specific test files:
```bash
pytest tests/nlu/test_pipeline.py  # Run NLU pipeline tests
```

## Todo

### Phase 1: Core Agent System
- [x] Implement NLU pipeline for intent recognition
- [x] Create interactive test interface
- [ ] Finish entity extraction (might have to do with AI)
- [ ] Implement main orchestrator agent
- [ ] Create task parsing and delegation system
- [ ] Develop agent communication protocol
- [ ] Add basic task queue management

### Phase 2: Specialized Agents
- [ ] Email management agent
- [ ] Calendar/scheduling agent
- [ ] Task management agent
- [ ] Note-taking agent
- [ ] Obsidian agent 
  - [ ] write new notes into obsidian
  - [ ] Parse the knowledge on obsidian
- [ ] Note taking agent

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