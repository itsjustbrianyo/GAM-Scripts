#!/usr/bin/python3
"""
This script is used to delete all emails from the list of
email accounts in Google. 

This script requires the following setup on your system:

Python: 3.10+
GAM: Latest version of GAMADV-XTD3

Version 1.0 - 20230704 - BM

"""
import os
import csv
from time import sleep
from datetime import datetime
import subprocess

BANNER="""
╭━━━╮╱╱╭╮╱╱╱╭╮╱╱╱╱╱╱╭━━━╮╱╱╱╱╱╱╭╮
╰╮╭╮┃╱╱┃┃╱╱╭╯╰╮╱╱╱╱╱┃╭━━╯╱╱╱╱╱╱┃┃
╱┃┃┃┣━━┫┃╭━┻╮╭╋━━╮╱╱┃╰━━┳╮╭┳━━┳┫┃╭━━╮
╱┃┃┃┃┃━┫┃┃┃━┫┃┃┃━┫╱╱┃╭━━┫╰╯┃╭╮┣┫┃┃━━┫
╭╯╰╯┃┃━┫╰┫┃━┫╰┫┃━┫╭╮┃╰━━┫┃┃┃╭╮┃┃╰╋━━┃
╰━━━┻━━┻━┻━━┻━┻━━╯╰╯╰━━━┻┻┻┻╯╰┻┻━┻━━╯


"""
print(BANNER)
sleep(2)

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

# List of email addresses.
ACCOUNTS = ["email1@example.com",
            "email2@exemple.com",
            "email3@example.com"]

# Run the GAM command to delete emails older than 1 month
output_list = []
for account in ACCOUNTS:
    try:
        command = GAM_PATH + ' user ' + account + ' delete messages query \"older_than:1m\" maxtodelete 999999 doit'
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        output_list.append(output.decode('utf-8'))
        print(f"Finished deleting emails for {account}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting emails for account {account}: {e.output.decode('utf-8')}")

# Save the list of output information to a CSV file
# Adjust OUTPUT_DIRECTORY if needed
date = datetime.now().strftime("%Y-%m-%d")
file_name = f"deleted_emails_{date}.csv"
OUTPUT_DIRECTORY = "/opt/automations/deletedEmails"

file_path = os.path.join(OUTPUT_DIRECTORY, file_name)
with open(file_path, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    for output in output_list:
        for line in output.splitlines():
            writer.writerow(line.split(','))
