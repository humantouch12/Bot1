import requests
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
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime
from enum import Enum
from decimal import Decimal
from datetime import datetime
from queue import Queue
from colorama import init, Fore
from current_prices import Current_price_forAll


init()
result_queue = Queue()
def Trade_check():
  print("------------------------------------------------------------Checking for possible trade ----------------------------------------------")
  try:
  
    Current_ExchangePrices = Current_price_forAll()

    with open("data/maintrade.json", 'r') as json_file:
      trade  = json.load(json_file)
    Main_crypto = trade[0]['main']

    with open("data/pairs.json", 'r') as json_file:
      interest_pairs = json.load(json_file)

    Interest_pair_combinations = [''.join(pair) for pair in product(interest_pairs, repeat=2)]
    filtered_prices = [pair for pair in Current_ExchangePrices["result"] if pair["symbol"] in Interest_pair_combinations]

    #Filter symbols based on main crypto 
    Main_crypto_pairs = [item for item in filtered_prices if Main_crypto in item["symbol"]]
    non_Main_crypto_pairs = [item for item in filtered_prices if Main_crypto not in item["symbol"]]

    #creating a combinantion of 3 index array 
    combinations = list(product(Main_crypto_pairs , non_Main_crypto_pairs, Main_crypto_pairs))
    # Create a list to store the combinations
    combine_set = []

    # Append each combination to the result array
    for combo in combinations:
      combine_set.append(list(combo))
    
    # another step starts here 

    first_set_sorting  = []
    for subarray in combine_set:
      # Step 1: Check for similarities between index0 and index1, and index1 and index2
      similarity_01 = SequenceMatcher(None, subarray[0]['symbol'], subarray[1]['symbol']).find_longest_match(0, len(subarray[0]['symbol']), 0, len(subarray[1]['symbol'])).size >= 3
      similarity_12 = SequenceMatcher(None, subarray[1]['symbol'], subarray[2]['symbol']).find_longest_match(0, len(subarray[1]['symbol']), 0, len(subarray[2]['symbol'])).size >= 3

      # If there are no similarities between index0 and index1 or between index1 and index2, skip the subarray
      if not (similarity_01 and similarity_12):
          continue

      # If there are similarities, add the subarray to the result
      first_set_sorting.append(subarray)

  # another step starts here 
    second_set_sorting = []
    for i, sub_array in enumerate(first_set_sorting):
        symbol0 = sub_array[0]['symbol']
        symbol1 = sub_array[1]['symbol']

          # Initialize SequenceMatcher
        matcher = SequenceMatcher(None, symbol0, symbol1)

      # Find matching blocks
        matching_blocks = matcher.get_matching_blocks()
      
      # Filter blocks based on minimum similarity
        relevant_blocks = [block for block in matching_blocks if block.size >= 3]

        for block in relevant_blocks:
            start = block.a
            end = block.a + block.size
            similarity = symbol0[start:end]

            if similarity in sub_array[2]['symbol']:
                #print("not needed")
              pass
            else:
              second_set_sorting.append(sub_array)
    # another step starts here 
    max_trade_cal = float('-inf')  # Initialize max_trade_cal with negative infinity
    max_trade_cal_subarray = None

    for data in second_set_sorting:
      # Extract symbols from index 0 and index 1
      symbols_0 = data[0]['symbol']
      symbols_1 = data[1]['symbol']

          # Calculate similarity using SequenceMatcher
      matcher = SequenceMatcher(None, symbols_0, symbols_1)
      match_blocks = matcher.get_matching_blocks()

          # Filter blocks with at least 3 letters similarity
      similarities = [block for block in match_blocks if block.size >= 3]

      # Print similarities
      for block in similarities:
          start_idx_0 = block.a
          start_idx_1 = block.b
          size = block.size
          centre_part = symbols_0[start_idx_0:start_idx_0 + size]
          
      
      # Check if "BTC" is at the beginning or end of the 'symbol' in the first dictionary
      first_symbol = data[0]['symbol']
      if first_symbol.startswith(Main_crypto):
          price1 = float(data[0]['price'])
      else:
          price1_cal = float(data[0]['price'])
          price1 = 1 / price1_cal

      second_symbol = data[1]['symbol']
      if second_symbol.startswith(centre_part):
          price2 = float(data[1]['price'])
      else:
          price2_cal = float(data[1]['price'])
          price2 = 1 / price2_cal

      third_symbol = data[2]['symbol']
      if third_symbol.startswith(Main_crypto):
          price3_cal = float(data[2]['price'])
          price3 = 1 / price3_cal
          
      else:
          price3 = float(data[2]['price'])
      

      # Add similar logic for the third symbol (data[2]) as you did before

      # Calculate trade_cal for each data list
      trade_cal = price1 * price2 * price3
      if trade_cal > max_trade_cal:
          max_trade_cal = trade_cal
          max_trade_cal_subarray = data
    
    if max_trade_cal >= 1.004:
      with open("data/tradeInfo.json" ,'w') as json_file:
        json.dump(max_trade_cal_subarray, json_file)
      print(Fore.GREEN +"Trade has be successfully Gotten")
      print(f" trade details: Rate :{max_trade_cal}, main trade : {Main_crypto}, Details:{max_trade_cal_subarray}")
      result_queue.put(True)
    else:
      
      print(Fore.YELLOW + "No Available Trade ")
      result_queue.put(False)
  except Exception as e:
      errorcode = 1
      with open("counters/error.json", 'w') as json_file:
          json.dump(errorcode, json_file)
      print( Fore.RED + f"an exception error has occured in Trade_check {e}")  


if __name__ == "__main__":
  Trade_check()


def trade_Check_result():
    return result_queue.get()
# Print or use the result



