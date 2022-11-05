import json
import requests
import os

# 9984618 15 min

# 9974970 4h

def send_signal(pair, botId):
    url = "https://app.3commas.io/trade_signal/trading_view"
    email_token = os.getenv('3COMMAS_EMAIL_TOKEN')

    headers = {'Content-Type': 'application/json'}

    payload = json.dumps({
        "message_type": "bot",
        "bot_id": botId,
        "email_token": email_token,
        "delay_seconds": 0,
        "pair": pair
    })

    response = requests.request("POST", url, headers=headers, data=payload)
