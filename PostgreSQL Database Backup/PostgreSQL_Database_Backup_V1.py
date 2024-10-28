#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#---- User Configuration ----

# Number of minutes between backups
interval = 720

# Delete backups older than maxDays
maxDays = 30

# Resolve Studio version (adjust as per your installation)
resolveVersion = '19.3.1'

# Resolve installation path
resolvePath = f'/Applications/DaVinci Resolve {resolveVersion}.app'

# Resolve Postgres database name and default authentication
dbName = 'resolve'  # Adjust based on your Resolve PostgreSQL database name
dbUser = 'postgres'
dbPassword = 'DaVinci'

# Database server IP address unless this script is running on the same server
dbHost = '127.0.0.1'

# Installed Postgres version (adjust as per your PostgreSQL installation)
pgVersion = '13'  # Adjusted to the latest version

#---- End of User configuration ----

import os
import sys
import getpass
import time
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

sleeptime = interval * 60
version = '1.0.1'
currentUser = getpass.getuser()

# Determine the host operating system and set OS specific variables
hostOS = sys.platform

if hostOS == 'darwin':
    eol = '\n'
    dumpTool = f'/Library/PostgreSQL/{pgVersion}/bin/pg_dump'
    destPath = os.path.join('/Users', currentUser, 'Documents/ResolveProjectBackup')
    # Generate .pgpass authentication file if missing
    # Without this file pg_dump requires manual authentication
    pgPass = os.path.join('/Users', currentUser, '.pgpass')
    if not os.path.isfile(pgPass):
        with open(pgPass, 'w') as pgPassFile:
            pgPassFile.write(f"{dbHost}:5432:*:{dbUser}:{dbPassword}")

# We assume Linux host unless macOS.
else:
    print("This script is intended for macOS only.")
    sys.exit(1)

def wincompliance(ts):
    '''remove space and colons from timestamp for macOS compliance'''
    noSpace = 'T'.join(ts.split())
    noColon = '-'.join(noSpace.split(':'))
    return noColon

# Verify if destination path is valid. Create destination directory if missing.
if not os.path.isdir(destPath):
    os.makedirs(destPath)

# Create log file if missing
logName = 'ResolveBackupLog.txt'
logPath = os.path.join(destPath, logName)
if not os.path.isfile(logPath):
    with open(logPath, 'w') as logfile:
        logfile.write(f"Resolve Postgres Database Backup Tool V{version}.")
        logfile.write(eol)

# Infinite backup loop
while True:

    # Form pg_dump argument string and create backup
    timeStamp = str(datetime.now())[:-7]
    backupName = f'Resolve_{dbName}_PostgresDump_{wincompliance(timeStamp)}'
    savePath = os.path.join(destPath, backupName + '.sqlc')
    command = f'{dumpTool} -U {dbUser} -h {dbHost} -F c -f {savePath} {dbName}'
    process = Popen(command, universal_newlines=True, stdout=PIPE, stderr=STDOUT, shell=True)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)
    print(f"{backupName} saved")

    # Write a log entry
    with open(logPath, 'a') as logfile:
        logfile.write(f"Created {backupName}.sqlc")
        logfile.write(eol)

    # Remove old backups
    now = time.time()
    for filename in os.listdir(destPath):
        if filename.endswith('sqlc'):
            deleteFile = os.path.join(destPath, filename)
            timeStamp = os.stat(deleteFile).st_mtime
            if (now - timeStamp) / 86400 > maxDays:
                os.remove(deleteFile)

    print('sleeping...')
    time.sleep(sleeptime)
