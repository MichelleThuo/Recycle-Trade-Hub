import requests, json
headers = {"Content-Type": "application/json"}
callbackurl='http://127.0.0.1:8000/mpesa/callback/'
payload ={    
    "Body": {        
       "stkCallback": {            
          "MerchantRequestID": "6e86-45dd-91ac-fd5d4178ab52861416",            
          "CheckoutRequestID": "ws_CO_12032024173304297758095711",            
          "ResultCode": 0,            
          "ResultDesc": "The service request is processed successfully.",            
          "CallbackMetadata": {                
             "Item": [{                        
                "Name": "Amount",                        
                "Value": 1.00                    
             },                    
             {                        
                "Name": "MpesaReceiptNumber",                        
                "Value": "NLJ7RT61SV"                    
             },                    
             {                        
                "Name": "TransactionDate",                        
                "Value": 20240312102115                    
             },                    
             {                        
                "Name": "PhoneNumber",                        
                "Value": 254708374149                    
             }]            
          }        
       }    
    }
 }

response = requests.post(callbackurl, headers = headers, json = payload)
print(response)