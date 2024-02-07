import json 



from colorama import init, Fore
from current_prices import Current_price_forAll
from allBal import all_Account_Details


init() 
def Current_asset_value():
  print("------------------------------------------------------------ Current Value of asset  is about to be checked ----------------------------------------------")
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
    
    account_data = all_Account_Details()
    usdt_balance = next((balance['free'] for balance in account_data['result']['balances'] if balance['asset'] == 'USDT'), None)
    total_values = {}
    for symbol, price in extracted_prices.items():
      balance_data = next((balance for balance in account_data['result']['balances'] if balance['asset'] == symbol), None)
      if balance_data:
        total_value = float(balance_data['free']) * float(price)
        print(total_value)
        total_values[symbol] = total_value
      
    total_values = {symbol: value for symbol, value in total_values.items() if value is not None} 
    #total_values = list(map(float, total_values))
    overall_total_value = sum(total_values.values())
    total_asset = overall_total_value + float(usdt_balance)

    with open("data/pre_asset.json", 'r') as json_file:
        pre_asset= json.load(json_file)
    current_total = total_asset - pre_asset

    if current_total > 0:
      print( Fore.GREEN + f"Current over all asset is :{total_asset}:USDT, you Gained: {current_total} ")
    else:
      print(Fore.RED + f"Current over all asset is :{total_asset}:USDT,  you loss {current_total}:USDT ")
  except Exception as e:
    errorcode = 1
    with open("counters/error.json", 'w') as json_file:
      json.dump(errorcode, json_file)
    print( Fore.RED + f"an exception error has occurred {e}")

  

  
if __name__ == "__main__":
  Current_asset_value()