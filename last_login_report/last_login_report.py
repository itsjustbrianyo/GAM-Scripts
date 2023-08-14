#!/usr/bin/python3
"""
This script is used export user last login details for
specific OUs. Once the data is exported it is written to 
last_login.csv and then automagically emailed.

If an error results while assigning licenses, that error will
be captured and emailed to support

This script requires the following setup on your system:

Python: 3.10+
GAM: Latest version

Version 1.0 - 20230428 - BM
Version 1.2 - 20230703 - BM
- Removed F string in COMMAND which was causing issues with GAMADV-XT3
- Reworked how the CSV file is created and now saves a local copy
Version 1.3 - 20230717 - BM
- Updated GAM command to search children OUs of OUs in the list
"""
import os
import csv
from datetime import datetime
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

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

# List of OUs to pull data from
OUs = ["/OU1",
       "/OU2",
       "/OU3"]

# Run the GAM command to get the last login information for users in the
# specified OUs and save it to a list
output_list = []
for ou in OUs:
    command = GAM_PATH + f" ou_and_children_ns {ou} print firstname lastname lastlogintime"
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    output_list.append(output.decode('utf-8'))

# Save the list of output information to a CSV file named last_login_date.csv
# Adjust OUTPUT_DIRECTORY if needed
date = datetime.now().strftime("%Y-%m-%d")
file_name = f"last_login_{date}.csv"
output_directory = "/opt/automations/last_login_report"

file_path = os.path.join(output_directory, file_name)
with open(file_path, 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    for output in output_list:
        for line in output.splitlines():
            writer.writerow(line.split(','))

# Email sender/receiver info
SENDER_EMAIL = "sender_email@example.com"
SENDER_PASSWORD = "supersecurepassword"
RECIPIENT_EMAIL = "recipient_email@example.com"

# Create the email
msg = MIMEMultipart()
msg['Subject'] = "Last Login Report"
msg['From'] = SENDER_PASSWORD
msg['To'] = RECIPIENT_EMAIL

# Attached the CSV file
with open(file_path, 'rb') as file:
    attachment = MIMEApplication(file.read(), _subtype='csv')
    attachment.add_header('Content-Disposition', 'attachment', filename=file_path)
    msg.attach(attachment)

# Send the email using Google
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
    smtp.send_message(msg)
