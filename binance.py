from binance.client import Client
from binance.enums import *
import logging

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):  # ✅ Correct
        self.logger = self.setup_logger()
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.API_URL = 'https://testnet.binance.vision/api'  # Spot testnet

    def setup_logger(self):
        logger = logging.getLogger('BasicBotLogger')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('bot_log.txt')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def place_market_order(self, symbol, side, quantity):
        try:
            order = self.client.order_market(
                symbol=symbol,
                side=side,
                quantity=quantity
            )
            self.logger.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing market order: {e}")
            return None

    def place_stop_order(self, symbol, side, quantity, stop_price):
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_STOP_LOSS,
                quantity=quantity,
                stopPrice=stop_price,
                timeInForce=TIME_IN_FORCE_GTC
            )
            self.logger.info(f"Stop order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing stop order: {e}")
            return None

    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        try:
            order = self.client.create_oco_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                stopLimitPrice=stop_limit_price,
                stopLimitTimeInForce=TIME_IN_FORCE_GTC
            )
            self.logger.info(f"OCO order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing OCO order: {e}")
            return None

    def get_account_info(self):
        try:
            info = self.client.get_account()
            self.logger.info("Fetched account info.")
            return info
        except Exception as e:
            self.logger.error(f"Error fetching account info: {e}")
            return None
if __name__ == "__main__":
    api_key = input("Enter your API Key: ")
    api_secret = input("Enter your Secret Key: ")

    bot = BasicBot(api_key, api_secret, testnet=True)

    while True:
        print("\nWhat would you like to do?")
        print("1. Place Market Order")
        print("2. Place Stop Order")
        print("3. Place OCO Order")
        print("4. View Account Info")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Buy or Sell? ").upper()
            qty = float(input("Quantity: "))
            bot.place_market_order(symbol, side, qty)

        elif choice == '2':
            symbol = input("Enter symbol: ").upper()
            side = input("Buy or Sell? ").upper()
            qty = float(input("Quantity: "))
            stop_price = input("Stop Price: ")
            bot.place_stop_order(symbol, side, qty, stop_price)

        elif choice == '3':
            symbol = input("Enter symbol: ").upper()
            side = input("Buy or Sell? ").upper()
            qty = float(input("Quantity: "))
            price = input("Take profit price: ")
            stop_price = input("Stop trigger price: ")
            stop_limit = input("Stop limit price: ")
            bot.place_oco_order(symbol, side, qty, price, stop_price, stop_limit)

        elif choice == '4':
            info = bot.get_account_info()
            print(info)

        elif choice == '5':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")