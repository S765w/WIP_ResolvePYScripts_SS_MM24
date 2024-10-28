This script is designed to automate the process of setting up a new project in DaVinci Resolve. It allows the user to select or customise any predefined project template with ready made project settings so that the user does not have to do any manual adjustments when starting or delivering a new project.   The scripts works within a python environment and interacts with DaVinci Resolve's API. The script functions based on set folder structures and valid file path directories. i.e. IKEA IMC SERVER/Projects/Campaign 0001/DR Project Templates/Custom Template V1.drp"

How to Use

Ensure resolve is open before running the script 
1.Select a Template

Custom /  Dolby Vision / Other   * Depending on the users selection. The script will automatically load a .drp project file from the project templates folder on the server. The project will automatically load with its predefined project settings. i.e. IKEA IMC SERVER/Projects/Campaign 0001/DR Project Templates/Custom Template V1.drp” if the user selects ‘Other’ they will be prompted to enter the path to the .drp file of their choice. 

2.Enter Your Project Name 

*A new .drp project file will automatically be saved to a project files folder on the server i.e. IKEA IMC SERVER/Projects/Campaign 0001/Project Files / YourProject’ 
Confirm Project Path
 The user can confirm the default directory to the source media files or choose a new path. 
Import Media Files
 The files will automatically be imported into predefined bins within the new project ready for the user to begin editing. 