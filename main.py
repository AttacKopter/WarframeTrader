import requests
import json

import pandas as pd

debug = True
def get_item_orders(item_url):
    request_url = url + "/" + item_url + "/orders"
    response = requests.get(request_url)
    orders =  pd.json_normalize(response.json()['payload']['orders'])[['platinum','quantity','order_type','user.status']]
    online_mask = (orders['user.status'] != 'offline')

    buy_orders_mask = (orders['order_type'] == 'buy')
    buy_orders = orders.loc[online_mask].loc[buy_orders_mask].sort_values(by='platinum')[['platinum','quantity']]
    buy_count = buy_orders['quantity'].sum()
    buy_mean = buy_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/buy_count
    buy_sd = pow(buy_orders.apply(lambda x: pow(x.platinum*x.quantity - buy_mean,2),axis = 1).sum()/buy_count,0.5)
    buy_outlier_mask = ((buy_orders['platinum'] > buy_mean - buy_sd * 3) & (buy_orders['platinum'] < buy_mean + buy_sd *3))
    buy_orders = buy_orders.loc[buy_orders_mask]

    sell_orders_mask = (orders['order_type'] == 'sell')
    sell_orders = orders.loc[online_mask].loc[sell_orders_mask].sort_values(by='platinum')[['platinum','quantity']]
    sell_count = sell_orders['quantity'].sum()
    sell_mean = sell_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/sell_count
    sell_sd = pow(sell_orders.apply(lambda x: pow(x.platinum*x.quantity - sell_mean,2),axis = 1).sum()/sell_count,0.5)
    sell_outlier_mask = ((sell_orders['platinum'] > sell_mean - sell_sd * 3) & (sell_orders['platinum'] < sell_mean + sell_sd *3))
    sell_orders = sell_orders.loc[sell_orders_mask]
    if debug:
        print("buy orders\n",buy_orders)
        print("buy mean",  buy_mean)
        print("buy count",buy_count)
        print("buy sd",buy_sd)

        print("sell orders\n",sell_orders)
        print("sell mean",sell_mean)
        print("sell count",sell_count)
        print("sell sd",sell_sd)

    # Remove Outliers

url = "https://api.warframe.market/v1/items"
response = requests.get(url)

tradable_items = pd.json_normalize(response.json()['payload']['items'])

item_urls = tradable_items['url_name']

orders = []
get_item_orders( item_urls[0])#.apply(get_item_orders)

