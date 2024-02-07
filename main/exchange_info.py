import json
import os
import websocket
import hmac
import hashlib
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime
import requests

from colorama import init, Fore
from idcreation import id_Creation


init()
def exchange_info():

  url = "wss://testnet.binance.vision/ws-api/v3"
  # getting time in milliseconds and hms
  """
  with open("current/time.json", 'r') as json_file:
    Time = json.load(json_file)
    # sorting to variables 
  seconds = Time / 1000
  time_object = datetime.utcfromtimestamp(seconds)
  period = time_object.strftime('%H:%M:%S')

  #getting id 
  with open("current/id.json", 'r') as json_file:
    id_value= json.load(json_file)
"""
  try: 
        ws = websocket.create_connection(url)
        id_value = id_Creation()

        exchangeInfo_payload = {
                        "id": id_value,
                        "method": "exchangeInfo",
                        "params": {
                                    "permissions": "SPOT" 
                                    }
                                    }
        # Send the ping payload
        ws.send(json.dumps(exchangeInfo_payload))
        # Receive the response variables 
        response = ws.recv()
        response_data = json.loads(response)
        """
          # saving in a json file 
        current_folder = os.path.abspath("current")
        file_paths = [os.path.join(current_folder, "exchangeInforesponse.json")]

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
        if 'status' in response_data and response_data['status'] == 200:
            exchangeInfo_data = response_data

            with open("current/exchangeinfo.json", 'w') as json_file:
                json.dump(exchangeInfo_data, json_file, indent=4)
            print( Fore.GREEN + "Exchange infomation has been gotten successfully")
            return exchangeInfo_data
        else:
            errorcode = 1
            with open("counters/error.json", 'w') as json_file:
              json.dump(errorcode, json_file)
            print( Fore.RED + f" an error occured in getting exchange infomation {response_data}")
            
          


  except Exception as e:
      errorcode = 1
      with open("counters/error.json", 'w') as json_file:
          json.dump(errorcode, json_file)
      print( Fore.RED +  f" an exception Error has occured in getting exchnage information{e}")
      
  finally:
         ws.close()


      
if __name__ == "__main__":
  exchange_info()