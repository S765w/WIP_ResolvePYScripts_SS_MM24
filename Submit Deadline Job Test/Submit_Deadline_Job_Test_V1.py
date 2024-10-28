import os
import subprocess

# Function to write the job info file with dynamic username
def create_job_info_file(file_path):
    # Get the logged-in username dynamically using environment variable
    user_name = os.getenv("USER")  # This is more reliable in environments like VSC
    
    # Create job_info_content with the dynamically set username
    job_info_content = f"""\
Name=Test CommandLine Job
UserName={user_name}
Pool=none
Priority=50
Plugin=CommandLine
"""
    with open(file_path, 'w') as file:
        file.write(job_info_content)

# Function to write the plugin info file
def create_plugin_info_file(file_path):
    plugin_info_content = """\
Executable=/bin/bash
Arguments=-c "echo Hello, Deadline!"
"""
    with open(file_path, 'w') as file:
        file.write(plugin_info_content)

# Function to submit the job to Deadline
def submit_job(job_info_path, plugin_info_path):
    # Specify the full path to the Deadline command
    deadline_command_path = "/Applications/Thinkbox/Deadline10/DeadlineCommand10.app/Contents/MacOS/DeadlineCommand10"

    # Check if deadlinecommand exists
    if not os.path.exists(deadline_command_path):
        print(f"Error: Deadline command not found at {deadline_command_path}. Ensure Deadline is installed correctly.")
        return

    try:
        result = subprocess.run(
            [deadline_command_path, "submitjob", job_info_path, plugin_info_path],
            capture_output=True, text=True
        )
        print(result.stdout)
        if result.returncode == 0:
            print("Job submitted successfully.")
        else:
            print("Error submitting job.")
            print(result.stderr)
    except FileNotFoundError as e:
        print(f"Error: Deadline command not found. Ensure Deadline is installed correctly.")
        print(e)

def get_directory_from_user(default_directory):
    """Ask the user to enter a directory path, defaulting to Desktop"""
    user_input = input(f"Enter a directory to save the job files (or press Enter to use default: {default_directory}): ")
    if user_input:
        # Expand user directory if a custom directory is provided
        expanded_path = os.path.expanduser(user_input)
        return expanded_path
    else:
        # Return the default directory if no input is provided
        return default_directory

def main():
    # Get the user's desktop path as the default directory
    default_directory = os.path.join(os.path.expanduser("~"), "Desktop/test")

    # Ask the user for a directory, or use the default
    directory = get_directory_from_user(default_directory)

    # Ensure the directory exists
    try:
        os.makedirs(directory, exist_ok=True)
    except PermissionError as e:
        print(f"PermissionError: Unable to create directory '{directory}'. {e}")
        return

    # Paths to job info and plugin info files
    job_info_path = os.path.join(directory, "job_info.job")
    plugin_info_path = os.path.join(directory, "plugin_info.job")

    # Create the job info and plugin info files
    try:
        create_job_info_file(job_info_path)
        create_plugin_info_file(plugin_info_path)
    except PermissionError as e:
        print(f"PermissionError: Unable to write to '{directory}'. {e}")
        return

    # Submit the job to Deadline
    submit_job(job_info_path, plugin_info_path)

if __name__ == "__main__":
    main()
