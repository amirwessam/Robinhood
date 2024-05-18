import robin_stocks
import robin_stocks.options as options
from datetime import datetime, timedelta
from utils import validate_stock_data, calculate_net_gain


class OptionsTradingBot:
    def __init__(self, bought_option, sold_option, account_info, trading_params, data_source):
        self.bought_option = bought_option
        self.sold_option = sold_option
        self.account_info = account_info
        self.trading_params = trading_params
        self.data_source = data_source

    def execute_trading_strategy(self):
        bought_option_buy_price = self.bought_option['buy_price']
        sold_option_sell_price = self.sold_option['sell_price']
        bought_option_strike = self.bought_option['strike_price']
        sold_option_strike = self.sold_option['strike_price']
        expiration_date = self.bought_option['expiration_date']

        # Helper function to check if the spread has reached the target
        def is_spread_up_10_percent(bought_option_buy_price, sold_option_sell_price):
            spread = sold_option_sell_price - bought_option_buy_price
            return spread >= (0.1 * bought_option_buy_price)

        # Helper function to check if the cumulative return is 5%
        def is_cumulative_return_5_percent(put_option_price, sold_option_sell_price, bought_option_buy_price):
            cumulative_return = (put_option_price + (
                        bought_option_buy_price - sold_option_sell_price)) / bought_option_buy_price
            return cumulative_return >= 0.05

        # Get current stock price
        current_stock_price = self.data_source.get_stock_price(self.bought_option['symbol'])

        # Condition 1: Buy a Put if bought option price drops below 80% of the premium collected
        if bought_option_buy_price < 0.8 * sold_option_sell_price:
            # Buy a Put at the higher strike price
            put_option_strike = max(bought_option_strike, sold_option_strike)
            put_option_expiration = expiration_date
            options.order_buy_option_limit(self.bought_option['symbol'], put_option_strike, put_option_expiration,
                                           'put', 1)

            # Check if the conditions to close the Put position are met
            while True:
                # Get current back call option price
                back_call_option_price = float(
                    options.get_option_market_data(self.bought_option['symbol'], expirationDate=expiration_date,
                                                   optionType='call', strike=sold_option_strike)[0][
                        'adjusted_mark_price'])

                # Check if the back call option price has increased by 5% from the trigger point
                if back_call_option_price >= 1.05 * bought_option_buy_price:
                    # Close the Put position
                    options.order_sell_option_limit(self.bought_option['symbol'], put_option_strike,
                                                    put_option_expiration, 'put', 1)
                    break

                # Check if the cumulative return is 5%
                put_option_price = float(
                    options.get_option_market_data(self.bought_option['symbol'], expirationDate=expiration_date,
                                                   optionType='put', strike=put_option_strike)[0][
                        'adjusted_mark_price'])
                if is_cumulative_return_5_percent(put_option_price, sold_option_sell_price, bought_option_buy_price):
                    # Close the Put position
                    options.order_sell_option_limit(self.bought_option['symbol'], put_option_strike,
                                                    put_option_expiration, 'put', 1)
                    break

        # Condition 2: Buy a Call if front option starts trading at intrinsic value
        if bought_option_strike + bought_option_buy_price == 0.8 * current_stock_price:
            # Buy a Call at the front option's expiration
            call_option_strike = bought_option_strike
            call_option_expiration = expiration_date
            options.order_buy_option_limit(self.bought_option['symbol'], call_option_strike, call_option_expiration,
                                           'call', 1)

            # Check if the condition to sell the additional Call is met
            while True:
                # Get current front sold option price
                front_sold_option_price = float(
                    options.get_option_market_data(self.bought_option['symbol'], expirationDate=expiration_date,
                                                   optionType='call', strike=sold_option_strike)[0][
                        'adjusted_mark_price'])

                # Check if the front sold option price trades at a profitable level
                if front_sold_option_price >= sold_option_sell_price:
                    # Sell the additional Call
                    options.order_sell_option_limit(self.bought_option['symbol'], sold_option_strike, expiration_date,
                                                    'call', 1)
                    break

        # Check if the spread is up 10% from the initial buy point
        if is_spread_up_10_percent(bought_option_buy_price, sold_option_sell_price):
            # Close the trade
            options.order_sell_option_limit(self.bought_option['symbol'], bought_option_strike, expiration_date, 'put',
                                            1)
            options.order_sell_option_limit(self.bought_option['symbol'], sold_option_strike, expiration_date, 'call',
                                            1)

        # Check if the front option crossed into trading at intrinsic value and the spread is profitable
        if bought_option_strike + bought_option_buy_price == 0.8 * current_stock_price and sold_option_sell_price > bought_option_buy_price:
            # Close the trade
            options.order_sell_option_limit(self.bought_option['symbol'], bought_option_strike, expiration_date, 'put',
                                            1)
            options.order_sell_option_limit(self.bought_option['symbol'], sold_option_strike, expiration_date, 'call',
                                            1)

        # Check if the option expiration date is approaching
        if datetime.strptime(expiration_date, "%Y-%m-%d") - datetime.now() <= timedelta(weeks=1):
            # Close the short option
            options.order_sell_option_limit(self.bought_option['symbol'], sold_option_strike, expiration_date, 'call',
                                            1)

            # Open an identical position one week closer in expiration
            new_expiration_date = (datetime.strptime(expiration_date, "%Y-%m-%d") + timedelta(weeks=1)).strftime(
                "%Y-%m-%d")
            options.order_sell_option_limit(self.bought_option['symbol'], bought_option_strike, expiration_date, 'put',
                                            1)
            options.order_sell_option_limit(self.bought_option['symbol'], sold_option_strike, expiration_date, 'call',
                                            1)
            options.order_buy_option_limit(self.bought_option['symbol'], bought_option_strike, new_expiration_date,
                                           'put', 1)
            options.order_buy_option_limit(self.bought_option['symbol'], sold_option_strike, new_expiration_date,
                                           'call', 1)

            # Update the expiration_date variable for the next iteration
            expiration_date = new_expiration_date

        # Repeat the first three steps
        if datetime.strptime(expiration_date, "%Y-%m-%d") - datetime.now() <= timedelta(weeks=3):
            # Reset the initial values for the next iteration
            self.bought_option = input("Enter the bought option details: ")
            self.sold_option = input("Enter the sold option details: ")
            self.account_info = input("Enter the account information: ")
            self.trading_params = input("Enter the trading parameters: ")

# Rest of the code remains unchanged
