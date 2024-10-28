#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import DaVinciResolveScript as dvr_script

# List of all the metadata fields we want to clear
METADATA_FIELDS = [
    'Description', 'Comments', 'Keywords', 'Scene', 'Shot', 'Take', 'Angle',
    'Resolution', 'Frame Rate (FPS)', 'Duration', 'Start Timecode', 'End Timecode',
    'Audio Channels', 'Audio Sample Rate', 'Bit Depth', 'Color Space', 'Codec',
    'File Path', 'Proxy', 'Proxy Media Path', 'Format', 'Creation Date', 
    'Modified Date', 'User Fields'
]

def find_bin_by_name(media_pool, bin_name):
    """Recursively search for a bin by name and return it."""
    def recurse_bins(folder):
        for subfolder in folder.GetSubFolders().values():
            if subfolder.GetName() == bin_name:
                return subfolder
            result = recurse_bins(subfolder)
            if result:
                return result
        return None
    return recurse_bins(media_pool.GetRootFolder())

def reset_metadata_for_clips(clips):
    """Resets all metadata fields for each clip by setting them to an empty string."""
    for clip_name, clip in clips.items():
        for field in METADATA_FIELDS:
            if clip.SetMetadata(field, ""):  # Setting metadata field to empty string
                print(f"Metadata field '{field}' cleared for clip: {clip_name}")
            else:
                print(f"Failed to clear metadata field '{field}' for clip: {clip_name}")

def main():
    resolve = dvr_script.scriptapp('Resolve')
    if not resolve:
        print("Error: Could not connect to DaVinci Resolve.")
        return

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        print("Error: Could not get project manager.")
        return

    project = project_manager.GetCurrentProject()
    if not project:
        print("Error: Could not get current project.")
        return

    media_pool = project.GetMediaPool()
    if not media_pool:
        print("Error: Could not get media pool.")
        return

    # Find the 'Source Media' bin
    source_media_bin = find_bin_by_name(media_pool, 'Source Media')
    if not source_media_bin:
        print("Error: 'Source Media' bin not found.")
        return

    # Load clips from the 'Source Media' bin
    clips = {clip.GetName(): clip for clip in source_media_bin.GetClips().values()}
    if not clips:
        print("No clips found in the 'Source Media' bin.")
        return

    # Reset metadata for all clips
    reset_metadata_for_clips(clips)

    # Success message
    print("All metadata fields have been successfully cleared for all clips in 'Source Media' bin.")

if __name__ == '__main__':
    main()
