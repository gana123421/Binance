from binance.client import Client
from binance.enums import *

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.API_URL = 'https://testnet.binance.vision/api'  # Spot testnet

    def place_market_order(self, symbol, side, quantity):
        return self.client.order_market(symbol=symbol, side=side, quantity=quantity)

    def place_stop_order(self, symbol, side, quantity, stop_price):
        return self.client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_STOP_LOSS,
            quantity=quantity,
            stopPrice=stop_price,
            timeInForce=TIME_IN_FORCE_GTC
        )

    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        return self.client.create_oco_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            stopPrice=stop_price,
            stopLimitPrice=stop_limit_price,
            stopLimitTimeInForce=TIME_IN_FORCE_GTC
        )

    def get_account_info(self):
        return self.client.get_account()
