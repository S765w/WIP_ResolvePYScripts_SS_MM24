Render Timelines Script 

This Python script is designed to automate the process of rendering multiple timelines in DaVinci Resolve. It provides options for the user to choose the render format and target location.
Features:

Render Multiple Timelines: The script automatically adds all timelines in the current project to the render queue.
Render Format Selection: The user can choose between ProRes and H.264 render formats or both
Render Location Selection: The script automatically disables proxies and links to the original media and renders the files with the predefined project settings. The user can specify the render location. If the specified location does not have write permissions, the user can enter a new path or use the default Desktop path.


How to Use

Ensure resolve is open before running the script
Run the script using Visual Studio Code
When prompted choose a number corresponding to your choice i.e. 1 = ProRes 2 = H.264
Files will begin rendering to default location on the server i.e.”/Users/samuel/IKEA IMC/Projects/Campaign 0001/Renders” or desktop 
