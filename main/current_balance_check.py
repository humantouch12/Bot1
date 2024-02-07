import json
import os
import websocket
import hmac
import hashlib
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime



def Current_Account_Details():
    # keys 
    api_key = "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe"
    secret_key = "l2ryxyHlrZep2kcuitbC4L3ngUeIuLcmCH16ztZ57GOs0fdixMCkeGzb2BGrK7dq"
    # url 
    url = "wss://testnet.binance.vision/ws-api/v3"  # Replace with the actual WebSocket endpoint

    #time 
    


    try: 
        ws = websocket.create_connection(url)
        with open("current/time.json", 'r') as json_file:
         Time = json.load(json_file)
    # sorting to variables 
        seconds = Time / 1000
        time_object = datetime.utcfromtimestamp(seconds)
        period = time_object.strftime('%H:%M:%S')

    # parameters 

        params = {
                'apiKey':f'{api_key}',
                'timestamp': f'{Time}',
                'recvWindow': '2000'
            }
    # payloads for signature creating 
        payload = '&'.join([f'{param}={params[param]}' for param in sorted(params)])

# Interpret secretKey as ASCII data and use it as a key for HMAC-SHA-256
        secret_key_bytes = secret_key.encode('ascii')
        signature = hmac.new(secret_key_bytes, msg=payload.encode('ascii'), digestmod=hashlib.sha256).hexdigest()
        # id 
        with open("current/id.json", 'r') as json_file:
            id_value= json.load(json_file)
    #account payload
        Details_payload = {
                        "id": id_value,
                        "method": "account.status",
                        "params": {
                                    "apiKey": "26nEQ5kY280Djh0AW78fWM6EPgKd8rw0vP7OqgJKbycJ8oJrBLGIRn9XyfZtpTVe",
                                    "signature": signature,
                                    "timestamp": Time,
                                    "recvWindow":2000,
                                    }
                                    }
    #websocket
    

        ws.send(json.dumps( Details_payload ))
        response = ws.recv()
        account_data = json.loads(response)
# STORING inside response file 
        current_folder = os.path.abspath("current")
        file_paths = [os.path.join(current_folder, "currentBalanceresponse.json")]

        # data set   
        data_sets = [account_data]                 
        for file_path, data_set in zip(file_paths, data_sets):
               
            try:
                      # Check if the file is not empty before loading
                    if os.path.getsize(file_path) > 0:
                        with open(file_path, 'r') as json_file:
                            existing_data = json.load(json_file)
                    else:
                        existing_data = []
            except FileNotFoundError:
                existing_data = []

            # Add the new response data to the existing data
            existing_data.append(data_set)

            # Write the combined data back to the JSON file
            with open(file_path, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)


        if 'status' in account_data  and account_data ['status'] == 200:
            check = {"status":200}
            status_check = [check]
            with open("current/currentBalanceStatus.json" ,'w') as json_file:
                json.dump(status_check, json_file, indent=4)
           
            assets_to_extract = ["USDT", "BTC", "BNB", "SOL", "ETH", "DOGE","XRP", "LTC", "TRX"]
            extracted_balances = {}

# Loop through the provided balance data
            for asset_data in account_data.get("result", {}).get("balances", []):
                asset_symbol = asset_data.get("asset")
                if asset_symbol in assets_to_extract:
                    extracted_balances[asset_symbol] = {
            "free": float(asset_data.get("free", 0)),
            "locked": float(asset_data.get("locked", 0))
                                                            }

            with open("current/current_balance.json" ,'w') as json_file:
                json.dump(extracted_balances, json_file, indent=4)

            balance = extracted_balances

            
              
            # code to awaite pong message    # saving response to file 
            try:
                with open('current/mainDisplay.json', 'r') as json_file:
                    existing_data = json_file.read().splitlines()
            except FileNotFoundError:
                existing_data = []

# Add the new data string to the existing data
            existing_data.append( f"[{period}] : current account balance has been checked successfully \n [{balance}]")

# Save the updated data back to the JSON file with a newline after each entry
            with open('current/mainDisplay.json', 'w') as json_file:
                json_file.write('\n'.join(existing_data))
                json_file.write('\n')  # Add a newline after the last entry
            # code to awaite pong message 
            

        else:
            check = {"status":400}
            status_check = [check]
            with open("current/currentBalanceStatus.json" ,'w') as json_file:
                json.dump(status_check, json_file, indent=4)
                         
            # code to awaite pong message    # saving response to file 
            try:
                with open('current/mainDisplay.json', 'r') as json_file:
                        existing_data = json_file.read().splitlines()
            except FileNotFoundError:
                    existing_data = []

# Add the new data string to the existing data
            existing_data.append( f"[{period}] :An error has occured in checking current account balance  ")

# Save the updated data back to the JSON file with a newline after each entry
            with open('current/mainDisplay.json', 'w') as json_file:
                json_file.write('\n'.join(existing_data))
                json_file.write('\n')  # Add a newline after the last entry
            
    except Exception as e:
        check = {"status":400}
        status_check = [check]
        with open("current/currentBalanceStatus.json" ,'w') as json_file:
            json.dump(status_check, json_file, indent=4)
            # error exception saved  
        errorException = {"error from":"current Balance","status":904,"description": str(e)}
        error = [errorException]
        with open("current/exceptionErrors.json" ,'w') as json_file:
                json.dump(error, json_file, indent=4)

    
    finally:
         ws.close()

           

if __name__ == "__main__":

# Example usage
    Current_Account_Details()


# Print or use the result
