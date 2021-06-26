#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import warnings
warnings.filterwarnings('ignore')


# In[ ]:


apikey = '838PSWV'
username = 'N788686'
pwd = 'jhjhjh87'


# In[ ]:


from smartapi import SmartConnect
import time
import requests
import pandas as pd
from datetime import datetime,date
import math

obj=SmartConnect(api_key=apikey)
data = obj.generateSession(username,pwd)
data
#refreshToken= data['data']['refreshToken']
#feedToken=obj.getfeedToken()
#userProfile= obj.getProfile(refreshToken)
#userProfile


# In[ ]:


obj.position()


# In[ ]:


obj.ltpData('NFO','BANKNIFTY24JUN21FUT','48506')


# In[ ]:


def place_order(token,symbol,qty,buy_sell,ordertype,price,variety= 'NORMAL',exch_seg='NSE',triggerprice=0):
    try:
        orderparams = {
            "variety": variety,
            "tradingsymbol": symbol,
            "symboltoken": token,
            "transactiontype": buy_sell,
            "exchange": exch_seg,
            "ordertype": ordertype,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "squareoff": "0",
            "stoploss": "0",
            "quantity": qty,
            "triggerprice":triggerprice
            }
        print(orderparams)
        orderId=obj.placeOrder(orderparams)
        print("The order id is: {}".format(orderId))
    except Exception as e:
        print("Order placement failed: {}".format(e.message))


# In[ ]:


url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
token_df = token_df.astype({'strike': float})
#token_df = token_df[(token_df['name'] == 'BANKNIFTY') & (token_df['instrumenttype'] == 'OPTIDX') & (token_df['expiry']==date(2021,6,10)) ]
token_df


# In[ ]:


def getTokenInfo (symbol, exch_seg ='NSE',instrumenttype='OPTIDX',strike_price = '',pe_ce = 'CE',expiry_day = None):
    df = token_df
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['expiry']==expiry_day) &  (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])


# In[ ]:


expiry_day = date(2021,6,10)

symbol = 'BANKNIFTY'

spot_token = getTokenInfo(symbol).iloc[0]['token']
ltpInfo = obj.ltpData('NSE',symbol,spot_token)
indexLtp = ltpInfo['data']['ltp']
indexLtp


# In[ ]:


ATMStrike = math.ceil(indexLtp/100)*100
ATMStrike


# In[ ]:


ce_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',ATMStrike,'CE',expiry_day).iloc[0]
ce_strike_symbol


# In[ ]:


pe_strike_symbol = getTokenInfo(symbol,'NFO','OPTIDX',ATMStrike,'PE',expiry_day).iloc[0]
pe_strike_symbol


# In[ ]:


place_order(ce_strike_symbol['token'],ce_strike_symbol['symbol'],ce_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')


# In[ ]:


place_order(pe_strike_symbol['token'],pe_strike_symbol['symbol'],pe_strike_symbol['lotsize'],'SELL','MARKET',0,'NORMAL','NFO')


# # STEP 1: Get LTP of SPOT . Help of ltpData() method
# 

# # STEP 2: Calculate ATM Strike help of SPOT
# 

# # STEP 3: Get token,symbol  of CE Strike 
# 

# # STEP 4: Get Token , symbol for PE Strike 
# 

# # STEP 5: place SELL order for CE , PE
# 
