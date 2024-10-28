Smart Bin Generator Script

This script is designed to automate the process of applying metadata to clips from importing a CSV file and organising them into Smart Bins using keywords for faster organisation in DaVinci Resolve. 

Connects to DaVinci Resolve and gets the current project and media pool.
Finds the 'Source Media' bin and loads all the clips from it.
Prompts the user to enter the path to a CSV file that contains metadata for the clips.
Applies the metadata from the CSV file to the corresponding clips.
Organises the clips into Smart Bins based on the 'Keywords' metadata field. Each unique keyword gets its own Smart Bin.


Ensure DaVinci Resolve is open and a project is loaded before running the script.
Make sure you have a project open in DaVinci Resolve with a bin named 'Source Media' that contains the clips you want to organise.
Prepare a CSV file with metadata for the clips. The CSV file should have a column named 'Clip Name' with the names of the clips, and other columns for the metadata fields you want to apply. Each row should contain the metadata for one clip. (Use the ‘Media Metadata Management Script’ if you want to automatically generate a CSV file with all the clips metadata within Resolve. Then use copy and paste the path when prompted)  
Run the script in a Python environment using Visual Studio Code
The script will prompt you to enter the full path to the CSV file.
