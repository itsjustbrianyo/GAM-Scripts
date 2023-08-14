# Teacher & Learning License Upgrade

This python script is used to automatically assign the **Teacher and Learning Upgrade** license in Google Workspace via group management. The script lives on (Ubuntu 22.04) and has an hourly cron job to run the script. If an error occurs, an email will be sent to the
(recipient_email) team.

## Assigning Licenses
To assign licenses using the script, add or remove users using the **license_TeachersLearningUpgrade** group in the Google Admin Console. The script will then run every hour on the hour and will assign or remove the license from users based on changes to the group membership.

## Crontab
The script is ran via crontab from the gam user account:

**crontab command** \
crontab -e

**crontab entry** \
\# Teacher & Learning License Automation \
0 7-18 * * 1-5 /opt/automations/licenseSync.py

## Requirements
- Python: Version 3.10+
- GAMADV-XTD3: Latest version - https://github.com/taers232c/GAMADV-XTD3
