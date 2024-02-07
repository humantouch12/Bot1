
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'main'))

#API Key: 26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe

#Secret Key: l2ryxyHlrZep2kcuitbC4L3ngUeIuLcmCH16ztZ57GOs0fdixMCkeGzb2BGrK7dq
# import of all necessary libuaries 
import threading
import time 

import json 
import websocket
import datetime

import subprocess
#importation of necessary pages 
from colorama import init, Fore

from main.internetConn import is_internet_available
from main.current_prices import Current_price_forAll
from main.ping_check import Ping_frame
from main.openingbal import Opening_Account_Details, get_opening_account_result
from main.pre_trade_Balance import PreTrade_Account_Details, get_pretrade_account_result
from main.asset_cal import cal_asset
from main.finalasset import Finalcal_asset
from main.trade_check import Trade_check, trade_Check_result
from main.first_trade import First_trade, First_trade_result
from main.asset_check import Account_status_check, Account_status_check_result
from main.second_trade import Second_trade, Second_trade_result
from main.asset_check2 import Account_status_check2, Account_status_check2_result
from main.third_trade import Third_trade, Third_trade_result
from main.asset_check3 import Account_status_check3
from main.rearrange import Reaarange
from main.Notional_check import Notional_Cal, Notional_Cal_result
from main.wait import Wait
from main.asset_value import asset_value
from main.pre_trade_asset_value import Pre_asset_value
from main.current_asset_value import Current_asset_value
#from main.Alarm import play_alarm_sound
from main.store import get_back
from main.current_mainaccount import RealTime_Main_Account_Details
from main.All_tax_cal import Tax_value
# pause threading events for functions to pause 





# variables 





init()



def curr_time():
     current_time = datetime.datetime.now()
     print("Trade Start/End Time :", current_time)

def fix():
    print(Fore.YELLOW +"  stopping all proccesse for 10s ")
    time.sleep(10)
    print("------Restarting the program-----")
    # Get the directory of the currently executing script
    script_dir = os.path.dirname(__file__)
    # Specify the name of your script
    script_name = "main.py"
    # Join the directory path with the script name
    script_path = os.path.join(script_dir, script_name)
    # Run the script with the appropriate Python interpreter
    python_path = sys.executable
    subprocess.run([python_path, script_path] + sys.argv[1:])




def Error_checker():
    try:
      with open("counters/error.json", 'r') as json_file:
          error = json.load(json_file)
      if error == 1:
          errorcode = 0
          with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
          resolve = fix()
      else:
          pass
    except Exception as e:
       
   
        with open("counters/error.json", 'r') as json_file:
          error = json.load(json_file)
        if error == 1:
          print(Fore.YELLOW +"  stopping all proccesse for 10s ")
          errorcode = 0
          with open("counters/error.json", 'w') as json_file:
            json.dump(errorcode, json_file)
          resolve = fix()
 

def cummulative():
    with open("counters/cummulative.json", 'r') as json_file:
        cumm_count = json.load(json_file)
    cumm_count +=1
    with open("counters/cummulative.json", 'w') as json_file:
            json.dump(cumm_count, json_file)
            

def Positive_Signal():
    positive = 1
    with open("counters/sectionSig.json", 'w') as json_file:
        json.dump(positive , json_file)

def Negative_Signal():
    Negative = 0
    with open("counters/sectionSig.json", 'w') as json_file:
        json.dump(Negative , json_file)  

def Replacements():
    resets = 0
    active = 1
    
    with open("counters/active.json", 'w') as json_file:
        json.dump(active, json_file)
    with open("counters/correctionperiod.json", 'w') as json_file:
            json.dump(resets, json_file)
    
    with open("counters/cummulative.json", 'w') as json_file:
            json.dump(resets, json_file)

    with open("counters/error.json", 'w') as json_file:
        json.dump(resets, json_file)

    with open("counters/exceptionCounter.json", 'w') as json_file:
            json.dump(resets, json_file)
    
    with open("counters/noTrade.json", 'w') as json_file:
            json.dump(resets, json_file)

    with open("counters/openingBal.json", 'w') as json_file:
            json.dump(resets, json_file)
                
    with open("counters/price.json", 'w') as json_file:
        json.dump(resets, json_file)
    
    with open("data/previous.json", 'w') as json_file:
        json.dump({}, json_file)
    
    with open("data/previous2.json", 'w') as json_file:
        json.dump({}, json_file)
    

