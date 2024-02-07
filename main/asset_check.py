import json 


from queue import Queue
from colorama import init, Fore
from Real_time_balance import RealTime_Account_Details



init()
result_queue = Queue()
def Account_status_check():
  print("------------------------------------------------------------checking for transfer confirmation ----------------------------------------------")
  try:
    with open("data/tradeInfo.json", 'r') as json_file:
      details = json.load(json_file)
    trade_pair = details[0]['symbol']
  
    with open("data/maintrade.json", 'r') as json_file:
      trade  = json.load(json_file)
    Main_crypto = trade[0]['main']

    if trade_pair.startswith(Main_crypto ):
      currency  = trade_pair[len(Main_crypto ):]

    else:
      currency = trade_pair[:-len(Main_crypto )]

    x = 0
  
    while x == 0:
      try:
        with open("current/preTrade_balance.json", 'r') as json_file:
          Pre_trade_acount = json.load(json_file)
        extracted_balances = RealTime_Account_Details()

        result = {}

        result[currency] = {}
        for nested_key, nested_value in extracted_balances[currency].items():
          if nested_key in Pre_trade_acount[currency]:
            result[currency][nested_key] = nested_value - Pre_trade_acount[currency][nested_key]
          else:
            result[currency][nested_key] = nested_value

# Check for positive increases
        positive_increase = {nested_key: nested_value for nested_key, nested_value in result[currency].items() if nested_value > 0}
        

        if positive_increase:
          #charges = 0.001 * positive_increase
          print( Fore.GREEN + f"  previous trade has been confirmed on {currency}: {positive_increase}")
          
          # tax update 
          with open("data/tax.json", 'r') as json_file:
            tax_account = json.load(json_file)
          tax_crypto_value = tax_account[currency]["Tax"]
          increment = positive_increase['free']
          tax = (0.001 * float(increment)) + tax_crypto_value
          tax_account[currency]["Tax"] = tax
          updated_tax_account = json.dumps(tax_account, indent=4)
          with open("data/tax.json", 'w') as file:
            file.write(updated_tax_account)

          x += 1
        else:
          x += 0
          print( Fore.YELLOW + f"Still awaiting comfirmation on {currency}.")

      except Exception as e:
        errorcode = 1
        with open("counters/error.json", 'w') as json_file:
          json.dump(errorcode, json_file)
        print( Fore.RED +f"an Exception error has occured{e}")

    print("\033[92m asset confirmed \033[0m")
    result_queue.put(True)
  except Exception as e:
    errorcode = 1
    with open("counters/error.json", 'w') as json_file:
      json.dump(errorcode, json_file)
    print( Fore.RED + f"an Exception error has occured in checking for transfer confirmation{e}")

  



if __name__ == "__main__":
  Account_status_check()



def Account_status_check_result():
    return result_queue.get()