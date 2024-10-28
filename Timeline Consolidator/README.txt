Timeline Consolidator Script

This script is designed to consolidate multiple timelines in DaVinci Resolve. It provides a GUI for the user to select the timelines to consolidate and specify the handle length.


Timeline Selection: The script provides a GUI pop-up menu for the user to select the timelines to consolidate. The user can select multiple timelines by checking the boxes next to the timeline names.

Handle Length: The user can specify the handle length in the GUI. The handle length is the number of frames to add to the start and end of each clip in the consolidated timeline.

Source Sequence Name: The user can specify the name of the new source sequence in the GUI. The source sequence is the timeline that the selected timelines will be consolidated into.


How to Use

Ensure DaVinci Resolve is open before running the script.
Run the script in a Python environment using Visual Studio Code
A GUI pop-up menu will appear. Select the timelines to consolidate by checking the boxes next to the timeline names.
Enter the handle length in the corresponding field.
Enter the name of the source sequence in the corresponding field.
Click "OK" to start the consolidation process. If you want to cancel the operation, click “Cancel”.

A new timeline is created with a name based on the current date..