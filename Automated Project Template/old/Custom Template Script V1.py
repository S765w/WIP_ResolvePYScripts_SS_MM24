

#!/usr/bin/env python

# Import the API
import DaVinciResolveScript as dvr_script
import sys
import os
import shutil

# Ensure DaVinci Resolve is open before running the script
resolve = dvr_script.scriptapp("Resolve")
if resolve is None:
    print("Please open DaVinci Resolve before running this script.")
    sys.exit()

projectManager = resolve.GetProjectManager()
if projectManager is None:
    print("Failed to get Project Manager")
    sys.exit()

# Prompt user to verify the folder structures
print("Please ensure your folder structures are correct before proceeding.")

# Function to get a valid path from the user
def get_valid_path(prompt, default_path=None):
    while True:
        path = input(prompt).strip()
        if path == "" and default_path:
            path = default_path
        if os.path.exists(path):
            return path
        else:
            print("Invalid path. Please enter a valid path.")

# 1. Prompt the user to enter the path to any template .drp file
templateFile = get_valid_path("Please enter the path to your template .drp file: ")

# 2. Ask for a Project Name and set a project filename
projectName = input('Enter Your Project Name: ').strip()
projectFile = os.path.join(os.path.dirname(templateFile), projectName + '.drp')

# 3. Make a copy of the project template with the new project filename
shutil.copy2(templateFile, projectFile)

# Move the new project file to the specified location
new_project_location = '/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Project Files'
new_project_path = os.path.join(new_project_location, projectName + '.drp')
shutil.move(projectFile, new_project_path)

# 4. Import the project that we just moved
if not projectManager.ImportProject(new_project_path):
    print(f"Failed to import project: {new_project_path}")
    sys.exit()

# 5. Load the project we just created
project = projectManager.LoadProject(projectName)
if project is None:
    print(f"Unable to load project: {projectName}")
    sys.exit()

# 6. Get mediaPool and mediaStorage Objects
mediaPool = project.GetMediaPool()
if mediaPool is None:
    print("Failed to get Media Pool")
    sys.exit()

mediaStorage = resolve.GetMediaStorage()
if mediaStorage is None:
    print("Failed to get Media Storage")
    sys.exit()

# Function to recursively find the "Source Media" folder
def find_folder_recursive(rootFolder, targetFolderName):
    if rootFolder.GetName() == targetFolderName:
        return rootFolder
    for folder in rootFolder.GetSubFolderList():
        foundFolder = find_folder_recursive(folder, targetFolderName)
        if foundFolder:
            return foundFolder
    return None

# 7. Check if the "Source Media" folder exists in the Master Bin
rootFolder = mediaPool.GetRootFolder()
sourceMediaFolder = find_folder_recursive(rootFolder, "Source Media")

if sourceMediaFolder is None:
    print("Source Media folder does not exist.")
    sys.exit()

# 8. Ask for the location of Clips from an external drive
mp = get_valid_path("Please enter the path location of your clips (e.g., /Volumes/A020/Media Assets/Footage): ")
clips = mediaStorage.AddItemListToMediaPool(mp)
if clips is None:
    print("Failed to add clips to Media Pool")
    sys.exit()

# Move clips to the "Source Media" folder
for clip in clips:
    mediaPool.MoveClips([clip], sourceMediaFolder)

# Function to import files to a specific folder
def import_to_folder(mediaPool, folderName, folderPath):
    items = mediaStorage.AddItemListToMediaPool(folderPath)
    if items is None:
        print(f"Failed to add {folderName} files to Media Pool")
        return
    folder = find_folder_recursive(rootFolder, folderName)
    if folder is None:
        print(f"{folderName} folder does not exist.")
        return
    for item in items:
        mediaPool.MoveClips([item], folder)
    print(f"{folderName} files successfully imported.")

# 9. Ask the user if they want to import more files into additional folders
additional_folders = {
    "1": {"name": "SFX", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/SFX"},
    "2": {"name": "Graphics", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Graphics"},
    "3": {"name": "Logo", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Logo"},
    "4": {"name": "Sound", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Sound"},
    "5": {"name": "Refs", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Refs"},
    "6": {"name": "Subtitles", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Subtitles"},
    "7": {"name": "Stills", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Stills"},
    "8": {"name": "VFX", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/VFX"},
    "9": {"name": "Proxies", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Source Media/Proxies"},
    "10": {"name": "Timelines", "path": "/Volumes/A020/Media Storage Drive_Temp Location/2024/Projects/Campaign 0001/Project Files/Timelines"}
}

folder_list = "\n".join([f"{key}. {folder['name']}" for key, folder in additional_folders.items()])

while True:
    more_files = input(f"Do you want to import more files into any of the following folders? (y/n): \n{folder_list}\n").strip().lower()
    if more_files == 'n':
        print("Project setup completed successfully.")
        break
    elif more_files == 'y':
        folder_choice = input("Please select a folder (1-10): ").strip()
        if folder_choice in additional_folders:
            folder = additional_folders[folder_choice]
            use_default = input(f"Do you want to use the default path for {folder['name']}? (y/n): ").strip().lower()
            if use_default == 'y':
                folderPath = folder['path']
            else:
                folderPath = get_valid_path(f"Please enter the path for {folder['name']} (default: {folder['path']}): ", folder['path'])
            import_to_folder(mediaPool, folder["name"], folderPath)
        else:
            print("Invalid choice.")
    else:
        print("Invalid input. Please enter 'y' or 'n'.")