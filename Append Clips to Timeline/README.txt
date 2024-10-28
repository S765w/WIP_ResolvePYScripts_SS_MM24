Append Clips to Timeline Script

This script, is designed to automate the process of creating a new timeline in DaVinci Resolve and appending all clips from the "Source Media" folder to the timeline. The timeline is given a unique name based on the current date and time.

The script includes a function which searches for the "Source Media" folder recursively in the Master Bin.

Unique Timeline Names: The script generates a unique name for each new timeline, based on the current date and time. This ensures that timelines do not override each other.

Automatic Clip Appending: The script automatically appends all clips in the "Source Media" folder to the new timeline.

How to Use

1. Ensure DaVinci Resolve is open and a project is loaded before running the script.
2. Check Your Folder Structure: Make sure that the clips you want to add to the timeline are in a folder named "Source Media" in the Master Bin.
3. Run the script in a Python environment using Visual Studio Code
4. Check the Output: If the script runs successfully, it will print "Timeline created successfully."
