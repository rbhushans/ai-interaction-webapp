import os
import time

def cleaner():
    directory = "models_users/"
    # First check if the directory exists. If not, create it
    if not (os.path.isdir(directory)):
        os.mkdir(directory)

    while True: # Run indefinitely to keep storage usage minimal
        files = os.listdir(directory)
        curr_time = time.time()
        for a_file in files:
            file_access_time = os.path.getatime(directory + a_file) # Seconds since epoch
            if (curr_time - file_access_time) > 3600:
                # File has existed without access for more than 1 hour. Delete it
                os.remove(directory + a_file)

        time.sleep(3600) # Wait 1 hour before starting cleanup again
