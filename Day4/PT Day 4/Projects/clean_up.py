import os
folder="Temp_files"
for file in os.listdir(folder):
    os.remove(os.path.join(folder,file))
print("Folder cleaned")