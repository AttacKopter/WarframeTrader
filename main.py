import requests
import json

import pandas as pd

def get_item_orders(item_url):
    request_url = url + "/" + item_url + "/orders"
    response = requests.get(request_url)
    orders =  pd.json_normalize(response.json()['payload']['orders'])
    online_mask = (orders['user.status'] != 'offline')
    print(orders[online_mask].head())
    return
    for response in responses:
        if response['visible'] == 'False':
            continue
        elif response['order_type'] == 'buy':
            buy_orders.append(response)
        elif response['order_type'] == 'sell':
            sell_orders.append(response)

    buy_orders = sorted(buy_orders, key=lambda d: d['platinum'])
    sell_orders = sorted(sell_orders, key=lambda d: d['platinum'])

    buy_mean = 0;
    sell_mean = 0;

    for buy_order in buy_orders:
        buy_mean = buy_mean + buy_order['platinum']
    for sell_order in sell_orders:
        sell_mean = sell_mean + sell_order['platinum']

    buy_mean = buy_mean/len(buy_orders)
    sell_mean = sell_mean/len(sell_orders)

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

orders =[]
item_urls.head().apply(get_item_orders)

