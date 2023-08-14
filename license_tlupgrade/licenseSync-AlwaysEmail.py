#!/usr/bin/python3
"""
This script is used to assign any users in the
license_TeachersLearningUpgrade group the Teachers
and Learning Upgrade license. Any users added to the group
will get the license, any users removed from the group
will have the license removed from their account.

If an error results while assigning licenses, that error will
be captured and emailed to (recipient_email)

This script requires the following setup on your system:

Python: 3.10+
GAMADV-XTD3: Latest version

Version 1.0 - 20230428 - BM
"""
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

BANNER = '''
╭━━━┳━━━┳━╮╭━╮╭╮
┃╭━╮┃╭━╮┃┃╰╯┃┃┃┃
┃┃╱╰┫┃╱┃┃╭╮╭╮┃┃┃╱╱╭┳━━┳━━┳━╮╭━━┳┳━╮╭━━╮
┃┃╭━┫╰━╯┃┃┃┃┃┃┃┃╱╭╋┫╭━┫┃━┫╭╮┫━━╋┫╭╮┫╭╮┃
┃╰┻━┃╭━╮┃┃┃┃┃┃┃╰━╯┃┃╰━┫┃━┫┃┃┣━━┃┃┃┃┃╰╯┃
╰━━━┻╯╱╰┻╯╰╯╰╯╰━━━┻┻━━┻━━┻╯╰┻━━┻┻╯╰┻━╮┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯

This script is used to assign any users in the
license_TeachersLearningUpgrade group the Teachers
and Learning Upgrade license. Any users added to the group
will get the license, any users removed from the group
will have the license removed from their account.

Script Version 1.0 - 20230428 - BM
'''
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

# GAM Licensing command to run
COMMAND = f"{GAM_PATH} group license_TeachersLearningUpgrade sync license 1010370001"

# Run the command and capture any errors
result = subprocess.check_output(COMMAND, stderr=subprocess.STDOUT, shell=True)

# Send an email if there was an error
# Email details
SENDER_EMAIL = "sender_email"
SENDER_PASSWORD = "super_strong_password"
RECIPIENT_EMAIL = "recipient_email"

# Create message object
msg = MIMEMultipart()
msg['Subject'] = "Google License Automation Error"
msg['From'] = SENDER_PASSWORD
msg['To'] = RECIPIENT_EMAIL

# Add error message to email body
body = MIMEText(result.decode('utf-8'))
msg.attach(body)

# Attach command output as a file
output_file = MIMEApplication(result)
output_file.add_header('Content-Disposition', 'attachment', filename='gam_output.txt')
msg.attach(output_file)

# Connect to SMTP server and send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)
server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
server.quit()

# Display output from running th ecomand
print(result.decode('utf-8'))