def Final_Replacements():
    replace = Replacements()

    final = 0 
    with open("counters/main.json", 'w') as json_file:
        json.dump(final, json_file)
    with open("counters/counter.json", 'w') as json_file:
        json.dump(final, json_file)

    with open("counters/secondary.json", 'w') as json_file:
        json.dump(final, json_file)
    with open("data/tax.json", 'r') as json_file:
        Tax_data = json.load(json_file)

# Update the "Tax" values to 0.0
    for key in Tax_data:
        Tax_data[key]["Tax"] = 0.0

# Write the updated data back to the JSON file
    with open("data/tax.json", 'w') as json_file:
        json.dump(Tax_data, json_file, indent=4)


    




def Main_Execution():
    while is_internet_available():
        P_Status = Positive_Signal()
        with open("counters/main.json", 'r') as json_file:
                main_counts = json.load(json_file)
        if main_counts == 0:
            Time = curr_time()
            print("------------------------------------------------------------------------------------------------------Trading bot  is about to Start an session-------------------------------------------------------------------------------------")
            main_counts +=1
            with open("counters/main.json", 'w') as json_file:
                    json.dump(main_counts, json_file)
        else:
            print(f"------------------------------------------------------------------------------------------------------Re-running Trading bot for {main_counts} time in same session-------------------------------------------------------------------------------------")
            main_counts +=1
            with open("counters/main.json", 'w') as json_file:
                    json.dump(main_counts, json_file)

        with open("counters/Finalcounter.json",'r') as json_file:
                Final_counter = json.load(json_file)

        while Final_counter < 20:
            try:
                Current_price_forAll
                price_thread = threading.Thread(target= Current_price_forAll)
                price_thread.start()

                price_thread.join()


                ping_thread = threading.Thread(target= Ping_frame)
                ping_thread.start()

                if main_counts == 1:
                    opening_asset_thread = threading.Thread(target = asset_value)
                    opening_asset_thread.start()

                    opening_asset_thread.join
                else:
                    pass
                correction  = Error_checker()
                openingAccount_thread = threading.Thread(target= Opening_Account_Details)
                openingAccount_thread.start()

                openingAccount_thread.join()
                opening_Acc_Result = get_opening_account_result()
                correction  = Error_checker()

                if opening_Acc_Result:

                # another while loop 
                    with open("counters/counter.json",'r') as json_file:
                        counter = json.load(json_file)
                    # another while loop 
                    while counter < 10:

                        with open("counters/noTrade.json",'r') as json_file:
                            Trades = json.load(json_file)

                        with open("counters/cummulative.json", 'r') as json_file:
                            cummulative_check = json.load(json_file)


                        if cummulative_check >= 2:
                            correctionperiod = 0
                            with open("counters/correctionperiod.json", 'w') as json_file:
                                    json.dump(correctionperiod, json_file)
            
                            active = 1
                            with open("counters/active.json", 'w') as json_file:
                                    json.dump(active, json_file)
                            
                            All_assetTo_USDT_thread = threading.Thread(target= get_back)
                            All_assetTo_USDT_thread.start()

                            All_assetTo_USDT_thread.join()
                            reset_cumm_count = 0
                            with open("counters/cummulative.json", 'w') as json_file:
                                json.dump(reset_cumm_count, json_file)

                            with open("counters/active.json", 'w') as json_file:
                                json.dump(reset_cumm_count, json_file)

                            with open("counters/getback.json", 'w') as json_file:
                                json.dump(reset_cumm_count, json_file)
                            resolve = fix()

                        else:
                            pass

                        correction  = Error_checker()
                        pretradeasset_thread = threading.Thread(target= Pre_asset_value)
                        pretradeasset_thread.start()

                        pretradeasset_thread.join()
                        correction  = Error_checker()
                        pretradeBal_thread = threading.Thread(target= PreTrade_Account_Details)
                        pretradeBal_thread.start()

                        pretradeBal_thread.join()
                        pretradeBal_Result = get_pretrade_account_result()
                        correction  = Error_checker()
                        if pretradeBal_Result:
                            
                            trading_check_thread = threading.Thread(target= Trade_check)
                            trading_check_thread.start()
    
                            trading_check_Result = trade_Check_result()
                            correction  = Error_checker()
                            if trading_check_Result:

                                N_Status = Negative_Signal()
                                Notional_thread = threading.Thread(target = Notional_Cal)
                                Notional_thread.start()

                                Notional_Results = Notional_Cal_result()

                                correction  = Error_checker()
                                if Notional_Results:
                                    first_trade_thread = threading.Thread(target= First_trade)
                                    first_trade_thread.start()

                                    first_trade_Result = First_trade_result()
                                    correction  = Error_checker()
                                    
                                    if first_trade_Result:
                                        value_update_thread = threading.Thread(target= RealTime_Main_Account_Details)
                                        value_update_thread.start()
                                        Confirmation_thread = threading.Thread(target= Account_status_check)
                                        Confirmation_thread.start()

                                        Confirmation_Result = Account_status_check_result()

                                        if Confirmation_Result:
                                            correction  = Error_checker()
                                            second_trade_thread = threading.Thread(target= Second_trade )
                                            second_trade_thread.start()

                                            second_trade_Result = Second_trade_result()
                                            correction  = Error_checker()
                                            if second_trade_Result:
                                                Confirmation_thread2 = threading.Thread(target= Account_status_check2)
                                                Confirmation_thread2.start()

                                                Confirmation_Result2 = Account_status_check2_result()
                                                correction  = Error_checker()
                                                if Confirmation_Result2:
                                                    third_trade_thread = threading.Thread(target= Third_trade )
                                                    third_trade_thread.start()

                                                    third_trade_Result = Third_trade_result()
                                                    correction  = Error_checker()
                                                    if third_trade_Result:
                                                        Confirmation_thread3 = threading.Thread(target= Account_status_check3)
                                                        Confirmation_thread3.start()

                                                        Confirmation_thread3.join()

                                                        wait_thread = threading.Thread(target = Wait)
                                                        wait_thread.start()

                                                        wait_thread.join()
                                                        correction  = Error_checker()
                                                        P_Status = Positive_Signal()
                                                        assetCal_thread = threading.Thread(target =  cal_asset)
                                                        assetCal_thread.start()

                                                        assetCal_thread.join()
                                                        correction  = Error_checker()
                                                        currenttradeasset_thread = threading.Thread(target= Current_asset_value)
                                                        currenttradeasset_thread .start()

                                                        currenttradeasset_thread .join()
                                                        correction  = Error_checker()

                                                        if counter == 9:
                                                            Final_counter += 1
                                                            with open("counters/Finalcounter.json",'r') as json_file:
                                                                json.dump(Final_counter, json_file)

                                                            print(f"section trades {Final_counter}")
                                                                    
                                                            counter = 0
                                                            with open("counters/counter.json", 'w') as json_file:
                                                                json.dump(counter, json_file)
                                                            print("10 sucessfull trade has been completed ")
                                                            replace = Replacements()
                                                        else :
                                                            counter +=  1
                                                            print(f"{counter} completed Trade(s)")
                                                            with open("counters/counter.json", 'w') as json_file:
                                                                json.dump(counter, json_file)
                                                            reset_cumm_count = 0
                                                            with open("counters/cummulative.json", 'w') as json_file:
                                                                json.dump(reset_cumm_count, json_file)
                                                        
                                                    
                                                            

                                                        #error fix function and start again , error count 

                                                    else:
                                                        P_Status = Positive_Signal()
                                                        print("\033[93m---currently working on fix for third trade error--\033[0m")

                                                        with open("data/maintrade.json", 'r') as json_file:
                                                            crypto= json.load(json_file)
                                                        Main_crypto = crypto[0]['main']

                                                        with open("data/tradeinfo.json",'r') as json_file:
                                                            tradeinfo = json.load(json_file)
                                                        trade = tradeinfo[2]['symbol']

                                                        if trade.startswith(Main_crypto ):
                                                            Current_crypto  = trade[len(Main_crypto ):]
                                                        else:
                                                            Current_crypto = trade[:-len(Main_crypto )]
    

                                                        change = {"main": Current_crypto}
                                                        changes = [change]

                                                        with open("data/maintrade.json",'w') as json_file:
                                                            json.dump(changes, json_file, indent = 4 )
                                                        
                                                        print("\033[92m---fix for third trade error completed--\033[0m")
                                                        resolve = fix()
                                                        

                                                else:
                                                    continue 
                                                    
                                                #error fix function and start again , error count 


                                            else:
                                                P_Status = Positive_Signal()
                                                print("\033[93m---currently working on fix for second trade error--\033[0m")
                                                with open("data/maintrade.json", 'r') as json_file:
                                                    crypto= json.load(json_file)
                                                Main_crypto = crypto[0]['main']
                                                with open("data/tradeinfo.json",'r') as json_file:
                                                    tradeinfo = json.load(json_file)
                                                trade = tradeinfo[0]['symbol']

                                                if trade.startswith(Main_crypto ):
                                                    Current_crypto  = trade[len(Main_crypto ):]
                                                else:
                                                    Current_crypto = trade[:-len(Main_crypto )]
                                                change = {"main": Current_crypto}
                                                changes = [change]
                                                with open("data/maintrade.json",'w') as json_file:
                                                    json.dump(changes, json_file, indent = 4 )
                                                print("\033[92m---fix for second trade error completed--\033[0m")
                                                resolve = fix()
                                                


                                        else:
                                            continue
                                        #error fix function and start again , error count 
                                    else:
                                        P_Status = Positive_Signal()
                                        if Trades ==3:
                                            countUp = cummulative()
                                            Reaarange_thread = threading.Thread(target= Reaarange)
                                            Reaarange_thread .start()
                                            Trades = 0
                                            with open("counters/noTrade.json", 'w') as json_file:
                                                json.dump(Trades, json_file)
                                        else:
                                            Trades += 1
                                            with open("counters/noTrade.json", 'w') as json_file:
                                                json.dump(Trades, json_file)

                                            with open("counters/error.json",'r') as json_file:
                                                error  = json.load(json_file)
                                            error += 1
                                            print(error,":\033[91m error occurance(s)\033[0m")
                    
                                            with open("counters/error.json", 'w') as json_file:
                                                json.dump(error, json_file)
                                            resolve = fix()



                                else:
                                    P_Status = Positive_Signal()
                                    if Trades ==3:
                                        countUp = cummulative()
                                        Reaarange_thread = threading.Thread(target= Reaarange)
                                        Reaarange_thread .start()
                                        Trades = 0
                                        with open("counters/noTrade.json", 'w') as json_file:
                                            json.dump(Trades, json_file)
                                    else:
                                        Trades += 1
                                        with open("counters/noTrade.json", 'w') as json_file:
                                            json.dump(Trades, json_file)
                                        


                                # no trade counter 
                                # restart trade 
                        

                            else:
                                P_Status = Positive_Signal()
                                if Trades ==3:
                                    countUp = cummulative()
                                    Reaarange_thread = threading.Thread(target= Reaarange)
                                    Reaarange_thread .start()
                                    Trades = 0
                                    with open("counters/noTrade.json", 'w') as json_file:
                                        json.dump(Trades, json_file)
                                else:
                                    Trades += 1
                                    with open("counters/noTrade.json", 'w') as json_file:
                                        json.dump(Trades, json_file)
                                    


                            #error fix function and start again 
                        else:

                            with open("counters/error.json",'r') as json_file:
                                error  = json.load(json_file)
                            error += 1
                            print(error,":\033[91m error occurance(s)\033[0m")
                    
                            with open("counters/error.json", 'w') as json_file:
                                json.dump(error, json_file)
                            resolve = fix()

                else:
                    with open("counters/error.json",'r') as json_file:
                        error  = json.load(json_file)
                    error += 1
                    print(error,":\033[91m error occurance(s)\033[0m")

                    with open("counters/error.json", 'w') as json_file:
                        json.dump(error, json_file)


                    resolve = fix()

                    #error fix function and start again 
            except Exception as e:
                print(f"an Exception errror has occured on main execution {e}")









        Tax_thread = threading.Thread(target =  Tax_value)
        Tax_thread.start()

        Tax_thread.join()

        FinalassetCal_thread = threading.Thread(target =  Finalcal_asset)
        FinalassetCal_thread.start()

        FinalassetCal_thread.join()
        
          
        All_assetTo_USDT_thread2 = threading.Thread(target= get_back)
        All_assetTo_USDT_thread2.start()

        All_assetTo_USDT_thread2.join()

        Placements = Final_Replacements()

        Time = curr_time()
        print(" \033[93m a complete trade session has been completed resting all proccesse for 5min\033[0m ")
        
                 
        #alarm_thread = threading.Thread(target = play_alarm_sound)
        #alarm_thread.start()

                
        time.sleep(300)
        resolve = fix()

                  #error fix function and start again 

                    

                    

                

          
        
        
                  




if __name__ == "__main__":
    Main_Execution()

   







#threading process start 





