import os

excludes = {'.py', '.com', '.zip', '.db', '__pycache__'}

def recurse_filetree(fp):
    for file in os.listdir(fp):
        if all(x not in file for x in excludes):
            command = f"zip redbean.zip {fp + file}"
            print(command)
            print(os.system(command))
            if '.' not in file[1:]:
                recurse_filetree(fp + file + '/')
recurse_filetree('./')
