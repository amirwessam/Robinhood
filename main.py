import tkinter as tk
from tkinter import font, ttk

from authentication import authenticate
from bot_options import OptionsTradingBot
from shares_bot import CoveredSharesBot
from utils import YourDataSource

class TradingBotApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.state('zoomed')

        self.configure(bg='darkblue')
        self.title("Trading Bot")

        self.customFont = font.Font(family="Helvetica", size=12)
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=self.customFont, foreground="black", background="lightblue")
        self.style.configure("TLabel", font=self.customFont, background="darkblue", foreground="white")

        self.label_username = ttk.Label(self, text="Username:")
        self.entry_username = ttk.Entry(self)
        self.label_password = ttk.Label(self, text="Password:")
        self.entry_password = ttk.Entry(self, show="*")
        self.button_login = ttk.Button(self, text="Login", command=self.login)

        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.button_login.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.stock_count = None
        self.bot_type = None
        self.stock_symbol = None
        self.long_option_cost = None
        self.long_option_strike = None
        self.short_option_premium = None
        self.short_option_strike = None

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        access_token, refresh_token = authenticate(username, password)

        if access_token and refresh_token:
            self.show_trading_bot_window(username)
        else:
            print("Authentication failed.")

    def show_trading_bot_window(self, username):
        self.destroy()

        self.trading_bot_window = tk.Toplevel()
        self.trading_bot_window.state('zoomed')  # this line maximizes the window
        self.trading_bot_window.title("Trading Bot")

        self.label_username = tk.Label(self.trading_bot_window, text=f"Welcome, {username}!")
        self.label_username.pack()

        # UI elements for trading bot options
        self.btn_stock_count = tk.Button(self.trading_bot_window, text="Number of stocks selected", command=self.set_stock_count)
        self.btn_bot_type = tk.Button(self.trading_bot_window, text="Select bot type", command=self.set_bot_type)
        self.btn_stock_symbol = tk.Button(self.trading_bot_window, text="Enter stock symbol", command=self.set_stock_symbol)
        self.btn_long_option_cost = tk.Button(self.trading_bot_window, text="Enter long option cost to buy", command=self.set_long_option_cost)
        self.btn_long_option_strike = tk.Button(self.trading_bot_window, text="Enter long option strike", command=self.set_long_option_strike)
        self.btn_short_option_premium = tk.Button(self.trading_bot_window, text="Enter short option premium collected", command=self.set_short_option_premium)
        self.btn_short_option_strike = tk.Button(self.trading_bot_window, text="Enter short option strike", command=self.set_short_option_strike)
        self.btn_add_bot = tk.Button(self.trading_bot_window, text="Add bot", command=self.add_bot)
        self.btn_run_bots = tk.Button(self.trading_bot_window, text="Run bots", command=self.run_bots)

        # Grid layout for the bot options
        self.btn_stock_count.pack()
        self.btn_bot_type.pack()
        self.btn_stock_symbol.pack()
        self.btn_long_option_cost.pack()
        self.btn_long_option_strike.pack()
        self.btn_short_option_premium.pack()
        self.btn_short_option_strike.pack()
        self.btn_add_bot.pack()
        self.btn_run_bots.pack()

    # Define the methods that correspond to each button's action
    def set_stock_count(self):
        self.stock_count_label = tk.Label(self.trading_bot_window, text="Stock Count:")
        self.stock_count = tk.Entry(self.trading_bot_window)
        self.stock_count_label.pack()
        self.stock_count.pack()

    def set_bot_type(self):
        self.bot_type_label = tk.Label(self.trading_bot_window, text="Bot Type:")
        self.bot_type = tk.Entry(self.trading_bot_window)
        self.bot_type_label.pack()
        self.bot_type.pack()

    def set_stock_symbol(self):
        self.stock_symbol_label = tk.Label(self.trading_bot_window, text="Stock Symbol:")
        self.stock_symbol = tk.Entry(self.trading_bot_window)
        self.stock_symbol_label.pack()
        self.stock_symbol.pack()

    def set_long_option_cost(self):
        self.long_option_cost_label = tk.Label(self.trading_bot_window, text="Long Option Cost:")
        self.long_option_cost = tk.Entry(self.trading_bot_window)
        self.long_option_cost_label.pack()
        self.long_option_cost.pack()

    def set_long_option_strike(self):
        self.long_option_strike_label = tk.Label(self.trading_bot_window, text="Long Option Strike:")
        self.long_option_strike = tk.Entry(self.trading_bot_window)
        self.long_option_strike_label.pack()
        self.long_option_strike.pack()

    def set_short_option_premium(self):
        self.short_option_premium_label = tk.Label(self.trading_bot_window, text="Short Option Premium:")
        self.short_option_premium = tk.Entry(self.trading_bot_window)
        self.short_option_premium_label.pack()
        self.short_option_premium.pack()

    def set_short_option_strike(self):
        self.short_option_strike_label = tk.Label(self.trading_bot_window, text="Short Option Strike:")
        self.short_option_strike = tk.Entry(self.trading_bot_window)
        self.short_option_strike_label.pack()
        self.short_option_strike.pack()
    def add_bot(self):
        premium_collected = self.premium_collected.get()
        avg_cost_per_share = self.avg_cost_per_share.get()

        # Check if the fields are not empty
        if premium_collected and avg_cost_per_share:
            try:
                premium_collected = float(premium_collected)
                avg_cost_per_share = float(avg_cost_per_share)
            except ValueError:
                print("Invalid input. Please enter a number.")
                return

            # Create the bot
            self.bot = CoveredSharesBot(
                stock_symbol=self.stock_symbol.get(),
                option_expiration=self.option_expiration.get(),
                premium_collected=premium_collected,
                avg_cost_per_share=avg_cost_per_share,
                trading_params=self.trading_params,
                data_source=self.data_source
            )
        else:
            print("All fields must be filled.")

    def run_bots(self):
        print("Running bots")

if __name__ == "__main__":
    app = TradingBotApp()
    app.mainloop()
    stock_symbol = app.stock_symbol.get()
