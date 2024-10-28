# Import the necessary modules
import DaVinciResolveScript as dvr_script
import sys
import datetime

# Function to find a folder recursively
def find_folder_recursive(root_folder, folder_name):
    for folder in root_folder.GetSubFolders().values():
        if folder.GetName() == folder_name:
            return folder
        result = find_folder_recursive(folder, folder_name)
        if result is not None:
            return result
    return None

# Ensure DaVinci Resolve is open before running the script
resolve = dvr_script.scriptapp("Resolve")
if resolve is None:
    print("Please open DaVinci Resolve before running this script.")
    sys.exit()

projectManager = resolve.GetProjectManager()
if projectManager is None:
    print("Failed to get Project Manager")
    sys.exit()

# Get the current project
project = projectManager.GetCurrentProject()
if project is None:
    print("No project is currently open.")
    sys.exit()

# Check if the "Source Media" folder exists in the Master Bin
mediaPool = project.GetMediaPool()
rootFolder = mediaPool.GetRootFolder()
sourceMediaFolder = find_folder_recursive(rootFolder, "Source Media")

if sourceMediaFolder is None:
    print("Source Media folder does not exist.")
    sys.exit()

# Get the clips from the "Source Media" folder
clips = sourceMediaFolder.GetClipList()
if clips is None or len(clips) == 0:
    print("No clips in the Source Media folder")
    sys.exit()

# Generate a unique timeline name based on the current date and time
timelineName = "Timeline_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# Prepare the list of clip info dictionaries
clipInfos = [{"mediaPoolItem": clip} for clip in clips]

# Create a new timeline and append the clips
timeline = mediaPool.CreateTimelineFromClips(timelineName, clipInfos)
if timeline is None:
    print("Failed to create timeline")
    sys.exit()

print("Timeline created successfully.")