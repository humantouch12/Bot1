import json 

from colorama import init, Fore




from allBal import all_Account_Details 
from usdt_check import usdt_asset_check
from current_prices import Current_price_forAll
from  correction_trade import Coreection_trade
from notional_check_single import Single_Notional_Cal

init()
def get_back():
  with open("counters/correctionperiod.json",'r') as json_file:
      correctionperiod = json.load(json_file)
   
  while correctionperiod < 4:
      try:
  #getting al variables 
         with open("current/prices.json", 'r') as json_file:
            starting_price = json.load(json_file)
         with open("counters/getback.json", 'r') as json_file:
            transac_count = json.load(json_file)


         account_data = all_Account_Details()
         Current_USDT = float(next(item["free"] for item in account_data["result"]["balances"] if item.get("asset") == "USDT" and "free" in item))
         
         if Current_USDT :
            Highest = usdt_asset_check()
            Main_crypto = Highest[0]
            main_value = Highest[1]
            Value =[main_value,Current_USDT ]
            with open("data/Highest.json", 'w') as json_file:
                  json.dump(Value, json_file)

            join1 = "USDT" + Main_crypto
            join2 = Main_crypto + "USDT"
            created_pairs = [join1, join2]
            for item in starting_price["result"]:
               if "symbol" in item and item["symbol"] in created_pairs:
                  Main_pair = item['symbol']
                  old_price = float(item['price'])
            Current_ExchangePrices  = Current_price_forAll()
            for item in Current_ExchangePrices["result"]:
               if "symbol" in item and item["symbol"] == Main_pair:
                  Current_price = float(item['price'])
               

            Details = [Main_crypto, Main_pair, Current_price]
            with open("data/correction.json", 'w') as json_file:
               json.dump(Details, json_file)
            print(old_price, Current_price)
            notional_check = Single_Notional_Cal()

            if notional_check:
            #print("here")    
               if old_price <= Current_price:
                  with open("counters/active.json", 'r') as json_file:
                     active = json.load(json_file)
               
               
                  if active == 1:
                     pause = 1
                     print("correction is starting")
                     with open("counters/pause.json", 'w') as json_file:
                        json.dump(pause, json_file)
                     correction = Coreection_trade()
                     if correction:
                        print(Fore.GREEN +f"correction has been made from {Main_crypto} to USDT successfully ")
                        

                        correctionperiod += 1
                        with open("counters/correctionperiod.json", 'w') as json_file:
                                json.dump(correctionperiod, json_file)
                        transac_count -=1
                        with open("counters/getback.json", 'w') as json_file:
                                json.dump(transac_count , json_file)

                        
                        
                     else:
                        correctionperiod += 1
                        with open("counters/correctionperiod.json", 'w') as json_file:
                                json.dump(correctionperiod, json_file)
                       
                        transac_count +=1
                        with open("counters/getback.json", 'w') as json_file:
                           json.dump(transac_count , json_file)
                        
                        print(Fore.RED + f"an error occured in correctting from {Main_crypto} to USDT suceesfully ")
               

                  else:
                     pass
         
         
         
         
               else:
                  print(" asset value is not  favourable trying again ")
                  correctionperiod += 1
               
                  with open("counters/correctionperiod.json", 'w') as json_file:
                     json.dump(correctionperiod, json_file)
               
                  transac_count +=1
                  with open("counters/getback.json", 'w') as json_file:
                     json.dump(transac_count , json_file)
               
            else:
                
                print(f"{Main_crypto} did not meet the required notional filter ")
                correctionperiod += 4
               
                with open("counters/correctionperiod.json", 'w') as json_file:
                     json.dump(correctionperiod, json_file)
         
         

      
         else:
            pass

      except Exception as e:
        errorcode = 1
        with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
        print( Fore.RED + f"exception error occured in get back function{e}") 
  with open("counters/getback.json", 'r') as json_file:
      transac_count = json.load(json_file)
  with open("data/Highest.json", 'r') as json_file:
      Values = json.load(json_file)
  Value_other = Values[0]   
  Value_Usdt = Values[1]       
  if transac_count ==4:
      if Value_Usdt > Value_other :
          print(" USDT is HIGH ")
          change = {"main": "USDT"}
          changes = [change]
          with open("data/maintrade.json",'w') as json_file:
               json.dump(changes, json_file, indent = 4 )
          print("------changing main trade to USDT----------")
          
      else:
         change = {"main": Main_crypto }
         changes = [change]
         with open("data/maintrade.json",'w') as json_file:
            json.dump(changes, json_file, indent = 4 )
         print(f"------changing main trade to {Main_crypto}----------")
  else:
     if Value_Usdt > Value_other :
          print(" USDT is HIGH ")
          change = {"main": "USDT"}
          changes = [change]
          with open("data/maintrade.json",'w') as json_file:
               json.dump(changes, json_file, indent = 4 )
          print("------changing main trade to USDT----------")
          
     else:
         change = {"main": Main_crypto }
         changes = [change]
         with open("data/maintrade.json",'w') as json_file:
            json.dump(changes, json_file, indent = 4 )
         print(f"------changing main trade to {Main_crypto}----------")
  
if __name__ == "__main__":
   get_back()