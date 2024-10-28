#!/usr/bin/env python3

import DaVinciResolveScript as dvr_script

# Function to get the DaVinci Resolve instance
def get_resolve():
    resolve = dvr_script.scriptapp('Resolve')
    if resolve is None:
        raise RuntimeError("Could not connect to DaVinci Resolve. Please ensure it is running.")
    return resolve

# Function to get the current project
def get_current_project(resolve):
    project_manager = resolve.GetProjectManager()
    current_project = project_manager.GetCurrentProject()
    if current_project is None:
        raise RuntimeError("No project is currently open in DaVinci Resolve.")
    return current_project

# Function to get all timelines from the project
def get_project_timelines(project):
    timelines = []
    timeline_count = project.GetTimelineCount()

    if timeline_count == 0:
        raise RuntimeError("No timelines found in the project.")

    for index in range(1, timeline_count + 1):  # Timeline indices start at 1
        timeline = project.GetTimelineByIndex(index)
        timelines.append(timeline)

    return timelines

# Function to rename timelines using SetName
def rename_timelines(timelines):
    print("\n=== Rename Timelines ===\n")
    for index, timeline in enumerate(timelines):
        current_name = timeline.GetName()
        print(f"Timeline {index + 1} ('{current_name}') rename to: ", end="")
        new_name = input()

        # Check if the user provided a new name
        if new_name.strip():
            try:
                # Rename the timeline using SetName()
                success = timeline.SetName(new_name)
                if success:
                    print(f"Renamed '{current_name}' to '{new_name}' successfully.")
                else:
                    print(f"Failed to rename '{current_name}'")
            except Exception as e:
                print(f"Error renaming '{current_name}': {e}")
        else:
            print(f"Skipped renaming '{current_name}'")

# Main function
def main():
    try:
        # Connect to DaVinci Resolve
        resolve = get_resolve()

        # Get the current project
        current_project = get_current_project(resolve)

        # Get all timelines from the project
        timelines = get_project_timelines(current_project)

        # Prompt the user to rename each timeline
        rename_timelines(timelines)

        print("\nTimeline renaming completed successfully.")

    except Exception as e:
        print(f"Error: {e}")

# Entry point for the script
if __name__ == '__main__':
    main()
