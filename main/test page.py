import json 



from colorama import init, Fore
from current_prices import Current_price_forAll
#from allBal import all_Account_Details


init()
def asset_value():
  print("------------------------------------------------------------ Opeaning Value of asset  is about to be checked ----------------------------------------------")
  try: 
  #creating pairs 
    with open("data/allcrypto.json", 'r') as json_file:
      data  = json.load(json_file) 
    front_usdt_data = ["USDT" + item for item in data]
    back_usdt_data = [item + "USDT" for item in data]
    extract = front_usdt_data + back_usdt_data

    Current_ExchangePrices = Current_price_forAll()
    extracted_prices = {}
    for symbol in extract:
      prices = [1 / float(item['price']) if item['symbol'].startswith("USDT") else float(item['price']) for item in Current_ExchangePrices['result'] if item['symbol'] == symbol]
      price = prices[0] if prices else None
      extracted_prices[symbol.replace("USDT", "")] = price

    extracted_prices = {symbol: price for symbol, price in extracted_prices.items() if price is not None}
    
    # account_data = all_Account_Details()
    with open("data/tax.json", 'r') as json_file:
      account_data  = json.load(json_file) 


    usdt_balance = next((balance_data["Tax"] for token, balance_data in account_data.items() if token == "USDT"), None)
    
    total_values = {}
    for symbol, price in extracted_prices.items():
      balance_data = next((balance_data["Tax"] for token, balance_data in account_data.items() if token == symbol), None)
      print(balance_data)
      if balance_data is not None:
        total_value = balance_data * price  # Using balance_data directly as a float
        total_values[symbol] = total_value
      
    total_values = {symbol: value for symbol, value in total_values.items() if value is not None} 
    #total_values = list(map(float, total_values))
    overall_total_value = sum(total_values.values())
    total_asset = overall_total_value + float(usdt_balance)
    total_values['USDT']= float(usdt_balance)

    with open("data/openingasset.json", 'w') as json_file:
        json.dump(total_asset, json_file)


    print(Fore.YELLOW +  f" Opening Overall Asset is : {total_asset} USDT")
    print(total_values)
  except Exception as e:
    errorcode = 1
    with open("counters/error.json", 'w') as json_file:
      json.dump(errorcode, json_file)
    print( Fore.RED + f"an exception error has occured in Opeaning Value of asset{e}  ")

  
if __name__ == "__main__":
  asset_value()