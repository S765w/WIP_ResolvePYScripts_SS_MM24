#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import datetime
import DaVinciResolveScript as dvr_script

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

def export_metadata_to_csv(clips, filepath):
    """Exports metadata from clips to a CSV file."""
    if not clips:
        print("No clips found in the specified bin.")
        return
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Clip Name'] + METADATA_FIELDS)
        writer.writeheader()
        for clip_name, clip in clips.items():
            metadata = {'Clip Name': clip_name}
            metadata.update({field: clip.GetMetadata(field) for field in METADATA_FIELDS})
            writer.writerow(metadata)
    print(f"Metadata exported successfully to: {filepath}")

def main():
    resolve = dvr_script.scriptapp('Resolve')
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    media_pool = project.GetMediaPool()

    print("Enter the name of the bin where the clips are located (leave blank for root):")
    bin_name = input()
    bin = find_bin_by_name(media_pool, bin_name) if bin_name else media_pool.GetRootFolder()

    clips = {clip.GetName(): clip for clip in bin.GetClips().values()} if bin else {}
    if not clips:
        print(f"No clips found in the bin: {bin_name}")
        return

    print("Choose an option:")
    print("1: Import metadata from a CSV and update clips.")
    print("2: Export metadata from clips to a CSV.")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        csv_path = input("Enter the full path to the CSV file for importing metadata: ")
        metadata_list = import_csv_metadata(csv_path)
        apply_metadata_to_clips(clips, metadata_list)
    elif choice == '2':
        csv_path = os.path.join(os.path.expanduser('~'), 'Desktop', f'exported_metadata_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.csv')
        export_metadata_to_csv(clips, csv_path)
    else:
        print("Invalid choice. Please select either 1 or 2.")

if __name__ == '__main__':
    main()
