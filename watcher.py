# watcher.py
import os
import time
import faiss
import psutil
import pickle
import numpy as np
from watchdog.observers import Observer
from indexer import extract_text_from_file # Reuse our text extractor
from watchdog.events import FileSystemEventHandler
from sentence_transformers import SentenceTransformer

# --- CONFIGURATION (Mirrors indexer.py) ---
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
INDEX_PATH = os.path.join("index", "file_content.index")
MAP_PATH = os.path.join("index", "file_path_map.pkl")

# --- BLACKLIST (Copied directly from indexer.py for consistency) ---
BLACKLIST = {
    'node_modules', 'venv', 'Lib', 'site-packages', '.git', '.cache',
    'AppData', 'Program Files', 'ProgramData', 'Windows', '$RECYCLE.BIN',
    '__pycache__', 'env', '.gradle', 'Program Files (x86)', 'MinGW', '.vscode'
}

def update_index(file_path, action='add'):
    """Adds, updates, or removes a file from the FAISS index."""
    print(f"\n-> Event: '{action.upper()}' for file: {file_path}")
    
    try:
        index = faiss.read_index(INDEX_PATH)
        with open(MAP_PATH, "rb") as f:
            file_path_map = pickle.load(f)
    except FileNotFoundError:
        print("   [Error] Index not found. Run indexer.py to create an initial index.")
        return
    
    # Remove the old entry if it exists
    if file_path in file_path_map:
        try:
            idx_to_remove = file_path_map.index(file_path)
            index.remove_ids(np.array([idx_to_remove]))
            file_path_map.pop(idx_to_remove)
            print(f"   - Removed old index entry.")
        except Exception as e:
            print(f"   [Error] Could not remove old index entry: {e}")

    # Add the new entry if the action is not 'delete'
    if action in ['add', 'update']:
        content = extract_text_from_file(file_path)
        if content and content.strip():
            embedding = MODEL.encode(content, convert_to_tensor=False)
            embedding_np = np.array([embedding]).astype('float32')
            index.add(embedding_np)
            file_path_map.append(file_path)
            print(f"   + Added new index entry.")

    # Save the updated index and map
    faiss.write_index(index, INDEX_PATH)
    with open(MAP_PATH, "wb") as f:
        pickle.dump(file_path_map, f)
    
    print("   Index update complete.")

class MyEventHandler(FileSystemEventHandler):
    """Handles file system events, ignoring blacklisted directories."""
    
    def _is_valid_path(self, path):
        """Checks if the event path is supported and not in a blacklisted directory."""
        # Check 1: Is it a directory? Ignore it.
        if os.path.isdir(path):
            return False
        # Check 2: Is any part of the path in our blacklist? Ignore it.
        if any(f"{os.path.sep}{folder_name}{os.path.sep}" in path for folder_name in BLACKLIST):
            return False
        # Check 3: Do we have an extractor for this file type?
        if not extract_text_from_file(path):
            return False
        return True

    def on_created(self, event):
        if self._is_valid_path(event.src_path):
            update_index(event.src_path, action='add')

    def on_modified(self, event):
        if self._is_valid_path(event.src_path):
            update_index(event.src_path, action='update')

    def on_deleted(self, event):
        # We only need the path for deletion, so we don't need all checks
        if not os.path.isdir(event.src_path):
             if not any(f"{os.path.sep}{folder_name}{os.path.sep}" in event.src_path for folder_name in BLACKLIST):
                update_index(event.src_path, action='delete')

if __name__ == "__main__":
    print("Starting real-time file watcher across all drives...")
    event_handler = MyEventHandler()
    observer = Observer()
    
    # --- LOGIC TO WATCH ALL DRIVES ---
    drives_to_watch = [p.mountpoint for p in psutil.disk_partitions()]
    for path in drives_to_watch:
        try:
            observer.schedule(event_handler, path, recursive=True)
            print(f" - Watching drive: {path}")
        except Exception as e:
            print(f"   [Warning] Could not watch {path}. Error: {e}")
        
    observer.start()
    print("\nWatcher is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("\nWatcher stopped.")