Reset Metadata Fields Script

This Python script is designed to interact with DaVinci Resolve’s API. 

The script allows the user to reset all metadata fields for clips in a DaVinci Resolve project.

The script searches for and clears all data from the fields which include 'Description', 'Comments', 'Keywords', 'Scene', 'Shot', 'Take', 'Angle', 'Resolution', 'Frame Rate (FPS)', 'Duration', 'Start Timecode', 'End Timecode', 'Audio Channels', 'Audio Sample Rate', 'Bit Depth', 'Colour Space', 'Codec', 'File Path', 'Proxy', 'Proxy Media Path', 'Format', 'Creation Date', 'Modified Date', 'User Fields'.


How to Use

1. Ensure DaVinci Resolve is open and a project is loaded before running the script.
2. The script will automatically look for a bin named 'Source Media'.
3. The script will then clear the metadata fields defined in `METADATA_FIELDS` for all clips in the 'Source Media' bin. 
