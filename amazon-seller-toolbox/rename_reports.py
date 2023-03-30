import os                              # Library for performing OS related tasks
from datetime import datetime          # Module for working with dates and times
import shutil                          # Library for file operations
import re                              # Module for regular expressions
import sys                             # Module for working with the Python interpreter
from dotenv import load_dotenv
import re



# Check if debug mode is specified
# debug = False

# Function to check if we are in debug mode
def in_debug_mode():
    # if debug == True:
    #     return True
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        # debug = True
        return True
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is not None:
        # debug = True
        return True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if in_debug_mode():
    clear_screen()
    print("We are in debug mode.") 

load_dotenv() # load environment variables from .env file

directory = os.getenv("SOURCE_DIR")  # Source directory
destination = os.getenv("DESTINATION_DIR")   # Destination directory


matching_found = False                  # Initializes boolean variable to check if matching file is found
for filename in os.listdir(directory):  # Looping through all files in the source directory
    # Check for filename matching pattern
    if re.match(r'^\d{9,15}\.txt$', filename):
        if in_debug_mode():
            print(f"Checking file for match: {filename}")
        start_date, end_date = '', ''
        # Open the file and read the first line for desired string
        with open(os.path.join(directory, filename), 'r') as f:
            if 'settlement-id' in f.readline():
                if in_debug_mode():
                    print(f"Processing file: {filename}")
                matching_found = True   # Set flag for matching file found

                # get the start and end date of the settlement report
                start_date, end_date = f.readline().split('\t')[1:3]
                start_date = datetime.strptime(start_date, '%d.%m.%Y %H:%M:%S UTC').strftime('%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%d.%m.%Y %H:%M:%S UTC').strftime('%Y-%m-%d')

                # Create a list of folders based on date range
                start_year_month = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m')
                end_year_month = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m')
                if start_year_month != end_year_month:
                    months_folder = [start_year_month, end_year_month]
                else:
                    months_folder = [start_year_month]

                # Get the marketplace out of Field 11 in line 3
                marketplace_regex = re.compile(r'(?:^[^.]*\.)?([^.]*)(?:\s*|$)')
                match = marketplace_regex.search(f.readline().split('\t')[11])
                if match:
                    marketplace = match.group(1).upper()
                else:
                    marketplace = ""
    
                if in_debug_mode():
                    print("Marketplace: ", marketplace)
        
        # Rename the file with the new format and move it to the correct folder(s)
        if start_date != '' and end_date != '':
            new_filename = f'{start_date} - {end_date} - {marketplace} - {filename}'
            if in_debug_mode():
                print(f"New Filename: {new_filename}")
            try:
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            except PermissionError:
                print(f"Skipping {filename} because it is currently in use by another process.")

        if start_date != '' and end_date != '':
            source_file_path = os.path.join(directory, new_filename)

            # Check if folder 0 exist and create it if needed
            if in_debug_mode():
                print(f"Checking folder: {months_folder[0]}")
            if not os.path.exists(os.path.join(destination, months_folder[0])):
                os.makedirs(os.path.join(destination, months_folder[0]))

            try:
                shutil.copy(source_file_path, os.path.join(destination, months_folder[0], new_filename))
                # os.rename(os.path.join(directory, filename), os.path.join(directory, 'processed', filename))
            except PermissionError:
                print(f"Skipping {filename} because it is currently in use by another process.")

            if len(months_folder) == 2:
                if in_debug_mode():
                    print(f"Checking folder: {months_folder[1]}")
                # Check if folder 1 exist and create it if needed
                if not os.path.exists(os.path.join(destination, months_folder[1])):
                    os.makedirs(os.path.join(destination, months_folder[1]))
                try:
                    shutil.copy(source_file_path, os.path.join(destination, months_folder[1], new_filename))
                except PermissionError:
                    print(f"Skipping {filename} because it is currently in use by another process.")

if not matching_found:
    print("No matching file found.")     # If no matching file found, print out a message.