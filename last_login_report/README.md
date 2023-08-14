# Last Login Export

This script is used export user last login details for
specific OUs. Once the data is exported it is written to 
last_login.csv and then automagically emailed.

If an error results while assigning licenses, that error will
be captured and emailed to support

This script requires the following setup on your system:

## Crontab
The script is ran via crontab from the gam user account:

**crontab command**

crontab -e

**crontab entry**

#Last Login Report

0 5 * * 1 /opt/automations/last_login_report.py

## Requirements
Python: Version 3.10+
GAMADV-XTD3: Latest version - https://github.com/taers232c/GAMADV-XTD3
