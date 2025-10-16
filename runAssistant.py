# run_assistant.py

import localModule
import aiGenerator

# --- NEW: A set of functions that should only run once and then exit the loop ---
SINGLE_SHOT_FUNCTIONS = {
    'open_application', 
    'find_files',
    'get_system_stats'
}

def execute_command_loop(user_command: str):
    """
    Handles the multi-step ReAct loop for a single user command.
    This loop continues until the AI provides a final answer.
    """
    #print(f"> {user_command}")
    
    # This list will store the history of tool calls and their results for the current command
    history = []
    
    # --- THIS IS THE FIX ---
    # Add a turn counter to prevent infinite loops
    max_turns = 2
    turn_count = 0
    
    # Start the inner "thought process" loop
    while turn_count < max_turns:
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")
        
        # 1. Gather fresh context for every step of the process
        current_context = localModule._get_current_context()
        print(f"Context: {current_context}")
        # 2. Pass the original command, context, AND history to the AI
        structured_command = aiGenerator.get_ai_interpretation(user_command, current_context, history)
        print(f"   [AI Interpretation: {structured_command}]")

        function_name = structured_command.get("function")
        params = structured_command.get("params")

        # 3. Decide what to do based on the AI's chosen function
        
        # --- EXIT CONDITION: The AI has the final answer ---
        if function_name == "answer_user":
            print(f"\n✅ Final Answer: {params.get('answer')}\n")
            break  # Exit the ReAct loop

        elif function_name == "suggest_application":
            app = params.get('app_name')
            reason = params.get('reason')
            response = input(f"   [Suggestion: {reason} Shall I open {app}? (y/n)] ")
            if response.lower() == 'y':
                result = localModule.open_application(app)
                print(f"   [Result: {result}]")
            # We break here as user interaction is a final step
            break 

        elif hasattr(localModule, function_name):
            # Call the tool (e.g., web_search)
            function_to_call = getattr(localModule, function_name)
            result = function_to_call(**params)
            print(f"   [Result: {str(result)[:500]}...]") # Print a snippet of the result
            
            # Add the result to history for the AI's next thought
            history.append(f"Observation: Your call to `{function_name}` returned the following result: {result}")
            
            # --- THIS IS THE FIX ---
            # If the function is a simple, direct action, stop the loop.
            if function_name in SINGLE_SHOT_FUNCTIONS:
                print(f"\n✅ Action '{function_name}' completed.\n")
                break
        else:
            print(f"   [Error: Function '{function_name}' not found in local module.]")
            break # Exit the loop on error

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
        
        # Start the ReAct loop for the user's command
        execute_command_loop(user_command)

if __name__ == "__main__":
    main()