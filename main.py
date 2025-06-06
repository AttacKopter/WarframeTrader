import requests
import json

url = "https://api.warframe.market/v1/items"
response = requests.get(url)

tradable_items = response.json()

item_urls = []

for item in tradable_items['payload']['items']:
    item_urls.append(item['url_name'])
    break

buy_orders = []
sell_orders = []

for item_url in item_urls:
    request_url = url + "/" + item_url + "/orders"
    responses = requests.get(request_url).json()['payload']['orders']
    for response in responses:
        if response['visible'] == 'False':
            continue
        elif response['order_type'] == 'buy':
            buy_orders.append(response)
        elif response['order_type'] == 'sell':
            sell_orders.append(response)

    print("SELL ORDERS:")
    for sell_order in sell_orders:
        print(sell_order['platinum'])
