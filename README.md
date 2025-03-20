# Multi-Agent Life Automation System

A sophisticated system that uses multiple AI agents to automate various life tasks, from calendar management to email handling. The system is designed to be modular, extensible, and user-friendly.

## Overview

This project implements a multi-agent system where different specialized AI agents work together to handle various life tasks. The system uses a Natural Language Understanding (NLU) pipeline to process user requests and route them to the appropriate agent.

### Key Components

1. **Natural Language Understanding (NLU) Pipeline**
   - Configurable intent recognition with weighted pattern matching
   - Context-aware entity extraction (dates, times, people, locations)
   - Support for multiple intents and complex queries
   - YAML-based configuration for easy customization
   - Confidence scoring for both intents and entities

2. **Specialized Agents**
   - Calendar Agent: Manages appointments and events
   - Email Agent: Handles email composition and management
   - Task Agent: Creates and manages to-do items
   - Note Agent: Manages note-taking and organization

3. **Unified Interface**
   - Single entry point for all agent interactions
   - Secure handling of sensitive data and API keys
   - Consistent response format across all agents

## Features

### Current Features
- Natural language processing of user requests
- Calendar event creation and management
- Email composition and sending
- Task creation and tracking
- Note-taking and organization
- Secure API key management
- Modular and extensible architecture

### NLU Capabilities
- **Intent Recognition**
  - Weighted pattern matching for accurate intent detection
  - Support for multiple intents in a single query
  - Confidence scoring based on pattern relevance

- **Entity Extraction**
  - Datetime parsing (absolute and relative dates/times)
  - Person name and pronoun recognition
  - Location detection
  - Duration and priority extraction
  - Context-aware entity filtering

- **Function Mapping**
  - Automatic mapping of intents to agent functions
  - Parameter extraction from entities
  - Confidence-based function selection

## Project Structure

```
.
├── agents/                 # Specialized AI agents
│   ├── calendar/          # Calendar management
│   ├── email/            # Email handling
│   ├── task/             # Task management
│   └── note/             # Note-taking
├── nlu/                   # Natural Language Understanding
│   ├── pipeline.py       # Main NLU processing
│   ├── entity_extractor.py # Entity extraction
│   └── config/           # NLU configuration
│       └── intents.yaml  # Intent definitions
├── utils/                # Shared utilities
├── config/               # System configuration
└── tests/               # Test suite
```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/automating-my-life.git
   cd automating-my-life
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

4. Configure NLU patterns (optional):
   ```bash
   # Edit nlu/config/intents.yaml to customize intent patterns
   ```

## Usage

### Basic Usage
```python
from nlu.pipeline import NLUPipeline

# Initialize the pipeline
pipeline = NLUPipeline()

# Process a user request
result = pipeline.process("Schedule a meeting with John tomorrow at 2pm")
```

### Example Queries
- "Schedule a meeting with John Smith tomorrow at 2:30 PM in the office for 1 hour"
- "Send an email to Sarah about the project deadline"
- "Create a high priority task to review the presentation"
- "Take a note about the meeting discussion"

## Testing

Run the test suite:
```bash
pytest
```

Test the NLU pipeline:
```bash
python -m nlu.pipeline
```

## Future Phases

### Phase 1: Enhanced NLU
- [x] Implement weighted pattern matching
- [x] Add context-aware entity extraction
- [ ] Add support for compound intents
- [ ] Implement entity disambiguation
- [ ] Add timezone support

### Phase 2: Agent Integration
- [ ] Implement agent communication protocols
- [ ] Add support for multi-agent tasks
- [ ] Create agent state management
- [ ] Implement task delegation

### Phase 3: Advanced Features
- [ ] Add machine learning for intent classification
- [ ] Implement context memory
- [ ] Add support for custom agents
- [ ] Create a plugin system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- Contributors and maintainers 