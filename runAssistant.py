# run_assistant.py

import localModule
import aiGenerator

def main():
    """
    Main function to run the command-line interface for the assistant.
    """
    print("Personal Assistant CLI started. Type 'exit' to quit.")
    
    while True:
        # Get command from user input
        user_command = input("> ")

        if user_command.lower() in ["exit", "quit"]:
            print("Exiting assistant. Goodbye!")
            break
        
        # 1. GATHER CONTEXT before calling the AI
        current_context = localModule._get_current_context()
        
        # 2. Pass the command AND context to the AI
        structured_command = aiGenerator.get_ai_interpretation(user_command, current_context)
        print(f"   [AI Interpretation: {structured_command}]")

        # 3. Handle the new 'suggest_application' function
        function_name = structured_command.get("function")
        params = structured_command.get("params")
        
        if function_name == "suggest_application":
            app = params.get('app_name')
            reason = params.get('reason')
            # Ask the user for confirmation
            response = input(f"   [Suggestion: {reason} Shall I open {app}? (y/n)] ")
            if response.lower() == 'y':
                result = localModule.open_application(app)
                print(f"   [Result: {result}]")
        elif hasattr(localModule, function_name):
            # The Core Engine calls the function from the module [cite: 67]
            function_to_call = getattr(localModule, function_name)
            result = function_to_call(**params)
            print(f"   [Result: {result}]")
        else:
            print(f"   [Error: Function '{function_name}' not found in local module.]")

if __name__ == "__main__":
    main()