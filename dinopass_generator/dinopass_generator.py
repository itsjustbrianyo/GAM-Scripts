"""
This script is used to generate password for user accounts from DinoPass
using their API. It takes a CSV file with email accounts as input and
outputs a new CSV file with passwords which can used to create new user
accounts.

This script requires Python 3.10+ and GAM installed and setup on your system.
Instructions for setting up GAM can be found at :
    - https://github.com/taers232c/GAMADV-XTD3

Version 1.0 - 20230510 - BM
"""
import os
import csv
import requests

# DinoPass API endpoint.
API_ENDPOINT = 'https://www.dinopass.com/password/simple'
# For stronger passwords, comment out the above line and uncomment the below line
# API_ENDPOINT = 'https://www.dinopass.com/password/strong'

# Function to generate a password using DinoPass API
def generate_password():
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        return response.text.strip()
    else:
        raise Exception('Failed to generate password')

# Function to update the CSV file with passwords
def update_csv_with_passwords(INPUT_FILE, OUTPUT_FILE):
    # Open the input CSV file
    with open(INPUT_FILE, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

        # Add 'password' header to the first row
        rows[0].append('password')

        # Generate and add passwords for each row
        for row in rows[1:]:
            if row:
                password = generate_password()
                row.append(password)

    # Write the updated rows to the output CSV file
    with open(OUTPUT_FILE, 'w', newline='', encoding="UTF-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)

# Usage example
INPUT_FILE = input("What is the name of the csv file: ")
OUTPUT_FILE = "output.csv"

update_csv_with_passwords(INPUT_FILE, OUTPUT_FILE)
