# import os
# import re
# def search(x):
#     path_dir="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\"
#     l = os.listdir(path_dir)
#     if len(l) == 0:
#         path_dir
#     for a in l:
#         if (os.path.isfile(str(path_dir)+str(a.lower()))):
#             if (x in a.lower()):
#                 return True
#     return False
        
# def extreme_search(x):
#     l = os.listdir()
#     for a in l:
#         if (os.path.isfile(a)):
#             pass
#             # if (self.lower() in a):
#             if (x.lower() in a):
#                 print("File exists at", os.getcwd(),a)
#             # elif (self.upper() in a):
#             elif (x.upper() in a):
#                 print("File exists at", os.getcwd(),a)
#                 break
#         elif (os.path.isdir(a)):
#             if (a == "System Volume Information"):
#                 pass
#             elif (a == "Config.Msi"):
#                 pass
#             else:
#                 # if (self.lower() in a):
#                 if (x.lower() in a):
#                     print("Folder exists at", os.getcwd(),a)
#                 # elif (self.upper() in a):
#                 elif (x.upper() in a):
#                     print("Folder exists at", os.getcwd(),a)
#                 os.chdir(a)
#                 search()
#     os.chdir(os.pardir)
# find()
# if (__name__=="__main__"):
#     x = input("Enter file/folder name: ")
#     search(x)

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


# import os
# import fnmatch
# import multiprocessing
# cnt = 0
# def search_files_in_drive(drive, pattern, results):
#     for root, _, files in os.walk(drive):
#         for filename in files:
#             global cnt
#             print(cnt)
#             cnt += 1
#             if fnmatch.fnmatch(filename, pattern):
#                 results.append(os.path.join(root, filename))

# def search_files_in_all_drives(pattern):
#     found_files = []
#     drives = ['%s:' % d for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists('%s:' % d)]

#     with multiprocessing.Pool() as pool:
#         manager = multiprocessing.Manager()
#         results = manager.list()

#         pool.starmap(search_files_in_drive, [(drive, pattern, results) for drive in drives])

#         found_files.extend(results)

#     return found_files

# if __name__ == "__main__":
#     file_pattern = input("Enter the file pattern (e.g., *.txt): ")

#     results = search_files_in_all_drives(file_pattern)

#     if results:
#         print("Found files:")
#         for file_path in results:
#             print(file_path)
#     else:
#         print("No files matching the pattern were found.")
#     print(cnt)
