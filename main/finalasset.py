import threading
import time 
import os
import json 
import websocket
from datetime import datetime
from colorama import init, Fore
from final_balance import Final_Account_Details


def Finalcal_asset():

  print(" --------------------------------------------calculating total profit or loss----------------------------------- ")
  try:
    with open("current/opening_balance.json",'r') as json_file:
      account_data = json.load(json_file)
    
    with open("data/allcrypto.json", "r") as json_file:
      assets_to_extract = json.load(json_file)

    pre_trade_Balance = {}

  # Loop through the provided balance data
    for asset_data in account_data.get("result", {}).get("balances", []):
      asset_symbol = asset_data.get("asset")
      if asset_symbol in assets_to_extract:
        pre_trade_Balance[asset_symbol] = {
              "free": float(asset_data.get("free", 0)),
              "locked": float(asset_data.get("locked", 0))
                                                              }
    
    extracted_balances = Final_Account_Details()
    
    differences = {key: extracted_balances[key]['free'] - pre_trade_Balance[key]['free'] for key in pre_trade_Balance.keys()}
    percentage_differences = {key: (differences[key] / pre_trade_Balance[key]['free']) * 100 for key in pre_trade_Balance.keys()}

    sorted_items = sorted(percentage_differences.items(), key=lambda x: x[1], reverse=True)

    for key, percentage in sorted_items:
      if percentage > 0:
          print(Fore.GREEN + f"{key}: {differences[key]}, {percentage}% ")
      elif percentage == 0:
          print(Fore.YELLOW +  f"{key}:{differences[key]}, {percentage}%")
      else:
          print( Fore.RED + f"{key}:{differences[key]}, {percentage}% \033[0m")
    
    print( Fore.GREEN + "Final trade asset has been calculated  successfully ")

  except Exception as e:
     errorcode = 1
     with open("counters/error.json", 'w') as json_file:
       json.dump(errorcode, json_file)
     print( Fore.RED +  f"An exception error occurred in final asset {e}")
if __name__ == "__main__":
  Finalcal_asset()