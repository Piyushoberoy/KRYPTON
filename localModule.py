# local_module.py

import os
import subprocess
import platform
import psutil # You may need to install this: pip install psutil
import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np
import pygetwindow as gw
import pyperclip # For clipboard access

# --- Add this new function ---
def semantic_search(query: str, top_k: int = 5) -> list:
    """Searches for files based on the conceptual meaning of a query.

    This function leverages a pre-built FAISS index and a Sentence Transformer
    model to find files whose content is semantically similar to the user's
    search query. It acts as the "search" component of a two-part system,
    requiring an index previously created by an indexing script.

    The process involves loading the index, converting the text query into a
    numerical vector (embedding), performing a high-speed similarity search
    against the indexed files, and returning the paths of the top matches.

    Args:
        query (str): The natural language search query from the user.
        top_k (int, optional): The maximum number of relevant file paths to
            return. Defaults to 5.

    Returns:
        list: A list of strings, where each string is the absolute path to a
            relevant file. Returns a list containing a single error message
            string if the index is not found or another error occurs.
    """
    try:
        # Load the pre-built index and file path map
        script_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(script_dir, "index", "file_content.index")
        map_path = os.path.join(script_dir, "index", "file_path_map.pkl")

        index = faiss.read_index(index_path)
        with open(map_path, "rb") as f:
            file_path_map = pickle.load(f)
            
        # Initialize the same model used for indexing
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create an embedding for the user's query
        query_embedding = model.encode([query])
        
        # Search the index for the top_k most similar file embeddings
        distances, indices = index.search(query_embedding, top_k)
        
        # Map the results back to file paths
        results = [file_path_map[i] for i in indices[0]]
        return results

    except FileNotFoundError:
        return ["Index not found. Please run the indexer.py script first."]
    except Exception as e:
        return [f"An error occurred during semantic search: {e}"]

# Functions for the local module [cite: 66]
def _get_drives() -> list:
    """Gets a list of all drive mount points on the system."""
    drives = []
    for partition in psutil.disk_partitions():
        drives.append(partition.mountpoint)
    return drives

def find_files(name: str, extension: str) -> list:
    """Finds files with a given name and extension across all drives.

    This function performs a comprehensive, system-wide search for files.
    It begins by identifying all connected storage drives and then
    systematically traverses every directory on each drive. The search is
    case-insensitive for the filename.

    It is designed to be robust, automatically skipping any directories
    that the user does not have permission to read, preventing the program
    from crashing.

    Args:
        name (str): The keyword or text to search for within the filename.
            The search is case-insensitive.
        extension (str): The exact file extension to match, without the dot
            (e.g., 'pdf', 'docx').

    Returns:
        list: A list of strings, where each string is the full, absolute
            path to a matching file. If no files are found, it returns a
            list containing a single 'No matching files found.' message.
    """
    results = []
    
    # Get the list of all drives to search
    search_paths = _get_drives() 
    
    # Loop through each drive and perform the search
    for start_path in search_paths:
        print(f"\n--- Searching in drive: {start_path} ---")
        try: # Use a try-except block to handle potential permission errors
            for root, dirs, files in os.walk(start_path):
                # The print statements from your code are kept here for debugging
                # print(files) 
                for file in files:
                    # print(file) 
                    if name.lower() in file.lower() and file.endswith(f".{extension}"):
                        full_path = os.path.join(root, file)
                        print(f"Found match: {full_path}") # Added a print for immediate feedback
                        results.append(full_path)
        except PermissionError:
            print(f"Skipping {start_path} due to a permission error.")
            continue # Move to the next drive if access is denied

    return results if results else ["No matching files found."]

def _get_current_context():
    """Gathers information about the user's current activity."""
    context = {}
    try:
        # Get the title of the currently active window
        active_window = gw.getActiveWindow()
        if active_window:
            context['active_window_title'] = active_window.title

        # Get the current content of the clipboard
        context['clipboard_content'] = pyperclip.paste()
        
    except Exception as e:
        context['error'] = str(e)
        
    return context

def open_application(app_name: str) -> str:
    """Opens a local application using OS-native commands.

    This function provides a cross-platform way to launch applications by
    their common name. It automatically detects the user's operating
    system and uses the appropriate command:
    - macOS: `open -a [app_name]`
    - Windows: `start [app_name]`
    - Linux: `xdg-open [app_name]`

    This approach is generic and can handle a wide variety of applications
    without needing to know their specific executable paths.

    Args:
        app_name (str): The common name of the application to open
            (e.g., 'Notepad', 'Chrome', 'Spotify').

    Returns:
        str: A status message indicating either the successful attempt to
            open the application or the error that occurred.
    """
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            subprocess.run(["open", "-a", app_name], check=True)
            
        elif system == "Windows":
            # A dictionary for modern apps that need special commands
            windows_special_apps = {
                "camera": "microsoft.windows.camera:",
                "calculator": "calculator:",
                "photos": "ms-photos:",
                "settings": "ms-settings:",
                "store": "ms-windows-store:",
                "alarms & clock": "ms-clock:",
                # Common Desktop App Aliases
                "word": "winword.exe",
                "excel": "excel.exe",
                "powerpoint": "powerpnt.exe"
            }
            
            # Check if the requested app is in our special list
            app_lower = app_name.lower()
            if app_lower in windows_special_apps:
                # If so, use its special command
                command = windows_special_apps[app_lower]
                subprocess.run(["start", command], shell=True, check=True)
            else:
                # Otherwise, use the generic 'start' command for traditional apps
                subprocess.run(["start", "", app_name], shell=True, check=True)
            
        elif system == "Linux":
            # Using xdg-open is generally more robust on Linux
            subprocess.run(["xdg-open", app_name], check=True)
            
        return f"Successfully attempted to open {app_name}."
    except Exception as e:
        return f"Could not open {app_name}. Error: {e}"

def get_system_stats() -> dict:
    """Gets basic system stats like CPU and Memory usage.

    This function uses the 'psutil' library to retrieve real-time
    performance metrics from the operating system. It provides a quick
    snapshot of the system's current load.

    Specifically, it measures:
    - The system-wide CPU utilization as a percentage over a 1-second
      interval for accuracy.
    - The percentage of virtual memory (RAM) currently in use.

    Returns:
        dict: A dictionary containing the system's current CPU and memory
            usage percentages. For example:
            {'cpu_percent': 15.4, 'memory_percent': 62.8}
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return {
        "cpu_percent": cpu_usage,
        "memory_percent": memory_info.percent
    }
    
def unknown_command(original_command: str, error: str = "AI did not return a valid command.") -> str:
    """Handles cases where the AI couldn't interpret the command or failed"""

    # This print is helpful for you to see what went wrong with the AI call
    print(f"   [Debug Info: AI call failed with error: {error}]")
    return f"Sorry, I had trouble understanding the command: '{original_command}'"