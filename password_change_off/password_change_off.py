#!/usr/bin/python3
"""docstring"""
import os
import csv
from datetime import datetime
import subprocess

BANNER="""
╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭┳━━━╮╱╱╱╱╱╱╱╱╭╮
┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃╭━╮┃╱╱╱╱╱╱╱╭╯╰╮
┃╰━╯┣━━┳━━┳━━┳╮╭╮╭┳━━┳━┳━╯┃╰━╯┣━━┳━━┳━┻╮╭╯
┃╭━━┫╭╮┃━━┫━━┫╰╯╰╯┃╭╮┃╭┫╭╮┃╭╮╭┫┃━┫━━┫┃━┫┃
┃┃╱╱┃╭╮┣━━┣━━┣╮╭╮╭┫╰╯┃┃┃╰╯┃┃┃╰┫┃━╋━━┃┃━┫╰╮
╰╯╱╱╰╯╰┻━━┻━━╯╰╯╰╯╰━━┻╯╰━━┻╯╰━┻━━┻━━┻━━┻━╯

--------------------------------------------------------------
This script is used to reset users password to not ask for a 
password change on the next login.

The script will run on the following root and any children OUs:

- /OU1
- /OU2
- /OU3

This script requires the following setup on your system:

Python: 3.10+
GAM: Latest version of GAMADV-XTD3

Version 1.0 - 20230629 - BM
Version 1.1 - 20230717 - BM
- Changed command to include any children OUs
--------------------------------------------------------------

"""
print(BANNER)

# Detects if Windows or Linux and if GAM is installed in the default location
if os.name == 'nt':
    WIN_CHECK = "C:\\GAM\\gam.exe"
    if os.path.exists(WIN_CHECK) is True:
        GAM_PATH = WIN_CHECK
    else:
        print("Unable to find GAM installation. Is it installed in C:\\GAM")
        exit()
elif os.name == "posix":
    NIX_CHECK = os.path.expanduser("~") + "/bin/gam/gam"
    NIX_CHECK_GAMADV = os.path.expanduser("~") + "/bin/gamadv-xtd3/gam"
    if os.path.exists(NIX_CHECK) is True:
        GAM_PATH = NIX_CHECK
    elif os.path.exists(NIX_CHECK_GAMADV) is True:
        GAM_PATH = NIX_CHECK_GAMADV
    else:
        print("Unable to find GAM installation. Is it installed in C:\\GAM")
        exit()
else:
    print("unable to detect OS. Exiting")
    exit()

# List of OUs to pull students from
OUs = ["/OU1",
       "/OU2",
       "/OU3"]

# Run the GAM command to reset the password and save that info to list to output to the console
output_list = []
for ou in OUs:
    command = GAM_PATH + f" ou_and_children {ou} update user changepassword off"
    output = subprocess.check_output(command,
            stderr=subprocess.STDOUT, shell=True)
    output_list.append(output.decode('utf-8'))
    print(f"Change completed on {ou}")

# Save the list of output information to a CSV file
date = datetime.now().strftime("%Y-%m-%d")
file_name = f"daily_password_changeoff.{date}.csv"
OUTPUT_DIRECTORY = "/opt/automations/daily_password_changeoff"

file_path = os.path.join(OUTPUT_DIRECTORY, file_name)
with open(file_path, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    for output in output_list:
        for line in output.splitlines():
            writer.writerow(line.split(','))
