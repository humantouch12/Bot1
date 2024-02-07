import random
import json
from colorama import init, Fore

init()


def Reaarange():
# random selection program 
  print("-------------------------------------------------------Re-shuffling process is taking place-----------------------------------------------------")
  try:
    with open("data/allcrypto.json",'r') as json_file:
      allcrypto = json.load(json_file)

    with open("data/maintrade.json", 'r') as json_file:
      trade  = json.load(json_file)
    Main_crypto = trade[0]['main']
    
  # Choose 4 random elements from the data list (excluding "USDT")
    random_selection = random.sample([item for item in allcrypto if item != Main_crypto], 9)

  # Append "USDT" to the result
    random_selection.append(Main_crypto)

    with open("data/pairs.json", 'w') as json_file:
      json.dump(random_selection, json_file)


    print( Fore.GREEN +"Re-shuffling process completed, New trading info are :",random_selection)
  except Exception as e:
        errorcode = 1
        with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
        print( Fore.RED + f"exception error occurred in Re-shuffling process {e}")


if __name__ == "__main__":
  Reaarange()



