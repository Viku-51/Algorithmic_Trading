#!/usr/bin/env python





from smartapi import SmartConnect
apikey = 'api_key' # Intentially hidden
username = 'username'
pwd = 'password'

obj=SmartConnect(api_key=apikey)
data = obj.generateSession(username,pwd)
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
userProfile= obj.getProfile(refreshToken)
userProfile





obj.tradeBook()


# In[ ]:Object returns Tradebook 


obj.orderBook()


# In[ ]:Object returns orderbook


obj.position()


# In[ ]:The current position is returned


obj.holding()


# In[ ]:Holding is displayed


obj.ltpData('NFO','NIFTY24JUN21FUT','48508') #Nifty futures expiry on JUN21


# In[ ]:LTP and orther details are displayed


import json
import pandas as pd
from datetime import datetime
def historicaldata ():
        try:
            historicParam={
            "exchange": "NSE",
            "symboltoken": "3045",
            "interval": "FIFTEEN_MINUTE",
            "fromdate": "2021-05-11 09:15", 
            "todate": "2021-05-12 10:30"
            }
            
            return obj.getCandleData(historicParam)
        except Exception as e:
            print("Historic Api failed: {}".format(e.message))


# In[ ]:


res_json = historicaldata()
columns = ['timestamp','O','H','L','C','V']
df = pd.DataFrame(res_json['data'], columns=columns)
df['timestamp'] = pd.to_datetime(df['timestamp'],format = '%Y-%m-%dT%H:%M:%S')
df


# In[ ]:




