  Automated Proxy Creation Script

This script automates the creation of proxy files from high-resolution media and organises them in date-based folders. Once the proxies are created, it synchronises them with a specified NAS location. It also recognises duplicate files and provides options for handling them.

How to Use

1. 1. Ensure DaVinci Resolve is open and a project is loaded before running the script.


Open in Visual Studio Code:
 - Open Visual Studio Code and load the script file (`Automated_Proxy_Creation.py`).

2. Edit default paths (optional):
The script uses default paths for source media, proxy storage and NAS location. If you need to update these paths, edit the following variables at the beginning of the script:
 - `default_source_media_path`
 - `Standard_Proxy_Storage_Path`
 - `Standard_NAS_location`


3. When prompted the script displays the default paths for source media, proxy storage and NAS location.
Type `y`: Use the default paths.
Type `n`: Enter new paths when prompted.

4. If duplicate files are found, the script will prompt you:
Type `y`: Overwrite the duplicate file.
Type `n`: Skip all duplicates.

5. Once the proxies are generated, they are organised into date-based folders.
The script will then synchronise the proxies with the NAS location.
Check the final status of the proxy creation and synchronisation.