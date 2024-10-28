#!/usr/bin/env python3

import os
import sys
import shutil  # Make sure shutil is imported
import subprocess
import logging
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Global variable to handle skipping all duplicates
skip_all_duplicates = False

# Check if required Python modules are installed
try:
    import watchdog
except ImportError:
    print("'watchdog' is not installed. Please install it using pip.")
    print("To install 'watchdog' with pip, run: `pip install watchdog`.")
    sys.exit(1)

# Check if rsync is installed
if shutil.which("rsync") is None:
    print("'rsync' is not installed. Please install it using Homebrew or another package manager.")
    print("To install 'rsync' with Homebrew, run: `brew install rsync`.")
    sys.exit(1)

# Get the current user's home directory dynamically
user_home_directory = os.path.expanduser("~")

# Set up base paths using the dynamic user home directory
default_source = os.path.join(user_home_directory, "Library/CloudStorage/Dropbox-UrbanVybezAB/Samuel S/Projects/IKEA IMC/Silverstack Test")
default_nas = os.path.join(user_home_directory, "Library/CloudStorage/Dropbox-UrbanVybezAB/Samuel S/Projects/IKEA IMC/NAS Test")
default_backup = os.path.join(user_home_directory, "Library/CloudStorage/Dropbox-UrbanVybezAB/Samuel S/Projects/IKEA IMC/Backup Test")

log_base_path = os.path.join(default_source, "Logs")
report_base_path = os.path.join(default_nas, "Reports")
backup_report_base_path = os.path.join(default_backup, "Reports")

# Create date-based folder for logs
log_date_folder = datetime.now().strftime('%Y-%m-%d')
log_folder_path = os.path.join(log_base_path, log_date_folder)

if not os.path.exists(log_folder_path):
    os.makedirs(log_folder_path)

# Set up logging
log_file_path = os.path.join(log_folder_path, "sync_log.txt")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Function to list and select folders in a directory
def list_and_select_folders(directory_path):
    """List all folders in a directory and allow the user to select by number."""
    try:
        folders = [f for f in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, f))]
        if not folders:
            print("No folders found in the directory.")
            return []
        
        # Display numbered options
        print("\nAvailable folders:")
        for i, folder in enumerate(folders):
            print(f"{i + 1}. {folder}")
        
        # Allow user to select folders
        selected_numbers = input("Enter the numbers of the folders you want to copy (comma-separated, e.g., 1,2,3): ").split(",")
        selected_folders = [folders[int(num.strip()) - 1] for num in selected_numbers if num.strip().isdigit()]
        return selected_folders
    except Exception as e:
        print(f"Error listing folders: {e}")
        return []

# Function to organize files into date-based folders
def organize_files_by_date(file_path, target_folder):
    """Organize files into date-based folders."""
    date_folder = datetime.now().strftime('%Y-%m-%d')
    date_folder_path = os.path.join(target_folder, date_folder)

    if not os.path.exists(date_folder_path):
        os.makedirs(date_folder_path)

    new_file_path = os.path.join(date_folder_path, os.path.basename(file_path))
    return new_file_path

# Function to mirror the source directory to the target directory
def sync_directories(source_folder, target_folder):
    """Sync source folder to target folder using rsync."""
    try:
        sync_command = f"rsync -avh --delete '{source_folder}/' '{target_folder}/'"
        logging.info(f"Running sync command: {sync_command}")
        result = subprocess.run(sync_command, shell=True, check=True, capture_output=True)
        sync_output = result.stdout.decode()
        logging.info(f"Successfully synchronized from {source_folder} to {target_folder}.\n{sync_output}")
        print(f"Successfully synchronized from {source_folder} to {target_folder}.")
        return sync_output
    except subprocess.CalledProcessError as e:
        error_message = f"Error during synchronization: {e.stderr.decode()}"
        logging.error(error_message)
        print(error_message)
        return error_message

# Function to handle duplicate files
def handle_duplicates(file_path, destination_folder):
    """Check and handle duplicates before copying files."""
    global skip_all_duplicates

    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, file_name)

    if os.path.exists(destination_path):
        if skip_all_duplicates:
            logging.info(f"Skipping {file_name} (duplicate) due to previous 'skip all' decision.")
            return False  # Skip the file

        choice = input(f"Duplicate found: {file_name} already exists in {destination_folder}. Overwrite? (y/n/skip all): ").lower()
        if choice == 'n':
            logging.info(f"Skipping {file_name}.")
            return False
        elif choice == 'skip all':
            skip_all_duplicates = True
            logging.info(f"Skipping all future duplicates.")
            return False
        elif choice == 'y':
            logging.info(f"Overwriting {file_name}.")
            return True
        else:
            logging.info(f"Invalid choice. Skipping {file_name}.")
            return False

    return True

# Function to generate a sync report
def generate_report(report_data, report_folder):
    """Generate a report with details of the sync process."""
    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    report_date_folder = datetime.now().strftime('%Y-%m-%d')
    report_folder_path = os.path.join(report_folder, report_date_folder)

    if not os.path.exists(report_folder_path):
        os.makedirs(report_folder_path)

    report_timestamp = datetime.now().strftime('%H-%M-%S')
    report_file_path = os.path.join(report_folder_path, f"sync_report_{report_timestamp}.txt")
    
    try:
        with open(report_file_path, 'w') as report_file:
            report_file.write("Synchronization Report\n")
            report_file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write("="*50 + "\n")
            report_file.write(report_data)
        logging.info(f"Report generated at: {report_file_path}")
        print(f"Report generated at: {report_file_path}")
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")
        print(f"Failed to generate report: {e}")

# Class to watch for changes in the source directory
class DirectoryWatchdogHandler(FileSystemEventHandler):
    """Watchdog handler that triggers sync on file or folder changes."""
    def __init__(self, source_folder, target_folder, backup_folder):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.backup_folder = backup_folder

    def on_any_event(self, event):
        """Trigger sync on any file or folder change event."""
        print(f"Change detected: {event.src_path}. Starting sync...")
        sync_report = sync_directories(self.source_folder, self.target_folder)
        generate_report(sync_report, report_base_path)
        sync_report_backup = sync_directories(self.target_folder, self.backup_folder)
        generate_report(sync_report_backup, backup_report_base_path)

# Main function to run the script
def main():
    # List and select folders from the Silverstack Test directory
    selected_folders = list_and_select_folders(default_source)
    if not selected_folders:
        print("No folders selected. Exiting...")
        sys.exit(0)

    # Sync selected folders to NAS
    for folder in selected_folders:
        source_folder = os.path.join(default_source, folder)
        target_folder = os.path.join(default_nas, "Projects", folder)
        sync_report = sync_directories(source_folder, target_folder)
        generate_report(sync_report, report_base_path)

    # Start watching the source directory for changes
    event_handler = DirectoryWatchdogHandler(default_source, default_nas, default_backup)
    observer = Observer()
    observer.schedule(event_handler, path=default_source, recursive=True)
    observer.start()
    print("Watching for changes in the source directory...")

    try:
        observer.join()  # Wait for any events, and keep script alive
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopped watching the directory. Exiting...")

    print("Sync and backup process completed successfully.")

# Run the main function
if __name__ == "__main__":
    main()
