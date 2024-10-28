#!/usr/bin/env python3

# Import the APIs
import DaVinciResolveScript as dvr_script
import sys
import os
from time import time

# Function to check write permissions
def check_write_permission(directory):
    test_file = os.path.join(directory, "temp_test_file")
    
    try:
        with open(test_file, 'w') as f:
            f.write("Test")
        os.remove(test_file)
        return True
    except IOError:
        return False

# Ensure DaVinci Resolve is open before running the script
resolve = dvr_script.scriptapp("Resolve")
if resolve is None:
    print("Please open DaVinci Resolve before running this script.")
    sys.exit()

projectManager = resolve.GetProjectManager()
if projectManager is None:
    print("Failed to get Project Manager")
    sys.exit()

project = projectManager.GetCurrentProject()
if project is None:
    print("Failed to get Current Project")
    sys.exit()

mediaStorage = resolve.GetMediaStorage()
if mediaStorage is None:
    print("Failed to get Media Storage")
    sys.exit()

mediaPool = project.GetMediaPool()
if mediaPool is None:
    print("Failed to get Media Pool")
    sys.exit()

# Disable proxies
project.SetSetting('proxy_mode', 'off')

# Set render target directory based on user's choice
print("Choose your render format:")
print("1. ProRes")
print("2. H.264")
format_choice = input("Enter the number corresponding to your choice: ").strip()

# Get the user's home directory
home_dir = os.path.expanduser("~")

# Default render locations
default_target_location = "/Users/sasmi18/Urban Vybez AB Dropbox/Samuel S/Projects/IKEA IMC/Projects/Campaign 0001/Renders"
desktop_prores_location = os.path.join(home_dir, "Desktop/Renders/ProRes")
desktop_h264_location = os.path.join(home_dir, "Desktop/Renders/H.264")

if format_choice == "1":
    render_format = "ProRes"
    render_preset = 'ProRes 422 HQ'
    target_location = default_target_location
elif format_choice == "2":
    render_format = "H.264"
    render_preset = 'H.264 Master'
    target_location = default_target_location
else:
    print("Invalid choice.")
    sys.exit()

# Create the target directory if it does not exist
os.makedirs(target_location, exist_ok=True)

# Check write permission for the target location
if not check_write_permission(target_location):
    print(f"The specified render location {target_location} does NOT have write permissions.")
    user_input = input("Enter a new path or press Enter to use the default Desktop path: ").strip()
    
    if user_input:
        target_location = user_input
    else:
        if format_choice == "1":
            target_location = desktop_prores_location
        elif format_choice == "2":
            target_location = desktop_h264_location
    
    # Create the new target directory if it does not exist
    os.makedirs(target_location, exist_ok=True)

    # Check write permission for the new target location
    if not check_write_permission(target_location):
        print(f"The new specified render location {target_location} does NOT have write permissions. Exiting.")
        sys.exit(1)

print(f"Render location set to: {target_location}")

# Set the render preset
if not project.LoadRenderPreset(render_preset):
    print(f"Failed to load render preset: {render_preset}")
    sys.exit()

# Get the number of timelines
timeline_count = project.GetTimelineCount()
print(f"There are {timeline_count} timelines to add to Render Queue")

# Function to add timeline to render queue
def add_timeline_to_render(timeline, target_dir, timeline_name):
    # Create a path for each timeline render
    path = os.path.join(target_dir, timeline_name)

    # Render settings
    project.SetRenderSettings({
        "SelectAllFrames": 1,
        "TargetDir": path,
        "CustomName": timeline_name,
        "ExportVideo": True,
        "ExportAudio": True,
    })

    # Set the current timeline and add it to the render queue
    project.SetCurrentTimeline(timeline)
    render_job_id = project.AddRenderJob()
    
    return render_job_id

# Loop through each timeline and add it to the render queue
for i in range(1, timeline_count + 1):
    print(f"Currently adding timeline {i} to Render Queue...")
    timeline = project.GetTimelineByIndex(i)
    timeline_name = timeline.GetName()
    add_timeline_to_render(timeline, target_location, timeline_name)

# Start rendering
print("Starting rendering...")
project.StartRendering()
print("Rendering started.")

# Print a message when rendering is finished
print("Rendering finished.")


