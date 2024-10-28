Submit to Deadline Job Test Script

This script automates the submission of jobs to Thinkbox's Deadline render manager. It dynamically creates job files based on the logged-in user's specifications and sends them to Deadline for rendering.

How to Use

1. Make sure Deadline is installed and running

Make sure that Thinkbox Deadline is installed and configured correctly on your system. The script uses the "DeadlineCommand10" tool, the path of which should be set correctly in the script.

2. Open in Visual Studio Code (VSC)

- Open Visual Studio Code and load the script file (`submit_deadline_job_test.py`).
- Make sure that your Python environment is active and the required dependencies are installed.

3. Edit standard paths (optional)

The script saves job info and plugin info files in a default directory on your desktop (`~/Desktop/test`). You can either:

- Use the default path by pressing Enter when prompted.
- Enter your own path when prompted to do so.

4. Running the Script

- Run the script via the terminal in Visual Studio Code:

 python submit_deadline_job_test.py

- The script creates the required job files and sends them to Deadline with the command:
 - Job info file: Contains metadata for the job (e.g. job name, user name, plugin).
 - Plugin info file: Specifies the executable file and the arguments for rendering.

5. Submitting Jobs to Deadline

After the script has generated the job files, it automatically submits them to Deadline. If the submission was successful, a message like this is displayed:

The job was submitted successfully.

6. Reviewing Job Status

Once the job is submitted, you can monitor its progress using the Deadline Monitor tool. If there are any issues, check the logs for troubleshooting.

Requirements

1. Deadline 10 is installed:
 - Ensure that Thinkbox Deadline 10 is installed and configured correctly.
 - Ensure the executable file "DeadlineCommand10" is available and the path in the script is set correctly:
 ```python
 "/Applications/Thinkbox/Deadline10/DeadlineCommand10.app/Contents/MacOS/DeadlineCommand10"

2. Python 3.x:
 - Make sure that Python 3.x is installed on your system.
 - Make sure that your Python environment (e.g. virtualenv) is activated before you run the script.

3. Required Python modules:
 - `os`: For handling file paths and environment variables.
 - `subprocess`: For executing the deadline command line tool within the script.

 These modules are included in Python by default, so no additional installation is required.

4. MacOS/Linux shell (for .sh execution):
 - For executing commands via the shell on MacOS or Linux.

5. Authorisation settings:
 - Ensure that the script and its directories have the appropriate permissions to create and write files.
 - Use `chmod` to grant execution rights to the shell script if required:

 chmod +x /path/to/remote-render-trigger.sh