import os
import fnmatch

def search(pattern):
    found_files = []

    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for filename in fnmatch.filter(files, pattern):
                found_files.append(os.path.join(root, filename))

    return found_files

if __name__ == "__main__":
    file_pattern = input("Enter the file pattern (e.g., *.txt): ")

    results = search(file_pattern)

    if results:
        print("Found files:")
        for file_path in results:
            print(file_path)
    else:
        print("No files matching the pattern were found.")

