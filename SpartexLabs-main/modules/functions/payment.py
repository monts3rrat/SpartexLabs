import requests
import os
import asyncio

api_key = os.getenv('XCCAPI')


async def create_invoice(amount):
    url = "https://api.commerce.coinbase.com/charges"

    headers = {
        "Content-Type": "application/json",
        "X-CC-Api-Key": api_key,
        'X-CC-Version': '2018-03-22',
    }

    data = {
        "name": "Pay for SpartexLabs Bot",
        "description": "Pay for SpartexLabs Bot",
        "pricing_type": "fixed_price",
        "local_price": {
            "amount": amount,
            "currency": "USD"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return [response.json()['data']['hosted_url'], response.json()['data']['code']]


async def get_status(code):
    headers = {
        "Content-Type": "application/json",
        "X-CC-Api-Key": api_key,
        'X-CC-Version': '2018-03-22',
    }

    response = requests.get(f'https://api.commerce.coinbase.com/charges/{code}', headers=headers).json()
    try:
        return response['data']['payments'][0]['status']
    except IndexError:
        return 0
    except KeyError:
        return 1
