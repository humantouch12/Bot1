# import of all necessary  libuaries 
import websocket
import json 

from colorama import init, Fore
from idcreation import id_Creation


init()
# Function start 
def Real_time():
   
    url = "wss://testnet.binance.vision/ws-api/v3"  # Replace with the actual WebSocket endpoint
    
   # loop 
    
        # option 
    try:
        
        ws = websocket.create_connection(url)
        id_value = id_Creation()

    # request sections 
            # time request payload 
        time_payload = {
                        "id":  id_value,
                        "method": "time"
                                  }

    
        # Sending  the time payload
        ws.send(json.dumps(time_payload))

        # making response as  variables 
        response = ws.recv()
        response_data = json.loads(response)
        Time = response_data["result"]["serverTime"]
        
        # Check if the response is successfulor not 
        if 'status' in response_data and response_data['status'] == 200:
          print( Fore.GREEN + "time has been checked successfully") 
          return Time
        else:
           print(Fore.RED +  f"error in getting time{response_data}")
    except Exception as e:
       errorcode = 1
       with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
       print( Fore.RED + f"time exception error{e}")
            
            
if __name__ == "__main__":
       
                 
    Real_time()


