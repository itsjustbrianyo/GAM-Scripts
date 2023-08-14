"""
This script is used to deprovision Chromebooks and remove them from the
Google Workspace environment by moving the Chromebook to the Deprovisioning
OU, deprovisioning, and PowerWashing the Chromebook. Then finally removing
it from our tenant.

This script requires the following:

- Python 3.10+ - https://www.python.org/ 
- The latest version of GAMADV-XTD3 - https://github.com/taers232c/GAMADV-XTD3

Version 1.0 - 20230314 - BM

"""
import os
import subprocess
from time import sleep

BANNER = '''

┏━━━┓━━━┓━┓┏━┓┃┃┃━━━┓┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃
┃┏━┓┃┏━┓┃┃┗┛┃┃┃┃┃┓┏┓┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃
┃┃┃┗┛┃┃┃┃┏┓┏┓┃┃┃┃┃┃┃┃━━┓━━┓━┓━━┓┓┏┓┓━━┓┓━━┓━┓┃┓━┓┃━━┓
┃┃┏━┓┗━┛┃┃┃┃┃┃┃┃┃┃┃┃┃┏┓┃┏┓┃┏┛┏┓┃┗┛┃┫━━┫┫┏┓┃┏┓┓┫┏┓┓┏┓┃
┃┗┻━┃┏━┓┃┃┃┃┃┃┃┃┃┛┗┛┃┃━┫┗┛┃┃┃┗┛┃┓┏┛┃━━┃┃┗┛┃┃┃┃┃┃┃┃┗┛┃
┗━━━┛┛┃┗┛┛┗┛┗┛┃┃┃━━━┛━━┛┏━┛┛┃━━┛┗┛┃┛━━┛┛━━┛┛┗┛┛┛┗┛━┓┃
┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃━┛┃
┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┗┛┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃┃━━┛

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

# print(f"GAM has been detected in the following location {GAM_PATH}\n\n")

# Ask for csv file with serial numbers
file_name = input("What is the name of the csv file: ")

# Run GAM against the CSV file to move all devices to the Deprovisiong OU
move_ou = subprocess.run([GAM_PATH + " csv " + file_name +
                           " gam update cros query " +
                           "'id:~~serials~~' ou '/Deprovisioning'"],
                         stdout=subprocess.PIPE,
                         shell=True,
                         check=True)
sleep(3)
print(move_ou.stdout)

# Run GAM against the CSV file to PowerWash the devices
powerwash = subprocess.run([GAM_PATH + " csv " + file_name +
                            " gam cros_query 'id:~~serials~~'" +
                            " issuecommand command remote_powerwash doit"],
                        stdout=subprocess.PIPE,
                        shell=True,
                        check=True)
sleep(3)
print(powerwash.stdout)

# Run GAM against the CSV file to deprovision and powerwash the devices
deprovision = subprocess.run([GAM_PATH + " csv " + file_name +
                              " gam update cros query 'id:~~serials~~'" +
                              " action deprovision_retiring_device" +
                              " acknowledge_device_touch_requirement"],
                        stdout=subprocess.PIPE,
                        shell=True,
                        check=True)
sleep(3)
print(deprovision.stdout)

# Verify devcies are deprovisioned
verification = subprocess.run([GAM_PATH + " csv " + file_name +
                               " gam print cros query 'id:~~serials~~'" +
                               " status"],
                               stdout=subprocess.PIPE,
                            shell=True,
                            check=True)
sleep(3)
print(verification)
