# ai_integrator.py

import os
import json
import inspect
import google.generativeai as genai
from dotenv import load_dotenv
import localModule

# Load the environment variables from the .env file
load_dotenv()

# Configure the GenAI model with the API key
# api_key = os.getenv("GOOGLE_API_KEY")
api_key = "AIzaSyCpeBJnGrBtoHT1e0w_4CNSuuHFYv3m__c"
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
    
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemma-3-27b-it') # Or another suitable Gemma/Gemini model

def generate_function_descriptions():
    """Dynamically generates descriptions of functions from localModule."""
    descriptions = []
    # Get all function objects from localModule
    functions = inspect.getmembers(localModule, inspect.isfunction)
    for name, func in functions:
        # Get the docstring, which describes what the function does
        if not name.startswith('_'):
            docstring = inspect.getdoc(func)
            # Format it nicely for the prompt
            descriptions.append(f"- {name}: {docstring}")
    return "\n".join(descriptions)
        
def get_ai_interpretation(command: str, context: dict) -> dict:
    """Sends a command and context to the GenAI model for interpretation."""

    # 1. Get the directory where this script (aiGenerator.py) is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Create a full, robust path to the template file
    template_path = os.path.join(script_dir, 'prompt_template.txt')
    
    # 3. Read the prompt from the external template file
    try:
        with open(template_path, 'r') as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print(f"FATAL ERROR: The prompt template was not found at {template_path}")
        # Return an error that will be handled by the main loop
        return {"function": "unknown_command", "params": {"original_command": command, "error": "Prompt template file is missing."}}

    # 4. Dynamically generate the list of available functions
    function_list = generate_function_descriptions()
    
    # 5. Format the context for the prompt
    context_str = "\n".join([f"- {key}: {value}" for key, value in context.items()])

    # 6. Assemble the final prompt
    prompt = prompt_template.format(
        context=context_str,
        functions=function_list,
        command=command
    )
    
    try:
        response = model.generate_content(prompt)
        json_response_str = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(json_response_str)
    except Exception as e:
        print(f"An error occurred while calling the AI model: {e}")
        return {
            "function": "unknown_command",
            "params": {"original_command": command, "error": str(e)}
        }