import os
import time
import asyncio

def cleaner():
    directory = "models_users/"
    while True: # Run indefinitely to keep storage usage minimal
        files = os.listdir(directory)
        curr_time = time.time()
        for a_file in files:
            file_access_time = os.path.getatime(directory + a_file) # Seconds since epoch
            if (curr_time - file_access_time) > 3600:
                # File has existed without access for more than 1 hour. Delete it
                os.remove(directory + a_file)

        time.sleep(3600) # Wait 1 hour before starting cleanup again
