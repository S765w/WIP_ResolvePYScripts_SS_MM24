#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import DaVinciResolveScript as dvr_script

# Constants
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

def import_csv_metadata(filepath):
    """Imports metadata from a CSV file."""
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def apply_metadata_to_clips(clips, metadata_list):
    """Applies metadata to clips based on the data from the CSV."""
    for metadata in metadata_list:
        clip_name = metadata['Clip Name']
        clip = clips.get(clip_name)
        if clip:
            for key, value in metadata.items():
                if key != 'Clip Name' and key in METADATA_FIELDS:
                    clip.SetMetadata(key, value)
            print(f"Metadata updated for clip: {clip_name}")

def create_smart_bin(media_pool, name, criteria):
    """Creates a Smart Bin with the given criteria."""
    try:
        smart_bin = media_pool.CreateSmartBin(name, criteria)
        if smart_bin:
            print(f"Smart Bin '{name}' created successfully.")
        else:
            print(f"Failed to create Smart Bin '{name}'.")
    except AttributeError:
        print("Error: 'CreateSmartBin' method not found in 'media_pool'.")
    except Exception as e:
        print(f"Unexpected error when creating Smart Bin '{name}': {e}")

def generate_criteria(keyword):
    """Generates criteria for Smart Bin based on a keyword."""
    return [
        {"Property": "Keywords", "Operator": "Contains", "Value": keyword}
    ]

def organize_clips_into_smart_bins(media_pool, metadata_list):
    """Organizes clips into Smart Bins using keywords from metadata."""
    keywords_to_bins = {}
    for metadata in metadata_list:
        keywords = metadata.get('Keywords', '').split(',')
        for keyword in keywords:
            keyword = keyword.strip()
            if keyword:
                if keyword not in keywords_to_bins:
                    keywords_to_bins[keyword] = f"SmartBin_{keyword}"
    
    for keyword, bin_name in keywords_to_bins.items():
        criteria = generate_criteria(keyword)
        create_smart_bin(media_pool, bin_name, criteria)

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

    print("Enter the full path to the CSV file for importing metadata:")
    csv_path = input()
    metadata_list = import_csv_metadata(csv_path)

    if not metadata_list:
        print("No metadata found in the CSV file.")
        return

    # Apply metadata to clips
    apply_metadata_to_clips(clips, metadata_list)

    # Organize clips into Smart Bins
    organize_clips_into_smart_bins(media_pool, metadata_list)

    # Success message
    print("Metadata has been successfully applied and clips have been organized into Smart Bins.")

if __name__ == '__main__':
    main()
