import os
import fnmatch
cnt = 0
def search_files_in_all_drives(pattern):
    found_files = []

    # On Windows, drives are represented as letters (e.g., C:, D:)
    drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]
    for drive in drives:
        for root, dirs, files in os.walk(drive):
            # print(root, ",", dirs)
            # print(files)
            global cnt
            print(cnt)
            cnt += 1
            
            for filename in fnmatch.filter(files, pattern):
                found_files.append(os.path.join(root, filename))

    return found_files

if __name__ == "__main__":
    file_pattern = input("Enter the file pattern (e.g., *.txt): ")

    results = search_files_in_all_drives(file_pattern)

    if results:
        print("Found files:")
        for file_path in results:
            print(file_path)
    else:
        print("No files matching the pattern were found.")

