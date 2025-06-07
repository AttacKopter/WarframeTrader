import requests
import json

import pandas as pd

debug = False
def get_item_orders(item_url):
    request_url = url + '/' + item_url + '/orders'
    response = requests.get(request_url)
    orders =  pd.json_normalize(response.json()['payload']['orders'])[['platinum','quantity','order_type','user.status']]
    online_mask = (orders['user.status'] != 'offline')

    buy_orders_mask = (orders['order_type'] == 'buy') & (orders['quantity'] < 69) # real filter
    buy_orders = orders.loc[online_mask].loc[buy_orders_mask].sort_values(by='platinum',ascending=False)[['platinum','quantity']]
    buy_count = buy_orders['quantity'].sum()
    if buy_count == 0:
        return {}
        return {'buy mean':-1,'buy count':-1,'sell mean':-1,'sell count':-1,'split':-1,'name':item_url}
    buy_mean = buy_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/buy_count
    buy_sd = pow(buy_orders.apply(lambda x: pow(x.platinum*x.quantity - buy_mean,2),axis = 1).sum()/buy_count,0.5)
    buy_outlier_mask = ((buy_orders['platinum'] > buy_mean - buy_sd * 3) & (buy_orders['platinum'] < buy_mean + buy_sd *3))
    # Recompute after scrubbing outliers
    buy_orders = buy_orders.loc[buy_orders_mask]
    buy_count = buy_orders['quantity'].sum()
    buy_mean = buy_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/buy_count
    buy_sd = pow(buy_orders.apply(lambda x: pow(x.platinum*x.quantity - buy_mean,2),axis = 1).sum()/buy_count,0.5)
    if debug:
        print('buy mean',  buy_mean)
        print('buy count',buy_count)
        print('buy sd',buy_sd)

    sell_orders_mask = (orders['order_type'] == 'sell') & (orders['quantity'] < 69) # real filter
    sell_orders = orders.loc[online_mask].loc[sell_orders_mask].sort_values(by='platinum')[['platinum','quantity']]
    sell_count = sell_orders['quantity'].sum()
    if sell_count == 0:
        return {'buy mean':-1,'buy count':-1,'sell mean':-1,'sell count':-1,'split':-1,'name':item_url}
    sell_mean = sell_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/sell_count
    sell_sd = pow(sell_orders.apply(lambda x: pow(x.platinum*x.quantity - sell_mean,2),axis = 1).sum()/sell_count,0.5)
    sell_outlier_mask = ((sell_orders['platinum'] > sell_mean - sell_sd * 3) & (sell_orders['platinum'] < sell_mean + sell_sd *3))
    # Recompute after scrubbing outliers
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
    return {'buy mean':buy_mean,'buy count':buy_count,'sell mean':sell_mean,'sell count':sell_count,'split':split,'name':item_url}


url = 'https://api.warframe.market/v1/items'
response = requests.get(url)

tradable_items = pd.json_normalize(response.json()['payload']['items'])

item_urls = tradable_items['url_name']

orders = []
data = pd.DataFrame(list(item_urls.iloc[5:10].apply(get_item_orders))).dropna()
print(data)

