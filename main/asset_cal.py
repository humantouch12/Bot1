import threading
import time 
import os
import json 
import websocket
from datetime import datetime
from colorama import init, Fore
from Real_time_balance import RealTime_Account_Details


init()
def cal_asset():

  print(" --------------------------------------------calculating current profit or loss----------------------------------- ")
  try:
      with open("current/preTrade_balance.json",'r') as json_file:
        pre_trade_Balance = json.load(json_file)

  
      extracted_balances = RealTime_Account_Details()
      differences ={}
      for key in pre_trade_Balance.keys():
        if key in extracted_balances and 'free' in extracted_balances[key] and key in pre_trade_Balance and 'free' in pre_trade_Balance[key]:
            differences[key] = extracted_balances[key]['free'] - pre_trade_Balance[key]['free']
      percentage_differences = {key: ((differences[key] / pre_trade_Balance[key]['free']) * 100) if pre_trade_Balance[key]['free'] != 0 else 0 for key in differences.keys()}

      sorted_items = sorted(percentage_differences.items(), key=lambda x: x[1], reverse=True)

      for key, percentage in sorted_items:
        if percentage > 0:
            print(  f"{key}: {differences[key]}, {percentage}%")
        elif percentage == 0:
            print(Fore.GREEN +  f"{key}:{differences[key]}, {percentage}%")
        else:
            print(f"\033[91m{key}:{differences[key]}, {percentage}% \033[0m")
  
      print( Fore.RED +"\033[92mcurrent trade asset has been calculated  successfully \033[0m")
  except Exception as e:
     errorcode = 1
     with open("counters/error.json", 'w') as json_file:
        json.dump(errorcode, json_file)
     print( Fore.RED + f" an Exception error occured in calculating current profit or loss ")
     

if __name__ == "__main__":

  cal_asset()