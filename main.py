import requests
import json

import pandas as pd

def get_item_orders(item_url):
    request_url = url + "/" + item_url + "/orders"
    response = requests.get(request_url)
    orders =  pd.json_normalize(response.json()['payload']['orders'])[['platinum','quantity','order_type','user.status']]
    online_mask = (orders['user.status'] != 'offline')
    buy_orders_mask = (orders['order_type'] == 'buy')
    sell_orders_mask = (orders['order_type'] == 'sell')
    sell_orders = orders[online_mask][sell_orders_mask].sort_values(by='platinum')[['platinum','quantity']]
    buy_orders = orders[online_mask][buy_orders_mask].sort_values(by='platinum')[['platinum','quantity']]

    print(sell_orders)

    buy_count = buy_orders['quantity'].sum()
    buy_mean = buy_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/buy_count
    sell_count = sell_orders['quantity'].sum()
    sell_mean = sell_orders.apply(lambda x: x.platinum*x.quantity, axis=1).sum()/sell_count

    print(sell_mean)
    print(buy_mean)
    print(sell_count)
    print(buy_count)

    return

    # Remove Outliers

    buy_outlier_condition = lambda x: x['platinum'] < buy_mean
    sell_outlier_condition = lambda x: x['platinum'] > sell_mean

    buy_orders = [x for x in buy_orders if not buy_outlier_condition(x)]
    sell_orders = [x for x in sell_orders if not sell_outlier_condition(x)]

    buy_volume = len(buy_orders)
    sell_volume = len(sell_orders)

    print("SELL ORDERS:")
    for sell_order in sell_orders:
        print(sell_order)

    print(buy_mean)
    print(sell_mean)
    print(buy_volume)
    print(sell_volume)
    print(item_url)

url = "https://api.warframe.market/v1/items"
response = requests.get(url)

tradable_items = pd.json_normalize(response.json()['payload']['items'])

item_urls = tradable_items['url_name']

orders = []
get_item_orders( item_urls[0])#.apply(get_item_orders)

