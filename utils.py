import robin_stocks
from datetime import datetime


def calculate_percentage_change(initial_value, final_value):
    """
    Calculate the percentage change between two values.
    """
    return ((final_value - initial_value) / initial_value) * 100


def is_option_expired(expiration_date):
    """
    Check if an option has expired based on its expiration date.
    """
    today = datetime.date.today()
    expiration = datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
    return expiration < today


def validate_option_data(option_data):
    """
    Validate the option data retrieved from the Robinhood API or user input.
    Perform necessary checks to ensure the data is valid and complete.
    """
    required_fields = ['buy_price', 'sell_price', 'strike_price', 'expiration_date', 'premium_collected']
    for field in required_fields:
        if field not in option_data:
            raise ValueError(f"Missing required field: {field}")

    # Validate data types and ranges as needed

    # Return True if all checks pass
    return True


def calculate_net_gain(stock_price_gain, call_option_gain, sold_option_loss):
    """
    Calculate the net gain from stock price movement and option gains/losses.
    """
    return stock_price_gain + call_option_gain - sold_option_loss


def is_net_gain_reached(net_gain, take_profit_point, average_cost_per_share, premium_collected):
    """
    Check if the net gain reaches the specified take profit point.
    """
    target_gain = take_profit_point / 100 * (average_cost_per_share + premium_collected)
    return net_gain >= target_gain


def validate_stock_data(stock_data):
    """
    Validate the stock data retrieved from the Robinhood API or user input.
    Perform necessary checks to ensure the data is valid and complete.
    """
    required_fields = ['symbol', 'last_trade_price', 'premium_collected']
    for field in required_fields:
        if field not in stock_data:
            raise ValueError(f"Missing required field: {field}")

    # Validate data types and ranges as needed

    # Return True if all checks pass
    return True



class YourDataSource:
    def get_stock_price(symbol):
        stock_data = robin_stocks.stocks.get_latest_price(symbol)
        return float(stock_data[0])

    def get_option_market_data(symbol, expiration_date, option_type, strike):
        option_data = robin_stocks.options.get_option_market_data(symbol, expirationDate=expiration_date,
                                                                  optionType=option_type, strike=strike)
        return float(option_data[0]['adjusted_mark_price'])
