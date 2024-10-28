import os
import subprocess
import shutil
from datetime import datetime

# Organize files into folders by date
def organize_files_by_date(file_path, proxy_folder):
    file_name = os.path.basename(file_path)
    date_folder = datetime.now().strftime('%Y-%m-%d')
    date_folder_path = os.path.join(proxy_folder, date_folder)

    # Ensure the date folder exists
    if not os.path.exists(date_folder_path):
        os.makedirs(date_folder_path)

    new_file_path = os.path.join(date_folder_path, file_name)
    return new_file_path

# Generate proxies from source files
def generate_proxies(source_media_path, proxy_storage_path, resolution, format_choice):
    skip_all_duplicates = False

    for file_name in os.listdir(source_media_path):
        if file_name.startswith('.'):
            continue  # Skip hidden files like .DS_Store

        file_path = os.path.join(source_media_path, file_name)
        output_file_name = f"{os.path.splitext(file_name)[0]}_proxy.{format_choice}"
        proxy_path = os.path.join(proxy_storage_path, output_file_name)

        # Organize the proxy in the date-based folder
        new_proxy_path = organize_files_by_date(proxy_path, proxy_storage_path)

        # Check if a file with the same name already exists
        if os.path.exists(new_proxy_path):
            if skip_all_duplicates:
                print(f"Skipping {file_name} (duplicate) due to previous 'skip all' decision.")
                continue  # Skip creating and moving the file

            choice = input(f"Duplicate found: {output_file_name} already exists. Overwrite? (y/n for skip all): ").lower()

            if choice == 'n':
                skip_all_duplicates = True
                print("Skipping all future duplicates.")
                continue  # Skip the current file and all future duplicates
            elif choice != 'y':
                print(f"Skipping {file_name}. No new file created.")
                continue  # Skip only this file

        # FFmpeg command to generate the proxy
        command = f"ffmpeg -i '{file_path}' -vf scale={resolution} -c:v libx264 -crf 23 -preset medium -c:a aac '{proxy_path}'"
        print(f"Generating proxy for {file_name}...")
        subprocess.run(command, shell=True)
        print(f"Proxy created at: {proxy_path}")

        # Move the generated proxy to the dated folder
        shutil.move(proxy_path, new_proxy_path)
        print(f"File {output_file_name} moved to {new_proxy_path}")

    print(f"All proxies generated and organized in: {proxy_storage_path}")

# Sync the proxy folder to the NAS
def sync_to_nas(nas_location, folder_to_sync):
    command = f"rsync -avh --progress '{folder_to_sync}/' '{nas_location}'"
    print(f"Syncing proxies to NAS location: {nas_location}...")
    result = subprocess.run(command, shell=True, capture_output=True)
    
    if result.returncode != 0:
        print(f"Rsync failed with error: {result.stderr.decode()}")
    else:
        print("Proxies successfully synced to NAS.")

# Main script execution
if __name__ == "__main__":
    # Default paths
    default_source_media_path = "/Users/samuel/Library/CloudStorage/Dropbox-UrbanVybezAB/Samuel S/Projects/IKEA IMC/Projects/Campaign 0001/Source Media"
    default_proxy_storage_path = "/Users/samuel/Library/CloudStorage/Dropbox-UrbanVybezAB/Samuel S/Projects/IKEA IMC/Projects/Campaign 0001/Proxy"
    default_nas_location = "/Users/samuel/Library/CloudStorage/Dropbox-UrbanVybezAB/Samuel S/Projects/IKEA IMC/Projects/Campaign 0001/TEST NAS"
    resolution = "960x540"
    format_choice = "mp4"

    # Confirm paths with the user
    print(f"Current paths:\nSource Media: {default_source_media_path}\nProxy Storage: {default_proxy_storage_path}\nNAS Location: {default_nas_location}")
    confirm = input("Are these paths correct? (y/n): ").lower()

    if confirm != 'y':
        source_media_path = input(f"Enter the path to your high-resolution media folder (Default: {default_source_media_path}): ")
        if not source_media_path:
            source_media_path = default_source_media_path

        proxy_storage_path = input(f"Enter the path to save the proxy files (Default: {default_proxy_storage_path}): ")
        if not proxy_storage_path:
            proxy_storage_path = default_proxy_storage_path

        nas_location = input(f"Enter the NAS location to sync the proxies (Default: {default_nas_location}): ")
        if not nas_location:
            nas_location = default_nas_location
    else:
        source_media_path = default_source_media_path
        proxy_storage_path = default_proxy_storage_path
        nas_location = default_nas_location

    # Generate proxies
    generate_proxies(source_media_path, proxy_storage_path, resolution, format_choice)

    # Sync generated proxies to the NAS
    print(f"Syncing generated proxies to the NAS: {nas_location}...")
    sync_to_nas(nas_location, proxy_storage_path)

    print("Proxy creation and synchronization completed successfully.")