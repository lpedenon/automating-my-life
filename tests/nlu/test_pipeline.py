import pytest
from nlu import NLUPipeline, IntentType, Entity, FunctionCall

@pytest.fixture
def pipeline():
    return NLUPipeline()

def test_extract_intent_schedule_meeting(pipeline):
    # Test various ways of expressing meeting scheduling intent
    test_cases = [
        "schedule a meeting",
        "set up a meeting with John",
        "book a meeting for tomorrow",
        "arrange a meeting with the team"
    ]
    
    for text in test_cases:
        intent = pipeline.extract_intent(text)
        assert intent.type == IntentType.CALENDAR
        assert intent.confidence > 0
        assert intent.raw_text == text.lower()

def test_extract_intent_send_email(pipeline):
    # Test various ways of expressing email sending intent
    test_cases = [
        "send an email",
        "write an email to Sarah",
        "compose an email about the project",
        "draft an email to the team"
    ]
    
    for text in test_cases:
        intent = pipeline.extract_intent(text)
        assert intent.type == IntentType.SEND_EMAIL
        assert intent.confidence > 0
        assert intent.raw_text == text.lower()

def test_extract_intent_unknown(pipeline):
    # Test handling of unknown intents
    test_cases = [
        "random text",
        "do something",
        "hello world",
        "what's the weather?"
    ]
    
    for text in test_cases:
        intent = pipeline.extract_intent(text)
        assert intent.type == IntentType.UNKNOWN
        assert intent.confidence == 0.0
        assert intent.raw_text == text.lower()

def test_extract_entities_datetime(pipeline):
    # Test datetime entity extraction
    text = "schedule a meeting tomorrow at 2pm"
    entities = pipeline.extract_entities(text)
    
    datetime_entities = [e for e in entities if e.type == "datetime"]
    assert len(datetime_entities) > 0
    assert "tomorrow" in [e.value for e in datetime_entities]

def test_extract_entities_person(pipeline):
    # Test person entity extraction
    text = "send an email to John about the project"
    entities = pipeline.extract_entities(text)
    
    person_entities = [e for e in entities if e.type == "person"]
    assert len(person_entities) > 0
    assert "John" in [e.value for e in person_entities]

def test_extract_entities_subject(pipeline):
    # Test subject entity extraction
    text = "create a task about the new feature"
    entities = pipeline.extract_entities(text)
    
    subject_entities = [e for e in entities if e.type == "subject"]
    assert len(subject_entities) > 0
    assert "feature" in [e.value for e in subject_entities]

def test_map_to_function_schedule_meeting(pipeline):
    # Test function mapping for meeting scheduling
    intent = Intent(
        type=IntentType.CALENDAR,
        confidence=0.8,
        entities=[
            Entity(type="datetime", value="tomorrow", confidence=0.8, start=0, end=1),
            Entity(type="person", value="John", confidence=0.8, start=0, end=1)
        ],
        raw_text="schedule a meeting with John tomorrow"
    )
    
    function_call = pipeline.map_to_function(intent)
    assert function_call is not None
    assert function_call.name == "schedule_meeting"
    assert "datetime" in function_call.parameters
    assert "person" in function_call.parameters
    assert function_call.confidence == 0.8

def test_map_to_function_unknown_intent(pipeline):
    # Test function mapping for unknown intent
    intent = Intent(
        type=IntentType.UNKNOWN,
        confidence=0.0,
        entities=[],
        raw_text="random text"
    )
    
    function_call = pipeline.map_to_function(intent)
    assert function_call is None

def test_full_pipeline_process(pipeline):
    # Test the complete pipeline process
    test_cases = [
        {
            "input": "schedule a meeting with John tomorrow at 2pm",
            "expected_function": "schedule_meeting",
            "expected_params": ["datetime", "person"]
        },
        {
            "input": "send an email to Sarah about the project status",
            "expected_function": "send_email",
            "expected_params": ["person", "subject"]
        },
        {
            "input": "create a task about implementing the new feature",
            "expected_function": "create_task",
            "expected_params": ["subject"]
        }
    ]
    
    for case in test_cases:
        result = pipeline.process(case["input"])
        assert result is not None
        assert result.name == case["expected_function"]
        for param in case["expected_params"]:
            assert param in result.parameters
        assert result.confidence > 0

def test_pipeline_edge_cases(pipeline):
    # Test edge cases and error handling
    test_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "schedule",  # Incomplete intent
        "with John",  # Only entity
        "random text with meeting",  # Intent word in wrong context
    ]
    
    for text in test_cases:
        result = pipeline.process(text)
        if result is not None:
            assert result.confidence > 0
            assert result.name in ["schedule_meeting", "send_email", "create_task", "create_note"] 