# Deprovisiong Chromebooks

This script is used to deprovision Chromebooks and remove them from the
Google Workspace environment by moving the Chromebook to the Deprovisioning
OU, deprovisioning, and PowerWashing the Chromebook. Then finally removing
it from our tenant.

This script requires the following:

- A CSV file with the header of "serials" will need to be created and saved in the directory this script is ran from. 
- a OU named Deprovisioning in the root of your Google Domain (or adjust the path in the script)

## System Requirements
- Python 3.10+ - https://www.python.org/
- The latest version of GAM - https://github.com/GAM-team/GAM/wiki
