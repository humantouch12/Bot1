import json


from colorama import init, Fore
from exchange_info import exchange_info
from Real_time_balance import RealTime_Account_Details

from queue import Queue


init()
result_queue = Queue()
def Notional_Cal():


  print("----------------------------------------- checking for notional requirement --------------------------------------------------------------------")
  try:
    with open("data/tradeinfo.json", 'r') as json_file:
      tradeInfo = json.load(json_file)
    
    with open("data/maintrade.json", 'r') as json_file:
      trade  = json.load(json_file)
    Main_crypto = trade[0]['main']
      

    exchangeInfo_data = exchange_info()
    extracted_balances = RealTime_Account_Details()
    first = tradeInfo[0]['symbol']
    second = tradeInfo[1]['symbol']
    third = tradeInfo[2]['symbol']
    first_price =  float(tradeInfo[0]['price'])
    second_price =  float(tradeInfo[1]['price'])
    third_price =  float(tradeInfo[2]['price'])
    
    first_acc_get = extracted_balances.get(Main_crypto, {}).get('free')
    first_acc = 0.9 * first_acc_get

    first_check  = next((symbol for symbol in exchangeInfo_data ["result"]["symbols"] if symbol["symbol"] == first), None)
    first_notional_filter = next((filter_data for filter_data in first_check["filters"] if filter_data["filterType"] == "NOTIONAL"), None)
    first_minNotional = float(first_notional_filter["minNotional"])
    first_maxNotional = float(first_notional_filter["maxNotional"])

    if first.startswith(Main_crypto):
      first_cal = first_acc * first_price 
      second_acc  = first_acc * first_price 
    else:
      first_cal = (first_acc * 1/first_price) * first_price
      second_acc = (first_acc * 1/first_price)

    if first_cal >= first_minNotional:
      first_result = 1
      print( Fore.GREEN + "  First trade meet the notional requirement ")
    else:
      first_result = 0
      print( Fore.RED + " First trade does not meet the notional requirement")
    


    # second check start here 
    if first.startswith(Main_crypto ):
      second_crypto  = first[len(Main_crypto ):]

    else:
      second_crypto = first[:-len(Main_crypto )]

    second_check  = next((symbol for symbol in exchangeInfo_data ["result"]["symbols"] if symbol["symbol"] == second), None)
    second_notional_filter = next((filter_data for filter_data in second_check["filters"] if filter_data["filterType"] == "NOTIONAL"), None)
    second_minNotional = float(second_notional_filter["minNotional"])
    second_maxNotional = float(second_notional_filter["maxNotional"])

    if second.startswith(second_crypto):
      second_cal = second_acc * second_price
      third_acc  = second_acc * second_price
    else:
      second_cal= (second_acc * 1/second_price) * second_price

      third_acc = (second_acc * 1/second_price)
    
    if second_cal >= second_minNotional:
      second_result = 1
      print( Fore.GREEN + "second trade meet the notional requirement")
    else:
      second_result = 0
      print(Fore.RED + " second trade does not meet the notional requirement ")
    
    # third check start here 

    if third.startswith(Main_crypto ):
      third_crypto  = third[len(Main_crypto ):]

    else:
      third_crypto = third[:-len(Main_crypto )]

    third_check  = next((symbol for symbol in exchangeInfo_data ["result"]["symbols"] if symbol["symbol"] == third), None)
    third_notional_filter = next((filter_data for filter_data in third_check["filters"] if filter_data["filterType"] == "NOTIONAL"), None)
    third_minNotional = float(third_notional_filter["minNotional"])
    third_maxNotional = float(third_notional_filter["maxNotional"])

    if third.startswith(third_crypto):
      third_cal = third_acc * third_price
      
    else:
      third_cal= (third_acc * 1/third_price) * third_price

    if third_cal >= third_minNotional:
      third_result = 1
      print( Fore.GREEN + "third trade meet the notional requirement" )
    else:
      third_result = 0
      print(Fore.RED + " third trade does not meet the notional requirement")
    
    final_result = first_result + second_result + third_result

    if final_result == 3:
      print("  Trades pass the Notional Check  ")
      result_queue.put(True)
    else:
      print(Fore.RED + " one or more trade did not meet the notional requirement")
      result_queue.put(False)
  except Exception as e:
    errorcode = 1
    with open("counters/error.json", 'w') as json_file:
      json.dump(errorcode, json_file)
    print(Fore.RED + f"an exception error occurred in Notional check {e}")  

if __name__ == "__main__":
 
  Notional_Cal()


def Notional_Cal_result():
    return result_queue.get()