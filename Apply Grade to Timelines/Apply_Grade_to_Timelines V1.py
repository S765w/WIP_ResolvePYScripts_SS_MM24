# Import the API
import DaVinciResolveScript as dvr_script
import os
import sys

# Function to apply grade to all timeline items
def apply_grade_to_all_timeline_items(timeline, grade_mode, grade_path):
    items = timeline.GetItemListInTrack('video', 1)  # Assuming clips are on V1 track
    for item in items:
        if item:
            print(f"Applying grade {grade_path} to {item.GetName()}")
            try:
                timeline.ApplyGradeFromDRX(grade_path, grade_mode, item)
                print("Grade applied successfully.")
            except Exception as e:
                print(f"Error applying grade: {str(e)}")

# Function to apply grade to all clips in all timelines
def apply_grade_to_all_timelines(project, grade_mode, grade_path):
    timeline_count = project.GetTimelineCount()
    for i in range(1, timeline_count + 1):
        timeline_obj = project.GetTimelineByIndex(i)
        apply_grade_to_all_timeline_items(timeline_obj, grade_mode, grade_path)

# Load project
resolve = dvr_script.scriptapp("Resolve")
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

# Check if project is loaded
if not project:
    print("No project loaded.")
    sys.exit()

# Get current timeline or create a new one
timeline = project.GetCurrentTimeline()
if not timeline:
    mediaPool = project.GetMediaPool()
    timeline = mediaPool.CreateEmptyTimeline('MainTimeline')
    project.SetCurrentTimeline(timeline)

# Prompt the user to input the path of the .drx file
grade_path = input("Enter the path to the .drx file: ").strip()

# Check if the file exists
if not os.path.isfile(grade_path):
    print("File not found.")
    sys.exit()

# Set a fixed grade mode (e.g., 1 for Source Timecode aligned)
grade_mode = 1

# Prompt user for applying to current timeline or all timelines
apply_to_all = input("Do you want to apply the grade to the current timeline or all timelines? (C/A): ").strip().lower()

if apply_to_all == 'a':
    apply_grade_to_all_timelines(project, grade_mode, grade_path)
    print("Grade successfully applied to all clips in all timelines.")
else:
    # Apply grade to the current timeline
    apply_grade_to_all_timeline_items(timeline, grade_mode, grade_path)
    print("Grade successfully applied to all clips in the current timeline.")






