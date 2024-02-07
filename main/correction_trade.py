
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
import math

from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime
from enum import Enum
from decimal import Decimal
from datetime import datetime
from colorama import init, Fore


from realtime import Real_time
from idcreation import id_Creation
from allBal import all_Account_Details
from exchange_info import exchange_info



init()
def Coreection_trade():
  print("-----------------------------------------corecction Trade Has started--------------------------------------------------------------------")
  try:
    api_key = "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe"
    secret_key = "l2ryxyHlrZep2kcuitbC4L3ngUeIuLcmCH16ztZ57GOs0fdixMCkeGzb2BGrK7dq"
    url = "wss://testnet.binance.vision/ws-api/v3"
    # trade details 
    with open("data/correction.json", 'r') as json_file:
      details = json.load(json_file)
    # main crypto 
      Main_crypto = details[0]
    
    
      
    #Coreection trade pair 
    trade_pair = details[1]

    class OrderQuantity(Enum):
      enum_value1 = "BUY"
      enum_value2 = "SELL"
      enum_value3 = "MARKET"

  # exchange imformation 
    
    exchangeInfo_data = exchange_info()
    

    tradeExchangeDetails = next((symbol_data for symbol_data in exchangeInfo_data["result"]["symbols"] if symbol_data["symbol"] == trade_pair), None)
    market_lot_size_data = next((filter_data for filter_data in tradeExchangeDetails["filters"] if filter_data["filterType"] == "MARKET_LOT_SIZE"), None)
    min_qty = float(market_lot_size_data["minQty"])
    max_qty = float(market_lot_size_data["maxQty"])
    step_size = float(market_lot_size_data["stepSize"])
    # account details 
    account_data = all_Account_Details()
    Main_account = float(next(item["free"] for item in account_data["result"]["balances"] if item.get("asset") == Main_crypto  and "free" in item))
    

    if trade_pair.startswith(Main_crypto):
      trade_quantity = Main_account
      side ="SELL"
    
    else:
      trade_quantity = Main_account * 1/(details[2])
      side ="BUY"

    
    # LOT SIZE CHECK
    if step_size == 0:
      steps_amount = trade_quantity
    else:
      acessable = trade_quantity // step_size
      steps_amount   = acessable * step_size
    
    if int(steps_amount ) == 0:
      order_of_magnitude = int(math.floor(math.log10(abs(steps_amount))))
      multiplier = 10 ** (1 - 1 - order_of_magnitude)
      quantity  = math.floor(steps_amount * multiplier) / multiplier
    
    else:
      quantity = math.floor(steps_amount * 10) / 10 
    
    
    try:
      ws = websocket.create_connection(url)
      id_value = id_Creation()
      Time = Real_time()
      

      params = {
                  'apiKey':f'{api_key}',
                  'quantity':f'{quantity}',
                  'recvWindow': '2000',
                  'side':f'{side}',
                  'symbol':f'{trade_pair}',
                  'timestamp': f'{Time}',
                  'type':'MARKET'
                  
                              }

      payload = '&'.join([f'{param}={params[param]}' for param in sorted(params)])

      secret_key_bytes = secret_key.encode('ascii')
      signature = hmac.new(secret_key_bytes, msg=payload.encode('ascii'), digestmod=hashlib.sha256).hexdigest()


      Details_payload ={
              "id": id_value,
              "method": "order.place",
              "params": {
                          "apiKey": api_key,
                          "quantity":quantity,
                          "recvWindow" : 2000,
                          "side":side,
                          "symbol":trade_pair,
                          "timestamp": Time,
                          "type": "MARKET",
                          "signature": signature
                                }  }
      
      ws.send(json.dumps( Details_payload ))
      response = ws.recv()
      trading_data = json.loads(response)
      if 'status' in trading_data  and trading_data ['status'] == 200:
        print( Fore.GREEN + " Coreection trade was successful")
        return True
        
      else:
        print( Fore.RED + f" error in Coreection trading   {trading_data}")
        return False
    
    except Exception as e:
      errorcode = 1
      with open("counters/error.json", 'w') as json_file:
        json.dump(errorcode, json_file)
      print( Fore.RED + f"an exception error has occured in Coreection trading  {e}")
  except Exception as e:
    errorcode = 1
    with open("counters/error.json", 'w') as json_file:
      json.dump(errorcode, json_file)
    print( Fore.RED + f"  an exception error has occured in Coreection trading  {e}")



  
if __name__ == "__main__":
  
  Coreection_trade()




# Print or use the result