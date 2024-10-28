Automated File Sync and Backup Script 

This script automates the synchronisation of selected folders from a source directory and mirrors them to a NAS storage location and a backup server. It organises the files in date-based folders, detects duplicates and creates synchronisation reports.

How to Use

1. Open Visual Studio Code
- Open Visual Studio Code and load the script file (Automated File Sync and Backup.py`).

2. Edit Default Paths (Optional)
The script uses default paths for the source directory, the NAS and the backup server. If necessary, you can change these default paths at the beginning of the script:
- `default_source`: This is the source directory that contains the files you want to synchronise.
- `default_nas`: This is the NAS directory in which the files are to be synchronised.
- `default_backup`: This is the backup directory where a copy of the files will be stored outside the organisation.

For example:
```python default_source = "/Users/yourusername/path/to/source"
default_nas = "/Users/yourusername/path/to/nas"
default_backup = "/Users/yourusername/path/to/backup"


3. Run the Script
As soon as the script is loaded and the paths are defined, run the script. When prompted, the script will display the default paths for the source, NAS and backup directories.

- Enter "y": To use the default paths.
- Enter "n": To enter new paths when prompted.

4. Folder Selection
The script lists all available folders within the source directory . You will be prompted to select the folders you want to synchronise.

- Enter the numbers of the folders you want to synchronise (separated by commas). For example:


 Available folders:
 1. Projects
 2. Test Folder 1
 3. Logs
 Enter the numbers of the folders you want to copy (e.g. 1,2,3): 1,2


5 Dealing with duplicate files
If the script detects duplicate files during synchronisation, you will be asked how these should be handled:
- Enter "y": The duplicate file will be overwritten.
- Enter "n": All duplicates will be skipped.

6. Synchronisation and organisation
Once the folders are selected, the script will:
1. Organise the files into date-based folders (based on the current date).
2. Synchronise the selected files with the NAS directory.
3. Synchronise the NAS directory with the backup server to ensure that all files are safely backed up.

7. Reports and Logs
- Synchronisation logs: The script logs all synchronisation processes in a date-based log file located in the "Logs" folder of the source directory`.
- Synchronisation reports: After each synchronisation, a detailed synchronisation report is created and saved in the NAS and backup directories under the "Reports" folder.

Final Step
Check the final status of the synchronisation and backup process in the terminal or in the logs to confirm that everything has been synchronised and backed up as expected.


Troubleshooting

1. Make sure all required packages are installed
 - Watchdog: This package is required to monitor file changes. 

Install it using:

 ```bash
 pip install watchdog
 ```
 - Rsync: Used to synchronise directories. Make sure that it is also installed:

     ```bash
 brew install rsync
 ```

2. Directory permissions
 - Make sure that you have the authorisation to access and change the source, NAS and backup directories.

3. Path problems
 - If you have problems with file paths, check that the paths are correctly enclosed in inverted commas (especially if they contain spaces). Make sure that all directories are fully synchronised if you are using a cloud service such as Dropbox.

This script ensures that the files on your NAS and backup systems are synchronised consistently, ensuring efficient file management and backup.