from flask import Flask, render_template, request
from bot import BasicBot

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    result = None

    if request.method == 'POST':
        api_key = request.form['api_key']
        api_secret = request.form['api_secret']
        action = request.form['action']
        symbol = request.form['symbol']
        side = request.form['side']
        quantity = float(request.form['quantity'])

        bot = BasicBot(api_key, api_secret, testnet=True)

        try:
            if action == 'market':
                result = bot.place_market_order(symbol, side, quantity)
            elif action == 'stop':
                stop_price = request.form['stop_price']
                result = bot.place_stop_order(symbol, side, quantity, stop_price)
            elif action == 'oco':
                price = request.form['price']
                stop_price = request.form['stop_price']
                stop_limit_price = request.form['stop_limit_price']
                result = bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
            elif action == 'info':
                result = bot.get_account_info()
        except Exception as e:
            message = str(e)

    return render_template('index.html', result=result, message=message)

if __name__ == '__main__':
    app.run(debug=True)
