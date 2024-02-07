import json
import os
import websocket
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime

from colorama import init, Fore




from idcreation import id_Creation

init()
def Current_price_forAll():
    #getting id value 
    print("-------------------Current price is about to be checked ------------------------")
    # base url 
    url = "wss://testnet.binance.vision/ws-api/v3"  # Replace with the actual WebSocket endpoint
# time 
    
    try:
         
        ws = websocket.create_connection(url)
        id_value = id_Creation()
        

   # request sections 
        price_payload = {
        "id":id_value,
        "method": "ticker.price",
         #"params": {
                   # "symbol":'ETHBTC'
                   # }
            }

    
        # Send the ping payload
        ws.send(json.dumps(price_payload))

        # Receive the response variables 
        response = ws.recv()
        response_data = json.loads(response)

           # purpose = (" Time: ", response_data)

        # Check if the response is successful'
        if 'status' in response_data and response_data['status'] == 200:
            Current_ExchangePrices = response_data
            
            with open("counters/price.json", 'r') as json_file:
                counts = json.load(json_file)
            if counts == 0:
                with open("current/prices.json" ,'w') as json_file:
                    json.dump(Current_ExchangePrices, json_file, indent=4)

                    counts += 1
                with open("counters/price.json" ,'w') as json_file:
                    json.dump(counts, json_file, indent=4)
            else:
                pass

            
            
            print( Fore.GREEN +"current prices  has been checked successfully ")
            #print(Current_ExchangePrices)
            return Current_ExchangePrices 
            

        else:
             print(Fore.RED + f"an error occured in checking for current prices {response_data}")
             return False
            # code to awaite pong message 
          
            # code to awaite pong message 
    except Exception as e:
        errorcode = 1
        with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
         
        print(Fore.RED + f"an exception error occured in checking for current prices {e}")
         
   
    # Wait for 10 seconds before the next iteration
 

if __name__ == "__main__":

# Example usage
    Current_price_forAll()
