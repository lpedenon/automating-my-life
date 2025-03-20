from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
import yaml
from pathlib import Path
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from nlu.entity_extractor import Entity, get_entity_extractor

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
class Intent:
    type: IntentType
    confidence: float
    entities: List[Entity]
    raw_text: str
    matched_pattern: Optional[str] = None
    pattern_weight: Optional[float] = None

@dataclass
class FunctionCall:
    name: str
    parameters: Dict[str, Any]
    confidence: float

class NLUPipeline:
    def __init__(self, config_path: str = None):
        """Initialize NLU pipeline with configuration.
        
        Args:
            config_path: Path to intent configuration file
        """
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "intents.yaml"
            
        self.config = self._load_config(config_path)
        self.intent_patterns = self._build_intent_patterns()
        self.entity_extractors = {}  # Cache for entity extractors

    def _load_config(self, config_path: str) -> Dict:
        """Load intent configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def _build_intent_patterns(self) -> Dict[IntentType, List[Tuple[str, float]]]:
        """Build intent patterns from configuration with weights."""
        patterns = {}
        for intent_name, intent_data in self.config['intents'].items():
            try:
                intent_type = IntentType[intent_name.upper()]
                patterns[intent_type] = [
                    (pattern['keyword'], pattern['weight'])
                    for pattern in intent_data['patterns']
                ]
            except KeyError:
                print(f"Warning: Invalid intent type '{intent_name}' in configuration")
        return patterns

    def _get_entity_extractor(self, intent_type: str):
        """Get or create an entity extractor for the given intent type."""
        if intent_type not in self.entity_extractors:
            self.entity_extractors[intent_type] = get_entity_extractor(intent_type)
        return self.entity_extractors[intent_type]

    def extract_intent(self, text: str) -> Intent:
        """
        Extract the intent from the input text using weighted pattern matching.
        """
        text = text.lower()
        best_match = IntentType.UNKNOWN
        best_confidence = 0.0
        best_pattern = None
        best_weight = 0.0
        
        for intent_type, patterns in self.intent_patterns.items():
            # TODO: Logic is not correct, add a summation of weights instead
            for pattern, weight in patterns:
                if pattern in text:
                    # Calculate confidence based on pattern length and weight
                    pattern_confidence = len(pattern) / len(text)
                    weighted_confidence = pattern_confidence * weight
                    
                    if weighted_confidence > best_confidence:
                        best_confidence = weighted_confidence
                        best_match = intent_type
                        best_pattern = pattern
                        best_weight = weight
        
        return Intent(
            type=best_match,
            confidence=best_confidence,
            entities=[],
            raw_text=text,
            matched_pattern=best_pattern,
            pattern_weight=best_weight
        )

    def extract_entities(self, text: str, intent_type: str) -> List[Entity]:
        """Extract entities from text based on intent type.
        
        Args:
            text (str): The input text to extract entities from
            intent_type (str): The type of intent to use for entity extraction
            
        Returns:
            List[Entity]: List of extracted entities relevant to the intent type
        """
        return self._get_entity_extractor(intent_type).extract_entities(text)

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
            # Add metadata if available
            if entity.metadata:
                parameters[f"{entity.type}_metadata"] = entity.metadata
            
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
        entities = self.extract_entities(text, intent.type.value)
        intent.entities = entities
        return self.map_to_function(intent)
    
if __name__ == "__main__":
    # Test the pipeline
    pipeline = NLUPipeline()
    
    # Example input
    text = "Schedule a meeting with John Smith tomorrow at 2:30 PM in the office for 1 hour"
    
    print("\n=== Input Text ===")
    print(f"'{text}'")
    
    # Process through pipeline
    intent = pipeline.extract_intent(text)
    entities = pipeline.extract_entities(text, intent.type.value)
    intent.entities = entities
    function_call = pipeline.map_to_function(intent)
    
    print("\n=== Intent Information ===")
    print(f"Type: {intent.type.value}")
    print(f"Confidence: {intent.confidence:.2f}")
    print(f"Matched Pattern: {intent.matched_pattern}")
    print(f"Pattern Weight: {intent.pattern_weight}")
    print(f"Raw Text: {intent.raw_text}")
    print(f"Number of Entities: {len(entities)}")
    
    print("\n=== Entity Information ===")
    for entity in entities:
        print(f"\nEntity Type: {entity.type}")
        print(f"Value: {entity.value}")
        print(f"Confidence: {entity.confidence:.2f}")
        print(f"Position: {entity.start} to {entity.end}")
        if entity.metadata:
            print(f"Metadata: {entity.metadata}")
            if entity.type == 'datetime' and entity.metadata.get('human_readable'):
                print(f"Human Readable: {entity.metadata['human_readable']}")
    
    print("\n=== Function Call Information ===")
    if function_call:
        print(f"Function Name: {function_call.name}")
        print(f"Confidence: {function_call.confidence:.2f}")
        print("\nParameters:")
        for param_name, param_value in function_call.parameters.items():
            print(f"  {param_name}: {param_value}")
    else:
        print("No function call mapped")
    