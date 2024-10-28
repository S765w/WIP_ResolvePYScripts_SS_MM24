Media Metadata Management Script

This Python script is designed to import and export metadata from/to clips in a DaVinci Resolve project. It gives the user the option to import and apply metadata to clips based on the data from a CSV file.
or exports metadata from clips to a CSV file. 


The script uses a list of predefined metadata fields (`METADATA_FIELDS`), which includes fields like 'Description', 'Comments', 'Keywords', 'Scene', 'Shot', 'Take', 'Angle', 'Resolution', 'Frame Rate (FPS)', 'Duration', 'Start Timecode', 'End Timecode', 'Audio Channels', 'Audio Sample Rate', 'Bit Depth', 'Colour Space', 'Codec', 'File Path', 'Proxy', 'Proxy Media Path', 'Format', 'Creation Date', 'Modified Date', 'User Fields'. These are the fields that will be imported/exported when dealing with clip metadata.
   
How to Use

1. Ensure DaVinci Resolve is open and a project is loaded before running the script.
2. When prompted, enter the name of the bin where the clips are located. Leave it blank for the root bin.
3. Choose an option: Import metadata from a CSV and update clips (1) or Export metadata from clips to a CSV (2).
4. If you chose option 1, enter the full path to the CSV file for importing metadata.
5. If you chose option 2, the script will automatically create a CSV file on your Desktop with the exported metadata.
