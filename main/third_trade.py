
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
from queue import Queue

from realtime import Real_time
from idcreation import id_Creation
from Real_time_balance import RealTime_Account_Details
from exchange_info import exchange_info



init()
result_queue = Queue()
def Third_trade():
  print("-----------------------------------------Third Trade Has started--------------------------------------------------------------------")
  try:
    api_key = "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe"
    secret_key = "l2ryxyHlrZep2kcuitbC4L3ngUeIuLcmCH16ztZ57GOs0fdixMCkeGzb2BGrK7dq"
    url = "wss://testnet.binance.vision/ws-api/v3"
    # trade details 
    with open("data/tradeInfo.json", 'r') as json_file:
      details = json.load(json_file)
    # main crypto 
    with open("data/maintrade.json", 'r') as json_file:
      trade  = json.load(json_file)
    Main_crypto = trade[0]['main']

  # getting current trading crypto  
    second_trade = details[2]['symbol']
    if second_trade.startswith(Main_crypto ):
      Current_crypto  = second_trade[len(Main_crypto ):]

    else:
      Current_crypto = second_trade[:-len(Main_crypto )]
    

    with open("current/preTrade_balance.json", 'r') as json_file:
      Pre_trade_acount = json.load(json_file)
    previous_account  = Pre_trade_acount[Current_crypto]["free"]
    
    




      
    #trade pair 
    trade_pair = details[2]['symbol']

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
    extracted_balances = RealTime_Account_Details()

    # changes  from made here
    #current_account = 
    Main_account = extracted_balances[Current_crypto]["free"]#current_account - previous_account

    if trade_pair.startswith(Current_crypto):
      trade_quantity = Main_account
      side ="SELL"
    
    else:
      trade_quantity = Main_account * (1/(float(details[2]['price'])))
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
        print(Fore.GREEN + "Third trade was successful ")
        result_queue.put(True)
        
      else:
        print(Fore.RED + f"error in second trading{trading_data}")
        result_queue.put(False)
    
    except Exception as e:
      errorcode = 1
      with open("counters/error.json", 'w') as json_file:
          json.dump(errorcode, json_file)
      print( Fore.RED + f"an exception error has occured in Third trade  {e}")

  except Exception as e:
      errorcode = 1
      with open("counters/error.json", 'w') as json_file:
          json.dump(errorcode, json_file)
      print( Fore.RED + f"an exception error has occured in Third trade {e}")  



  
if __name__ == "__main__":
  
  Third_trade()


def Third_trade_result():
    return result_queue.get()