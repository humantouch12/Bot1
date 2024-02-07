import websocket
import json
import time
import os
from datetime import datetime

from colorama import init, Fore
from idcreation import id_Creation

init()
def Ping_frame():
    print("------------------------------------------ping frame is about to be sent--------------------------------------------------")
    
    # url variables 
    url = "wss://testnet.binance.vision/ws-api/v3"  # Replace with the actual WebSocket endpoint

    # getting ID 
    
   # loop start 
    while True:
       
        try:
            id_value = id_Creation()
        # websocket connection 
            ws = websocket.create_connection(url)
        

   # request payload  
            ping_payload = {
            "id":id_value,
            "method": "ping"
            }

    
        # Send the ping payload
            ws.send(json.dumps(ping_payload))

        # Receive the response variables 
            response = ws.recv()
            response_data = json.loads(response)

            """
            current_folder = os.path.abspath("current")
            file_paths = [os.path.join(current_folder, "pingresponse.json")]

        # data set   
            data_sets = [response_data]                 
            for file_path, data_set in zip(file_paths, data_sets):
               
                try:
                      # Check if the file is not empty before loading
                        if os.path.getsize(file_path) > 0:
                            with open(file_path, 'r') as json_file:
                                existing_data = json.load(json_file)
                        else:
                            existing_data = []
                except FileNotFoundError:
                    existing_data = []

            # Add the new response data to the existing data
                existing_data.append(data_set)

            # Write the combined data back to the JSON file
                with open(file_path, 'w') as json_file:
                    json.dump(existing_data, json_file, indent=4)
"""
        # Check if the response is successful'
            if 'status' in response_data and response_data['status'] == 200:
                 
                 print(Fore.GREEN + "ping has been sent successfully")
                    # getting time stamp and converting it to HOURS
            else:
                 print(Fore.RED + f"an error has occured in sending ping {response_data}")

          
        
        except Exception as e:
         errorcode = 1
         with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
         
         print(Fore.RED + f"an exception error has occured in sending ping{e} ")
   
        # Print any exception that occurs
       
    # Wait for 10 seconds before the next iteration
        finally:
            ws.close()

        time.sleep(150)
        
if __name__ == "__main__":

    Ping_frame()