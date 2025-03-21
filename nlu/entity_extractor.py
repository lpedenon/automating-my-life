from dataclasses import dataclass
from typing import List, Dict, Optional
import re
from datetime import datetime, timedelta
import dateparser
from abc import ABC, abstractmethod

@dataclass
class Entity:
    type: str
    value: str
    confidence: float
    start: int
    end: int
    metadata: Optional[Dict] = None

class BaseEntityExtractor(ABC):
    """Abstract base class for entity extraction."""
    
    def __init__(self):
        self.patterns = {}
        self.compiled_patterns = {}
        
    def compile_patterns(self):
        """Compile regex patterns for the extractor."""
        self.compiled_patterns = {
            entity_type: [re.compile(pattern) for pattern in patterns]
            for entity_type, patterns in self.patterns.items()
        }
    
    @abstractmethod
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract entities from text using regex patterns."""
        pass
    
    def _calculate_confidence(self, entity_type: str, value: str) -> float:
        """Calculate confidence score for an extracted entity."""
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
            if re.match(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)', value):
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
    """Extractor for calendar-related entities."""
    
    def __init__(self):
        super().__init__()
        self.patterns = {
            'datetime': [
                # Time patterns
                # at 2pm, 2:00pm, 2:00 PM (requires am/pm)
                r'\b(?:at\s+)?\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)\b',  # Require am/pm
                # 24 hour format (STILL DOESN'T WORK)
                # r'\b(?:at\s+)?\d{1,2}(?::\d{2})?\b',  # 24-hour format
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
        entities = []
        datetime_entities = []
        
        # First pass: collect all entities
        self._collect_entities(text, entities, datetime_entities)
        
        # Process datetime entities if found
        if datetime_entities:
            self._process_datetime_entities(datetime_entities, entities)
        
        return entities
    
    def _collect_entities(self, text: str, entities: List[Entity], datetime_entities: List[Entity]) -> None:
        for entity_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    entity = self._create_entity(entity_type, match)
                    if entity_type == 'datetime':
                        datetime_entities.append(entity)
                    else:
                        entities.append(entity)
    
    def _create_entity(self, entity_type: str, match: re.Match) -> Entity:
        value = match.group()
        start, end = match.span()
        confidence = self._calculate_confidence(entity_type, value)
        metadata = self._extract_metadata(entity_type, value)
        
        return Entity(
            type=entity_type,
            value=value,
            confidence=confidence,
            start=start,
            end=end,
            metadata=metadata
        )
    
    def _process_datetime_entities(self, datetime_entities: List[Entity], entities: List[Entity]) -> None:
        datetime_entities.sort(key=lambda x: x.start)
        combined_text = ' '.join(entity.value for entity in datetime_entities)
        parsed_date = dateparser.parse(combined_text)
        
        if parsed_date:
            metadata = self._create_combined_datetime_metadata(combined_text, parsed_date)
            combined_entity = Entity(
                type='datetime',
                value=combined_text,
                confidence=max(entity.confidence for entity in datetime_entities),
                start=datetime_entities[0].start,
                end=datetime_entities[-1].end,
                metadata=metadata
            )
            entities.append(combined_entity)
        else:
            entities.extend(datetime_entities)
    
    def _create_combined_datetime_metadata(self, combined_text: str, parsed_date: datetime) -> Dict:
        metadata = {
            'original': combined_text,
            'parsed': parsed_date,
            'type': 'absolute' if 'at' in combined_text.lower() or re.match(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)', combined_text) else 'relative',
            'human_readable': None
        }
        
        day_suffix = self._get_day_suffix(parsed_date.day)
        metadata['human_readable'] = parsed_date.strftime(f"%B %d{day_suffix}, %Y at %I:%M %p")
        return metadata
    
    def _get_day_suffix(self, day: int) -> str:
        if day % 10 == 1 and day != 11:
            return "st"
        elif day % 10 == 2 and day != 12:
            return "nd"
        elif day % 10 == 3 and day != 13:
            return "rd"
        return "th"
    
    def _extract_metadata(self, entity_type: str, value: str) -> Optional[Dict]:
        if entity_type == 'datetime':
            return self._parse_datetime(value)
        return None
    
    def _parse_datetime(self, value: str) -> Dict:
        metadata = {
            'original': value,
            'parsed': None,
            'type': None,
            'human_readable': None
        }
        
        parsed_date = dateparser.parse(value)
        
        if parsed_date:
            metadata['parsed'] = parsed_date
            metadata['type'] = 'absolute' if 'at' in value.lower() or re.match(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)', value) else 'relative'
            
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
    """Extractor for email-related entities."""
    
    def __init__(self):
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
    """Extractor for task-related entities."""
    
    def __init__(self):
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
    """Extractor for note-related entities."""
    
    def __init__(self):
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

# Factory function to get the appropriate extractor
def get_entity_extractor(intent_type: str) -> BaseEntityExtractor:
    """Factory function to get the appropriate entity extractor based on intent type."""
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