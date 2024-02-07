import requests
import json 
import os
import time
from itertools import product
import difflib
from itertools import permutations
from difflib import SequenceMatcher
import websocket
import hmac
import hashlib
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime
from enum import Enum
from decimal import Decimal
from datetime import datetime

from realtime import Real_time



# quantity quoteOrderQty
def transfer():
   class OrderQuantity(Enum):
      enum_value1 = "BUY"
      enum_value2 = "SELL"
      enum_value3 = "MARKET"

   api_key = "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe"
   secret_key = "l2ryxyHlrZep2kcuitbC4L3ngUeIuLcmCH16ztZ57GOs0fdixMCkeGzb2BGrK7dq"
   amount = "1.1"
   symbol = "LINKUSDT"
   deci_amo = Decimal(str(amount))
   deci_amount = float(deci_amo)
   
    # url 
   url = "wss://testnet.binance.vision/ws-api/v3" 

   try:
      ws = websocket.create_connection(url)
      Time = Real_time()
    # sorting to variables 
      

      params = {
                'apiKey':f'{api_key}',
                'timestamp': f'{Time}',
                'recvWindow': '2000',
                'symbol':f'{symbol}',
                'side':'SELL',
                'type':'MARKET',
                'quoteOrderQty':f'{deci_amount}'
            }
      
      payload = '&'.join([f'{param}={params[param]}' for param in sorted(params)])

      secret_key_bytes = secret_key.encode('ascii')
      signature = hmac.new(secret_key_bytes, msg=payload.encode('ascii'), digestmod=hashlib.sha256).hexdigest()
      
      id_value= "OIIR34445"
      
      Details_payload = {
                        "id": id_value,
                        "method": "order.place",
                        "params": {
                                    "apiKey": api_key,
                                    "timestamp": Time,
                                    "recvWindow":2000,
                                    "symbol": symbol ,
                                    "side":"SELL",
                                    "type":"MARKET",
                                    "quoteOrderQty": deci_amount,
                                    "signature": signature
                                    
                                    }
                                    }

      ws.send(json.dumps( Details_payload ))
      response = ws.recv()
      account_data = json.loads(response)
# STORING inside response file 
      current_folder = os.path.abspath("current")
      file_paths = [os.path.join(current_folder, "response.json")]

      data_sets = [account_data]                 
      for file_path, data_set in zip(file_paths, data_sets):
          try:
             
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
      if 'status' in account_data and account_data ['status'] == 200:
         print("successful")
      else:
         print(f" unnsuccessful {account_data}")
   except Exception as e:
      print(e)



transfer()