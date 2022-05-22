import os
import re
def search(x):
    path_dir="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\\"
    l = os.listdir(path_dir)
    for a in l:
        if (os.path.isfile(str(path_dir)+str(a.lower()))):
            if (x in a.lower()):
                return True
    return False
        
def extreme_search(x):
    l = os.listdir()
    for a in l:
        if (os.path.isfile(a)):
            pass
            # if (self.lower() in a):
            if (x.lower() in a):
                print("File exists at", os.getcwd(),a)
            # elif (self.upper() in a):
            elif (x.upper() in a):
                print("File exists at", os.getcwd(),a)
                break
        elif (os.path.isdir(a)):
            if (a == "System Volume Information"):
                pass
            elif (a == "Config.Msi"):
                pass
            else:
                # if (self.lower() in a):
                if (x.lower() in a):
                    print("Folder exists at", os.getcwd(),a)
                # elif (self.upper() in a):
                elif (x.upper() in a):
                    print("Folder exists at", os.getcwd(),a)
                os.chdir(a)
                search()
    os.chdir(os.pardir)
# find()
if (__name__=="__main__"):
    x = input("Enter file/folder name: ")
    search(x)