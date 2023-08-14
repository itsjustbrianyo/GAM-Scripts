# Moving Chromebooks

This script is used to move Chromebooks in our Google Workspace environment from one OU to another.

A CSV file with the header of "serials" will need to be created and saved in the directory this script is ran from. You'll be asked for the OU name when ran. The OU name should be something similar to /OU1/SubOU which you can find from logging into the Google Admin panel.

## Requirements
- Python 3.10+ - https://www.python.org/
- GAMADV-XTD3 - Latest version available at https://github.com/taers232c/GAMADV-XTD3
