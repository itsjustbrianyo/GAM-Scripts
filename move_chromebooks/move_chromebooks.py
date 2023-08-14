#!/bin/python3
"""
This script is used to move Chromebooks from one OU to another. You'll need
a CSV file with the serial numbers of the Chromebooks and will be asked which
OU to move them to (i.e. /OU1/SubOU)

This script requires Python 3.10+ and GAM installed and setup on your system.
Instructions for setting up GAM can be found at :
    - https://github.com/taers232c/GAMADV-XTD3

Version 1.0 - 20230510 - BM

"""
import os
import subprocess

BANNER = '''

╭━╮╭━╮╱╱╱╱╱╱╱╱╱╱╱╱╱╭━━━┳╮╱╱╱╱╱╱╱╱╱╱╱╱╭╮╱╱╱╱╱╱╱╭╮
┃┃╰╯┃┃╱╱╱╱╱╱╱╱╱╱╱╱╱┃╭━╮┃┃╱╱╱╱╱╱╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱┃┃
┃╭╮╭╮┣━━┳╮╭┳┳━╮╭━━╮┃┃╱╰┫╰━┳━┳━━┳╮╭┳━━┫╰━┳━━┳━━┫┃╭┳━━╮
┃┃┃┃┃┃╭╮┃╰╯┣┫╭╮┫╭╮┃┃┃╱╭┫╭╮┃╭┫╭╮┃╰╯┃┃━┫╭╮┃╭╮┃╭╮┃╰╯┫━━┫
┃┃┃┃┃┃╰╯┣╮╭┫┃┃┃┃╰╯┃┃╰━╯┃┃┃┃┃┃╰╯┃┃┃┃┃━┫╰╯┃╰╯┃╰╯┃╭╮╋━━┃
╰╯╰╯╰┻━━╯╰╯╰┻╯╰┻━╮┃╰━━━┻╯╰┻╯╰━━┻┻┻┻━━┻━━┻━━┻━━┻╯╰┻━━╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯

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

# Ask for csv file with serial numbers
file_name = input("What is the name of the csv file: ")

# Check if the CSV file exists
if not os.path.isfile(file_name):
    print("CSV file not found. Please make sure the file exists.")
    exit(1)

# Ask for the OU
ou_name = input("Which OU will the Chromebooks be moved to: ")

# Run GAM against the CSV file to move all devices to the Deprovisiong OU
try:
    move_ou = subprocess.run([GAM_PATH + " csv " + file_name +
                            " gam update cros query " +
                            "'id:~~serials~~' ou " + ou_name],
                            stdout=subprocess.PIPE,
                            shell=True,
                            check=True)
    print(move_ou.stdout)
except subprocess.CalledProcessError as e:
    print("An error occurred while running the GAM command:")
    print(e)
    exit(1)