import robin_stocks
import robin_stocks.options

class CoveredSharesBot:
    def __init__(self, stock_symbol, option_expiration, premium_collected, avg_cost_per_share, trading_params, data_source):
        self.stock_symbol = stock_symbol
        self.option_expiration = option_expiration
        self.premium_collected = premium_collected
        self.avg_cost_per_share = avg_cost_per_share
        self.trading_params = trading_params
        self.data_source = data_source

        # Initialize the current_price to None (or some default value)
        self.current_price = None

        # The 80% trigger point
        self.trigger_point = self.premium_collected * 0.8

        # The 60% sell point
        self.sell_point = self.premium_collected * 0.6

        # The 50% take profit point
        self.take_profit = self.trading_params.get('take_profit')

        # The put strike price
        self.put_strike = self.avg_cost_per_share - self.trigger_point

        # The call strike price
        self.call_strike = self.avg_cost_per_share + self.premium_collected

    def retrieve_stock_data(self):
        try:
            stock_data = self.data_source.get_stock_price(self.stock_symbol)
            self.current_price = float(stock_data['last_trade_price'])
        except Exception as e:
            print("Error retrieving stock data:", e)

    def condition_1_shares_decline(self):
        if self.current_price <= (self.avg_cost_per_share - self.trigger_point):
            print("Shares have declined by 80% of premium collected. Buying a put option...")

            # Buy the put option
            robin_stocks.options.trade_option(
                optionType='put',
                symbol=self.stock_symbol,
                expirationDate=self.option_expiration,
                strike=self.put_strike,
                price='ask_price',
                quantity=1,
                action='buy_to_open'
            )

            # Sell the put option when the shares rise above the 60% sell point
            if self.current_price >= (self.avg_cost_per_share - self.sell_point):
                print("Shares have risen above the 80% threshold. Selling the put option...")

                robin_stocks.options.trade_option(
                    optionType='put',
                    symbol=self.stock_symbol,
                    expirationDate=self.option_expiration,
                    strike=self.put_strike,
                    price='ask_price',
                    quantity=1,
                    action='sell_to_close'
                )

    def condition_2_shares_rise_above_strike(self):
        if self.current_price >= self.call_strike:
            print("Shares have risen above the strike price. Buying a call option...")

            # Buy the call option
            robin_stocks.options.trade_option(
                optionType='call',
                symbol=self.stock_symbol,
                expirationDate=self.option_expiration,
                strike=self.call_strike,
                price='ask_price',
                quantity=1,
                action='buy_to_open'
            )

            # Sell the call option when the shares fall below the 50% take profit point
            if self.current_price <= (self.avg_cost_per_share - self.take_profit):
                print("Shares have fallen below the 50% threshold. Selling the call option...")

                robin_stocks.options.trade_option(
                    optionType='call',
                    symbol=self.stock_symbol,
                    expirationDate=self.option_expiration,
                    strike=self.call_strike,
                    price='ask_price',
                    quantity=1,
                    action='sell_to_close'
                )

    def run(self):
        while True:
            # Check the current stock price
            self.retrieve_stock_data()
            # Run conditions
            self.condition_1_shares_decline()
            self.condition_2_shares_rise_above_strike()
