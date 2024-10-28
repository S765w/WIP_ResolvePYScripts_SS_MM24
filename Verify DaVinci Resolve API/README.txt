Verify DaVinci Resolve API Script

This Python script is designed to verify the availability of DaVinci Resolve's scripting API in the current environment. 

The script attempts to get an instance of the DaVinci Resolve application using the scripting API. If successful, it prints a success message. If it fails, it prints an error message.

This script is used to trouble shoot and test that the latest version of python is interacting successfully with resolves API in order for any external scripts to work correctly. 


How to Use

1. Run the script in a Python environment where DaVinciResolveScript module is installed.
2. The script will attempt to get an instance of the DaVinci Resolve application.
3. If successful, it will print "Successfully got Resolve instance."
4. If it fails, it will print "Error: Could not get resolve instance." and the exception that occurred.

