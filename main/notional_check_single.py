import json


from colorama import init, Fore
from exchange_info import exchange_info
from Real_time_balance import RealTime_Account_Details




init()

def Single_Notional_Cal():


  print("----------------------------------------- checking for single notional requirement --------------------------------------------------------------------")
  try:
    with open("data/correction.json", 'r') as json_file:
      Trade_details = json.load(json_file)

    Main_crypto = Trade_details[0]
    
    exchangeInfo_data = exchange_info()
    extracted_balances = RealTime_Account_Details()

    first = Trade_details[1]
    first_price = Trade_details[2]  
    
    
    first_acc_get = extracted_balances.get(Main_crypto, {}).get('free')
    first_acc = 0.95 * first_acc_get
    
    first_check  = next((symbol for symbol in exchangeInfo_data ["result"]["symbols"] if symbol["symbol"] == first), None)
    first_notional_filter = next((filter_data for filter_data in first_check["filters"] if filter_data["filterType"] == "NOTIONAL"), None)
    first_minNotional = float(first_notional_filter["minNotional"])
    first_maxNotional = float(first_notional_filter["maxNotional"])

    if first.startswith(Main_crypto):
      first_cal = first_acc * first_price 
      
    else:
      first_cal = (first_acc * 1/first_price) * first_price
      

    if first_cal >= first_minNotional:
      
      print( Fore.GREEN + "   notional requirement has been met")
      return True
    else:
      
      print( Fore.RED + "  notional requirement was not met")
      return False 
    



  except Exception as e:
    errorcode = 1
    with open("counters/error.json", 'w') as json_file:
      json.dump(errorcode, json_file)
    print(Fore.RED + f"an exception error occurred in Notional check {e}")  

if __name__ == "__main__":
 
  Single_Notional_Cal()

