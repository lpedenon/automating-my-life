from dataclasses import dataclass
from typing import List, Dict, Optional
import re
from datetime import datetime, timedelta
import dateparser
from abc import ABC, abstractmethod

@dataclass
class Entity:
    """Represents an extracted entity from text.
    
    Attributes:
        type (str): The type of entity (e.g., 'datetime', 'person', 'location')
        value (str): The actual text value of the entity
        confidence (float): Confidence score for the extraction (0.0 to 1.0)
        start (int): Starting position of the entity in the text
        end (int): Ending position of the entity in the text
        metadata (Optional[Dict]): Additional structured data about the entity
    """
    type: str
    value: str
    confidence: float
    start: int
    end: int
    metadata: Optional[Dict] = None

class BaseEntityExtractor(ABC):
    """Abstract base class for entity extraction.
    
    This class provides the foundation for all entity extractors, defining the common
    interface and shared functionality. Each specific extractor (e.g., CalendarEntityExtractor)
    should inherit from this class and implement the extract_entities method.
    
    Attributes:
        patterns (Dict[str, List[str]]): Dictionary mapping entity types to their regex patterns
        compiled_patterns (Dict[str, List[re.Pattern]]): Compiled regex patterns for efficient matching
    """
    
    def __init__(self):
        """Initialize the base entity extractor."""
        self.patterns = {}
        self.compiled_patterns = {}
        
    def compile_patterns(self):
        """Compile regex patterns for efficient matching.
        
        This method should be called after setting up patterns in the subclass's __init__.
        It compiles all regex patterns once for better performance during extraction.
        """
        self.compiled_patterns = {
            entity_type: [re.compile(pattern) for pattern in patterns]
            for entity_type, patterns in self.patterns.items()
        }
    
    @abstractmethod
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract entities from text using regex patterns.
        
        This is the main method that must be implemented by all subclasses.
        It should use the compiled patterns to find and extract entities from the input text.
        
        Args:
            text (str): The input text to extract entities from
            
        Returns:
            List[Entity]: List of extracted entities with their metadata
        """
        pass
    
    def _calculate_confidence(self, entity_type: str, value: str) -> float:
        """Calculate confidence score for an extracted entity.
        
        The confidence score is based on the entity type and characteristics of the value.
        Higher scores indicate higher confidence in the extraction.
        
        Args:
            entity_type (str): Type of the entity being extracted
            value (str): The extracted value
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        base_confidence = {
            'datetime': 0.9,
            'person': 0.8,
            'location': 0.7,
            'duration': 0.8,
            'priority': 0.7,
            'subject': 0.7,
        }.get(entity_type, 0.6)
        
        # Adjust confidence based on value characteristics
        if entity_type == 'datetime':
            # Higher confidence for specific dates/times
            if re.match(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?', value):
                return 0.95
            # Lower confidence for relative dates
            if re.match(r'\b(?:tomorrow|today|yesterday)\b', value):
                return 0.85
                
        elif entity_type == 'person':
            # Higher confidence for full names
            if len(value.split()) > 1:
                return 0.9
                
        return base_confidence

class CalendarEntityExtractor(BaseEntityExtractor):
    """Extractor for calendar-related entities.
    
    This extractor specializes in finding entities relevant to calendar events,
    such as dates, times, people, locations, and durations.
    
    Supported entity types:
    - datetime: Dates and times (e.g., "tomorrow at 2pm", "next Friday")
    - person: Names and pronouns (e.g., "John Smith", "he")
    - location: Places (e.g., "in the office", "at home")
    - duration: Time periods (e.g., "1 hour", "30 minutes")
    """
    
    def __init__(self):
        """Initialize the calendar entity extractor with relevant patterns."""
        super().__init__()
        self.patterns = {
            'datetime': [
                # Time patterns (e.g., "2pm", "14:00", "2:00 PM")
                r'\b\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?\b',
                # Date patterns (e.g., "tomorrow", "next Friday", "March 15th")
                r'\b(?:tomorrow|today|yesterday|next\s+\w+|last\s+\w+)\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:st|nd|rd|th)?\b',
                # Relative dates (e.g., "in 2 days", "3 weeks from now")
                r'\b(?:in|after)\s+\d+\s+(?:day|week|month|year)s?\b',
            ],
            'person': [
                # Name patterns (assuming capitalized words are names)
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                # Pronouns
                r'\b(?:he|she|they|him|her|them)\b',
            ],
            'location': [
                # Location patterns (e.g., "in the office", "at home")
                r'\b(?:in|at|on)\s+[a-zA-Z\s]+(?:\s+[a-zA-Z\s]+)*\b',
            ],
            'duration': [
                # Duration patterns (e.g., "for 1 hour", "30 minutes")
                r'\b(?:for\s+)?\d+\s+(?:hour|minute|day|week|month)s?\b',
            ],
        }
        self.compile_patterns()
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract calendar-related entities from text.
        
        Args:
            text (str): Input text to extract entities from
            
        Returns:
            List[Entity]: List of extracted calendar entities
        """
        entities = []
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    value = match.group()
                    start, end = match.span()
                    
                    confidence = self._calculate_confidence(entity_type, value)
                    metadata = self._extract_metadata(entity_type, value)
                    
                    entities.append(Entity(
                        type=entity_type,
                        value=value,
                        confidence=confidence,
                        start=start,
                        end=end,
                        metadata=metadata
                    ))
        
        return entities
    
    def _extract_metadata(self, entity_type: str, value: str) -> Optional[Dict]:
        """Extract additional metadata for calendar entities.
        
        Currently handles datetime metadata, which includes parsed date/time
        and human-readable format.
        
        Args:
            entity_type (str): Type of the entity
            value (str): The extracted value
            
        Returns:
            Optional[Dict]: Metadata dictionary if applicable, None otherwise
        """
        if entity_type == 'datetime':
            return self._parse_datetime(value)
        return None
    
    def _parse_datetime(self, value: str) -> Dict:
        """Parse datetime string into structured data.
        
        Uses dateparser library to handle various date/time formats and
        converts them into a standardized format with metadata.
        
        Args:
            value (str): The datetime string to parse
            
        Returns:
            Dict: Dictionary containing parsed datetime and metadata
        """
        metadata = {
            'original': value,
            'parsed': None,
            'type': None,
            'human_readable': None
        }
        
        parsed_date = dateparser.parse(value)
        
        if parsed_date:
            metadata['parsed'] = parsed_date
            metadata['type'] = 'absolute' if 'at' in value.lower() or re.match(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?', value) else 'relative'
            
            day_suffix = "th"
            if parsed_date.day % 10 == 1 and parsed_date.day != 11:
                day_suffix = "st"
            elif parsed_date.day % 10 == 2 and parsed_date.day != 12:
                day_suffix = "nd"
            elif parsed_date.day % 10 == 3 and parsed_date.day != 13:
                day_suffix = "rd"
            
            metadata['human_readable'] = parsed_date.strftime(f"%B %d{day_suffix}, %Y at %I:%M %p")
        else:
            metadata['type'] = 'unknown'
            metadata['human_readable'] = value
            
        return metadata

class EmailEntityExtractor(BaseEntityExtractor):
    """Extractor for email-related entities.
    
    This extractor specializes in finding entities relevant to email composition,
    such as recipients and email subjects.
    
    Supported entity types:
    - person: Names and email addresses (e.g., "John Smith", "john@example.com")
    - subject: Email subjects (e.g., "subject: Project Update")
    """
    
    def __init__(self):
        """Initialize the email entity extractor with relevant patterns."""
        super().__init__()
        self.patterns = {
            'person': [
                # Name patterns
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
                # Email addresses
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            ],
            'subject': [
                # Subject patterns (text between quotes or after "subject:")
                r'(?:subject:|")([^"\n]+)(?:"|$)',
            ],
        }
        self.compile_patterns()
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract email-related entities from text.
        
        Args:
            text (str): Input text to extract entities from
            
        Returns:
            List[Entity]: List of extracted email entities
        """
        entities = []
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    value = match.group()
                    start, end = match.span()
                    
                    confidence = self._calculate_confidence(entity_type, value)
                    
                    entities.append(Entity(
                        type=entity_type,
                        value=value,
                        confidence=confidence,
                        start=start,
                        end=end
                    ))
        
        return entities

class TaskEntityExtractor(BaseEntityExtractor):
    """Extractor for task-related entities.
    
    This extractor specializes in finding entities relevant to task management,
    such as assignees, priorities, and durations.
    
    Supported entity types:
    - person: Names of task assignees (e.g., "John Smith")
    - priority: Priority levels (e.g., "high priority", "urgent")
    - duration: Time periods (e.g., "2 hours", "30 minutes")
    """
    
    def __init__(self):
        """Initialize the task entity extractor with relevant patterns."""
        super().__init__()
        self.patterns = {
            'person': [
                # Name patterns
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
            ],
            'priority': [
                # Priority patterns
                r'\b(?:high|low|urgent|important|critical)\s+priority\b',
                r'\b(?:urgent|important|critical)\b',
            ],
            'duration': [
                # Duration patterns
                r'\b(?:for\s+)?\d+\s+(?:hour|minute|day|week|month)s?\b',
            ],
        }
        self.compile_patterns()
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract task-related entities from text.
        
        Args:
            text (str): Input text to extract entities from
            
        Returns:
            List[Entity]: List of extracted task entities
        """
        entities = []
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    value = match.group()
                    start, end = match.span()
                    
                    confidence = self._calculate_confidence(entity_type, value)
                    
                    entities.append(Entity(
                        type=entity_type,
                        value=value,
                        confidence=confidence,
                        start=start,
                        end=end
                    ))
        
        return entities

class NoteEntityExtractor(BaseEntityExtractor):
    """Extractor for note-related entities.
    
    This extractor specializes in finding entities relevant to note-taking,
    such as subjects and locations.
    
    Supported entity types:
    - subject: Note subjects (e.g., "subject: Project Status")
    - location: Note locations (e.g., "in the meeting room")
    """
    
    def __init__(self):
        """Initialize the note entity extractor with relevant patterns."""
        super().__init__()
        self.patterns = {
            'subject': [
                # Subject patterns
                r'(?:subject:|")([^"\n]+)(?:"|$)',
            ],
            'location': [
                # Location patterns
                r'\b(?:in|at|on)\s+[a-zA-Z\s]+(?:\s+[a-zA-Z\s]+)*\b',
            ],
        }
        self.compile_patterns()
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract note-related entities from text.
        
        Args:
            text (str): Input text to extract entities from
            
        Returns:
            List[Entity]: List of extracted note entities
        """
        entities = []
        
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    value = match.group()
                    start, end = match.span()
                    
                    confidence = self._calculate_confidence(entity_type, value)
                    
                    entities.append(Entity(
                        type=entity_type,
                        value=value,
                        confidence=confidence,
                        start=start,
                        end=end
                    ))
        
        return entities

def get_entity_extractor(intent_type: str) -> BaseEntityExtractor:
    """Factory function to get the appropriate entity extractor based on intent type.
    
    This function creates and returns the appropriate entity extractor based on the
    specified intent type. It implements the factory pattern to encapsulate the
    creation of different extractors.
    
    Args:
        intent_type (str): The type of intent (e.g., 'calendar', 'email', 'task', 'note')
        
    Returns:
        BaseEntityExtractor: An instance of the appropriate entity extractor
        
    Raises:
        ValueError: If no extractor is found for the given intent type
    """
    extractors = {
        'calendar': CalendarEntityExtractor,
        'email': EmailEntityExtractor,
        'task': TaskEntityExtractor,
        'note': NoteEntityExtractor,
    }
    
    extractor_class = extractors.get(intent_type)
    if not extractor_class:
        raise ValueError(f"No entity extractor found for intent type: {intent_type}")
    
    return extractor_class()

if __name__ == "__main__":
    # Test the entity extractors
    test_texts = {
        'calendar': "Schedule a meeting with John Smith tomorrow at 2:30 PM in the office for 1 hour",
        'email': "Send an email to john@example.com with subject: Project Update",
        'task': "Create a high priority task for Sarah to complete in 2 hours",
        'note': "Create a note about Project Status in the meeting room"
    }
    
    for intent_type, text in test_texts.items():
        print(f"\n=== Testing {intent_type.title()} Entity Extractor ===")
        print(f"Input text: '{text}'")
        
        extractor = get_entity_extractor(intent_type)
        entities = extractor.extract_entities(text)
        
        for entity in entities:
            print(f"\nType: {entity.type}")
            print(f"Value: {entity.value}")
            print(f"Confidence: {entity.confidence:.2f}")
            print(f"Position: {entity.start} to {entity.end}")
            if entity.metadata:
                print(f"Metadata: {entity.metadata}") 