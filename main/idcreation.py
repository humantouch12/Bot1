import uuid
import json
import time
import os 
from datetime import datetime
from colorama import init, Fore


init()
def id_Creation():
    try:

        new_uuid = uuid.uuid4()

            # Convert the UUID to a string
        uuid_str = str(new_uuid)

        print(Fore.GREEN + "new id has been created")
        return uuid_str
    except Exception as e:
        errorcode = 1
        with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
        print( Fore.RED + f"an exception error occurred in  id creation")

"""
    while True:
        current_folder = "current"
        os.makedirs(current_folder, exist_ok=True)
        with open("current/time.json", 'r') as json_file:
            milliseconds = json.load(json_file)

        seconds = milliseconds / 1000
        time_object = datetime.utcfromtimestamp(seconds)
        Time = time_object.strftime('%H:%M:%S')
        # Generate a UUID
        new_uuid = uuid.uuid4()

          # Convert the UUID to a string
        uuid_str = str(new_uuid)

        # Print the generated UUID
        file_path = os.path.join(current_folder, "id.json")
        with open (file_path,"w") as json_file:
            json.dump(uuid_str, json_file)
       # print("Generated UUID:", new_uuid)

       # format for sending to main display 
        try:
            with open('current/mainDisplay.json', 'r') as json_file:
              existing_data = json_file.read().splitlines()
        except FileNotFoundError:
              existing_data = []

# Add the new data string to the existing data
        existing_data.append( f"[{Time}] : New id has been created ")

# Save the updated data back to the JSON file with a newline after each entry
        with open('current/mainDisplay.json', 'w') as json_file:
            json_file.write('\n'.join(existing_data))
            json_file.write('\n')  # Add a newline after the last entry

        # Wait for 1 minute
        time.sleep(10)
        
"""
# Call the function to start generating UUIDs every minute
if __name__ == "__main__":
    id_Creation()

