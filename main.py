import requests
import json
import os
import pandas as pd
from pandarallel import pandarallel

debug = False
global errors,success
errors = {}
success = 0
def get_item_orders(item_url):
    global success,errors
    url = 'https://api.warframe.market/v1/items'
    try:
        request_url = url + '/' + item_url + '/orders'
        response = requests.get(request_url)
        orders =  pd.json_normalize(response.json()['payload']['orders']).assign(name=item_url)
        errors.pop(item_url,None)
        success += 1
<<<<<<< HEAD
        print(success)
=======
        print(success,)
>>>>>>> 79c337d (Made it make data well)
        return orders
    except:
        try:
            errors[item_url] += 1
        except:
            errors[item_url] = 1
        print(success,end=' ')
        print(errors)
        return get_item_orders(item_url)

def handle_data(orders):
    buy_orders_mask = (orders['order_type'] == 'buy') & (orders['quantity'] < 69) # real filter
    buy_orders = orders.loc[buy_orders_mask].sort_values(by='platinum',ascending=False)[['platinum','quantity','creation_date']]
    buy_count = buy_orders['quantity'].sum()
    if buy_count == 0:
        return {}
    buy_mean = buy_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/buy_count
    buy_sd = pow(buy_orders.apply(lambda x: pow(x.platinum*x.quantity - buy_mean,2),axis = 1).sum()/buy_count,0.5)
    buy_outlier_mask = ((buy_orders['platinum'] > buy_mean - buy_sd * 3) & (buy_orders['platinum'] < buy_mean + buy_sd *3))
    #Recompute after scrubbing outliers
    buy_orders = buy_orders.loc[buy_orders_mask]
    buy_count = buy_orders['quantity'].sum()
    buy_mean = buy_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/buy_count
    buy_sd = pow(buy_orders.apply(lambda x: pow(x.platinum*x.quantity - buy_mean,2),axis = 1).sum()/buy_count,0.5)
    if debug:
        print('buy mean',  buy_mean)
        print('buy count',buy_count)
        print('buy sd',buy_sd)

    sell_orders_mask = (orders['order_type'] == 'sell') & (orders['quantity'] < 69) #Real filter
    sell_orders = orders.loc[sell_orders_mask].sort_values(by='platinum')[['platinum','quantity','creation_date']]
    sell_count = sell_orders['quantity'].sum()
    if sell_count == 0:
        return {}
    sell_mean = sell_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/sell_count
    sell_sd = pow(sell_orders.apply(lambda x: pow(x.platinum*x.quantity - sell_mean,2),axis = 1).sum()/sell_count,0.5)
    sell_outlier_mask = ((sell_orders['platinum'] > sell_mean - sell_sd * 3) & (sell_orders['platinum'] < sell_mean + sell_sd *3))
    #Recompute after scrubbing outliers
    sell_orders = sell_orders.loc[sell_orders_mask]
    sell_count = sell_orders['quantity'].sum()
    sell_mean = sell_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/sell_count
    sell_sd = pow(sell_orders.apply(lambda x: pow(x.platinum*x.quantity - sell_mean,2),axis = 1).sum()/sell_count,0.5)
    if debug:
        print('sell mean',sell_mean)
        print('sell count',sell_count)
        print('sell sd',sell_sd)
    #Compute split
    split = sell_orders['platinum'].iloc[0]  - buy_orders['platinum'].iloc[0]
    if debug:
        print('sell - buy',split)
    return_values =  {'buy mean':buy_mean,'buy count':buy_count,'sell mean':sell_mean,'sell count':sell_count,'split':split,'name':item_url}
    return return_values

data_path = 'data.csv'
item_path = 'items.csv'

url = 'https://api.warframe.market/v1/items'
response = requests.get(url)
tradable_items = None
if os.path.exists(item_path):
    print('using saved items')
    tradable_items = pd.read_csv(item_path)
else:
    print('no item csv')
    tradable_items = pd.json_normalize(response.json()['payload']['items'])
    tradable_items.to_csv(item_path,index=False)

if os.path.exists(data_path):
    print('using saved data')
    data = pd.read_csv('data.csv')
else:
    print('no data csv')
    item_urls = tradable_items['url_name']
    orders = []
    pandarallel.initialize()
    raw_data = item_urls.head.parallel_apply(get_item_orders)
    data = pd.concat(list(raw_data))
    data.to_csv(data_path,index=False)
