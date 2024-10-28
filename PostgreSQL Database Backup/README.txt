PostgreSQL Database Backup Script

This Python script is designed to regularly backup a DaVinci Resolve PostgreSQL database and delete backups older than a specified number of days.

User Configuration: At the top of the script, you can configure several variables such as the interval between backups, the maximum age of backups, the Resolve Studio version, the Resolve installation path, the database name, user, password, and host, and the installed Postgres version.

Operating System Detection: The script detects the host operating system and sets OS specific variables accordingly. Currently, the script is intended for macOS only.

Backup Creation: The script uses the `pg_dump` tool to create a backup of the specified database. The backup is saved in a .sqlc file in the specified destination path.

Backup Deletion: The script automatically deletes backups that are older than the specified maximum age.

Logging: The script creates a log file in the destination path and writes a log entry each time a backup is created.

How to Use

1. Configure the user configuration variables at the top of the script as per your setup.
2. Run the script in a Python environment using Visual Studio Code
3. The script will create a backup of the specified database at the specified interval and delete backups older than the specified maximum age.
4. You can check the log file in the destination path to see when backups were created.