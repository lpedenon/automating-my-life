import sys
from typing import Optional
from nlu import NLUPipeline, IntentType, Entity, FunctionCall

def print_intent_info(intent) -> None:
    """Print detailed information about the extracted intent."""
    print("\n=== Intent Information ===")
    print(f"Type: {intent.type.value}")
    print(f"Confidence: {intent.confidence:.2f}")
    print(f"Raw Text: {intent.raw_text}")
    print(f"Number of Entities: {len(intent.entities)}")

def print_entity_info(entity: Entity) -> None:
    """Print detailed information about an entity."""
    print(f"\n  Entity Type: {entity.type}")
    print(f"  Value: {entity.value}")
    print(f"  Confidence: {entity.confidence:.2f}")
    print(f"  Position: {entity.start} to {entity.end}")

def print_function_call_info(function_call: Optional[FunctionCall]) -> None:
    """Print detailed information about the function call."""
    print("\n=== Function Call Information ===")
    if function_call is None:
        print("No function call generated (unknown intent)")
        return
    
    print(f"Function Name: {function_call.name}")
    print(f"Confidence: {function_call.confidence:.2f}")
    print("\nParameters:")
    for param_name, param_value in function_call.parameters.items():
        print(f"  {param_name}: {param_value}")

def print_pipeline_info(text: str, pipeline: NLUPipeline) -> None:
    """Print detailed information about the entire pipeline process."""
    print("\n=== Input Text ===")
    print(f"'{text}'")
    
    # Extract and print intent information
    intent = pipeline.extract_intent(text)
    print_intent_info(intent)
    
    # Extract and print entity information
    print("\n=== Entity Information ===")
    entities = pipeline.extract_entities(text)
    if entities:
        for entity in entities:
            print_entity_info(entity)
    else:
        print("No entities found")
    
    # Map to function and print function call information
    intent.entities = entities
    function_call = pipeline.map_to_function(intent)
    print_function_call_info(function_call)

def main():
    """Main CLI interface for testing the NLU pipeline."""
    pipeline = NLUPipeline()
    
    print("=== NLU Pipeline Test Interface ===")
    print("Type 'exit' to quit")
    print("Type 'help' to see available commands")
    
    while True:
        try:
            text = input("\nEnter text to process: ").strip()
            
            if text.lower() == 'exit':
                print("\nGoodbye!")
                break
            elif text.lower() == 'help':
                print("\nAvailable Commands:")
                print("  exit  - Exit the program")
                print("  help  - Show this help message")
                print("\nExample Inputs:")
                print("  - schedule a meeting with John tomorrow at 2pm")
                print("  - send an email to Sarah about the project status")
                print("  - create a task about implementing the new feature")
                continue
            
            if not text:
                print("Please enter some text to process")
                continue
            
            print_pipeline_info(text, pipeline)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again or type 'exit' to quit")

if __name__ == "__main__":
    main() 