# Natural Language Understanding (NLU) Module

A sophisticated natural language understanding system that processes user input to extract intents and entities, with support for weighted pattern matching and context-aware entity extraction.

## Features

### Intent Recognition
- **Weighted Pattern Matching**: Each intent has associated patterns with weights (0.0 to 1.0)
- **Confidence Calculation**: Based on pattern length and weight
  ```python
  pattern_confidence = len(pattern) / len(text)
  weighted_confidence = pattern_confidence * weight
  ```
- **Pattern Configuration**: Defined in YAML for easy maintenance
  ```yaml
  intents:
    calendar:
      patterns:
        - keyword: meeting
          weight: 1.0
        - keyword: schedule
          weight: 0.9
  ```

### Entity Extraction
- **Specialized Extractors**: Dedicated extractors for different entity types
- **Regex-based Pattern Matching**: Comprehensive patterns for various entities
- **Confidence Scoring**: Based on pattern complexity and context
- **Metadata Extraction**: Additional structured data for certain entities

#### Supported Entity Types
1. **Datetime**
   - Specific times: "2:30 PM", "14:00"
   - Relative dates: "tomorrow", "next Friday"
   - Absolute dates: "March 15th"
   - Durations: "1 hour", "30 minutes"

2. **Person**
   - Full names: "John Smith"
   - Pronouns: "he", "she", "they"

3. **Location**
   - Prepositional phrases: "in the office", "at home"

4. **Duration**
   - Time periods: "for 1 hour", "30 minutes"

5. **Priority**
   - Priority levels: "high priority", "urgent"

### Context-Aware Processing
- Entity extraction is filtered based on intent type
- Different entity types are relevant for different intents:
  ```python
  relevant_entities = {
      'calendar': ['datetime', 'person', 'location', 'duration'],
      'email': ['person', 'subject'],
      'task': ['person', 'priority', 'duration'],
      'note': ['subject', 'location']
  }
  ```

## Implementation Details

### Intent Detection
1. Text is converted to lowercase for case-insensitive matching
2. Each pattern is checked against the text
3. Confidence is calculated based on:
   - Pattern length relative to text length
   - Pattern weight from configuration
4. Best matching intent is selected based on weighted confidence

### Entity Extraction
1. Text is processed through regex patterns for each entity type
2. Matches are converted to Entity objects with:
   - Type
   - Value
   - Confidence score
   - Position in text
   - Optional metadata

### Datetime Processing
- Relative dates are converted to absolute dates
- Times are normalized to 24-hour format
- Metadata includes:
  - Original text
  - Parsed datetime
  - Type (absolute/relative)

## Usage

### Basic Usage
```python
from nlu.pipeline import NLUPipeline

pipeline = NLUPipeline()
result = pipeline.process("Schedule a meeting with John tomorrow at 2pm")
```

### Configuration
1. Edit `config/intents.yaml` to modify:
   - Intent patterns and weights
   - Entity type definitions
   - Function mappings

2. Customize entity patterns in `entity_extractor.py`

### Testing
Run the test interface:
```bash
python -m nlu.pipeline
```

## Current Limitations

1. **Intent Detection**
   - Currently uses simple pattern matching
   - No support for compound intents
   - Limited context awareness

2. **Entity Extraction**
   - Basic regex patterns may miss complex cases
   - Limited support for ambiguous entities
   - No machine learning-based extraction

3. **Datetime Processing**
   - Limited support for complex date expressions
   - No timezone handling
   - Basic duration parsing

## TODO

### Short-term Improvements
- [ ] Implement compound intent detection
- [ ] Add support for timezone handling
- [ ] Improve datetime parsing with dateparser library
- [ ] Add validation for configuration files
- [ ] Implement entity disambiguation

### Long-term Goals
- [ ] Integrate machine learning for intent classification
- [ ] Add support for context memory
- [ ] Implement fuzzy matching for entity extraction
- [ ] Add support for custom entity types
- [ ] Create a plugin system for custom extractors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Dependencies
- Python 3.8+
- PyYAML
- datetime (standard library)
- re (standard library)

## License
This module is part of the Multi-Agent Life Automation System and is licensed under the MIT License. 