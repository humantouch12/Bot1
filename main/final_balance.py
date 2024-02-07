import json
import os
import websocket
import hmac
import hashlib
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime
import requests


from colorama import init, Fore
from realtime import Real_time
from idcreation import id_Creation



init()
def Final_Account_Details():
    # keys 
    api_key = "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe"
    secret_key = "l2ryxyHlrZep2kcuitbC4L3ngUeIuLcmCH16ztZ57GOs0fdixMCkeGzb2BGrK7dq"
    # url 
    url = "wss://testnet.binance.vision/ws-api/v3"  # Replace with the actual WebSocket endpoint

    #time 
    

    try: 
        
        ws = websocket.create_connection(url)
        Time = Real_time()

        

    # parameters 

        params = {
                'apiKey':f'{api_key}',
                'recvWindow': '1000',
                'timestamp': f'{Time}'
                
            }
    # payloads for signature creating 
        payload = '&'.join([f'{param}={params[param]}' for param in sorted(params)])

# Interpret secretKey as ASCII data and use it as a key for HMAC-SHA-256
        secret_key_bytes = secret_key.encode('ascii')
        signature = hmac.new(secret_key_bytes, msg=payload.encode('ascii'), digestmod=hashlib.sha256).hexdigest()
        # id 
        
        id_value = id_Creation()
    #account payload
        Details_payload = {
                        "id": id_value,
                        "method": "account.status",
                        "params": {
                                    "apiKey": "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe",
                                    "signature": signature,
                                    "timestamp": Time,
                                    "recvWindow":1000,
                                    }
                                    }
    #websocket
    

        ws.send(json.dumps( Details_payload ))
        response = ws.recv()
        account_data = json.loads(response)

        if 'status' in account_data  and account_data ['status'] == 200:
          with open("data/allcrypto.json", 'r') as json_file:
            assets_to_extract= json.load(json_file)
        
          extracted_balances = {}

# Loop through the provided balance data
          for asset_data in account_data.get("result", {}).get("balances", []):
              asset_symbol = asset_data.get("asset")
              if asset_symbol in assets_to_extract:
                  extracted_balances[asset_symbol] = {
            "free": float(asset_data.get("free", 0)),
            "locked": float(asset_data.get("locked", 0))
                                                            }
          
          
          print(Fore.GREEN +  " final balance account has been checked ")
          return extracted_balances
            

        else:
            errorcode = 1
            with open("counters/error.json", 'w') as json_file:
                json.dump(errorcode, json_file)
            print( Fore.RED + "error getting real time balance ")
            
              
            
    except Exception as e:
        errorcode = 1
        with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
        print( Fore.RED + f"exception error occured in real time balnce{e}")
        

    
   


if __name__ == "__main__":
# Example usage
    Final_Account_Details()


# Print or use the result
