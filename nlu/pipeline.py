from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum

class IntentType(Enum):
    CALENDAR = "calendar"
    EMAIL = "email"
    TASK = "task"
    NOTE = "note"
    UNKNOWN = "unknown"
    # think about knowledge graph
    # Obsidan API traversal
    # Notion API traversal

@dataclass
class Entity:
    type: str
    value: str
    confidence: float
    start: int
    end: int

@dataclass
class Intent:
    type: IntentType
    confidence: float
    entities: List[Entity]
    raw_text: str

@dataclass
class FunctionCall:
    name: str
    parameters: Dict[str, Any]
    confidence: float

class NLUPipeline:
    def __init__(self):
        self.intent_patterns = {
            IntentType.CALENDAR: [
                "meeting",
                "due",
            ],
            IntentType.EMAIL: [
                "email",
                "mail",
                "send",
            ],
            IntentType.TASK: [
                "task",
            ],
            IntentType.NOTE: [
                "note",
            ]
        }
        
        self.entity_types = {
            "datetime": ["when", "time", "date", "schedule"],
            "person": ["who", "with", "to"],
            "subject": ["about", "regarding", "concerning"],
            "priority": ["important", "urgent", "high priority", "low priority"]
        }

    def extract_intent(self, text: str) -> Intent:
        """
        Extract the intent from the input text.
        """
        text = text.lower()
        best_match = IntentType.UNKNOWN
        best_confidence = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    confidence = len(pattern) / len(text)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent_type
        
        return Intent(
            type=best_match,
            confidence=best_confidence,
            entities=[],
            raw_text=text
        )

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract entities from the input text.
        """
        entities = []
        words = text.lower().split()
        
        for i, word in enumerate(words):
            for entity_type, keywords in self.entity_types.items():
                if word in keywords:
                    # Look for the value in the next word
                    if i + 1 < len(words):
                        value = words[i + 1]
                        entities.append(Entity(
                            type=entity_type,
                            value=value,
                            confidence=0.8,  # Default confidence
                            start=i,
                            end=i + 1
                        ))
        
        return entities

    def map_to_function(self, intent: Intent) -> Optional[FunctionCall]:
        """
        Map the extracted intent and entities to a function call.
        """
        if intent.type == IntentType.UNKNOWN:
            return None
            
        # Create a mapping of intents to function names
        function_mapping = {
            IntentType.CALENDAR: "schedule_meeting",
            IntentType.EMAIL: "send_email",
            IntentType.TASK: "create_task",
            IntentType.NOTE: "create_note"
        }
        
        # Extract parameters from entities
        parameters = {}
        for entity in intent.entities:
            parameters[entity.type] = entity.value
            
        return FunctionCall(
            name=function_mapping[intent.type],
            parameters=parameters,
            confidence=intent.confidence
        )

    def process(self, text: str) -> Optional[FunctionCall]:
        """
        Process the input text through the entire NLU pipeline.
        """
        intent = self.extract_intent(text)
        entities = self.extract_entities(text)
        intent.entities = entities
        return self.map_to_function(intent) 
    
if __name__ == "__main__":
    pipeline = NLUPipeline()
    print(pipeline.process("Schedule a meeting with John tomorrow at 2pm"))
    