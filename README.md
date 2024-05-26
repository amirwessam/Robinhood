# **Trading Bot README**

## **Overview**
This repository contains the implementation of a trading bot using the Robinhood API. The bot is designed to automate trading options and shares based on predefined conditions and strategies. The main components of the bot include authentication, data retrieval, trading logic, and a user interface.

## **Files**
- **`authentication.py`**: Handles the authentication process with the Robinhood API using credentials stored in an environment file.
- **`bot_options.py`**: Contains the `CoveredSharesBot` class, which implements the trading logic for managing covered shares.
- **`data_retrieval.py`**: Provides functions to retrieve and process stock and option data from the Robinhood API.
- **`main.py`**: Defines the main application using Tkinter for the user interface, allowing users to log in and interact with the trading bot.
- **`monitoring.py`**: Implements the `DataMonitor` class to continuously monitor stock and option data and trigger trading actions.
- **`shares_bot.py`**: Contains additional logic for the `CoveredSharesBot` class.
- **`utils.py`**: Utility functions for data validation, percentage change calculations, and other helper methods.

## **Installation**
1. **Clone the repository:**
    ```sh
    git clone https://github.com/amirwessam/automated-trading-bot.git
    ```
2. **Create and activate a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install the required dependencies:**
    ```sh
    pip install robin-stocks python-dotenv tkinter
    ```
4. **Create a `.env` file in the root directory of the project and add your Robinhood credentials:**
    ```sh
    ROBINHOOD_USERNAME=your_username
    ROBINHOOD_PASSWORD=your_password
    ```

## **Usage**
1. **Run the main application:**
    ```sh
    python main.py
    ```
2. **Log in using your Robinhood credentials through the user interface.**
3. **The trading bot will start monitoring stock and option data and execute trades based on the predefined conditions.**

## **Classes and Functions**

### **`authentication.py`**
- **`authenticate()`**: Authenticates with Robinhood using credentials from the `.env` file.

### **`bot_options.py`**
- **`CoveredSharesBot`**: Class for managing covered shares and executing trading logic.
  - **`retrieve_stock_data()`**: Retrieves the current stock price.
  - **`condition_1_shares_decline()`**: Checks if shares have declined by 80% of the premium collected and buys a put option if true.
  - **`condition_2_shares_rise_above_strike()`**: Checks if shares have risen above the strike price and buys a call option if true.
  - **`close_trade()`**: Closes all positions if the take profit point is reached.
  - **`buy_put_option(strike)`**: Buys a put option at the specified strike price.
  - **`buy_call_option(strike)`**: Buys a call option at the specified strike price.
  - **`close_all_positions()`**: Closes all open positions.
  - **`execute_trading_bot()`**: Continuously executes the trading bot logic.

### **`data_retrieval.py`**
- **`get_option_data(symbol, expiration_date)`**: Retrieves option chain data.
- **`get_share_price(symbol)`**: Retrieves the current share price.
- **`process_option_data(option_chain)`**: Processes and transforms option chain data.

### **`main.py`**
- **`TradingBotApp`**: Tkinter-based application for user interaction.
  - **`login()`**: Authenticates the user and shows the trading bot window.

### **`monitoring.py`**
- **`DataMonitor`**: Class for monitoring stock and option data.
  - **`start_monitoring(interval)`**: Starts monitoring the data source at the specified interval.
  - **`process_data(data)`**: Processes data and triggers events based on defined conditions.
  - **`is_option_expired(expiration_date)`**: Checks if an option has expired based on its expiration date.

### **`shares_bot.py`**
Contains similar logic to `bot_options.py` for managing covered shares with additional functionalities.

### **`utils.py`**
- **`calculate_percentage_change(initial_value, final_value)`**: Calculates the percentage change between two values.
- **`is_option_expired(expiration_date)`**: Checks if an option has expired.
- **`validate_option_data(option_data)`**: Validates option data.
- **`calculate_net_gain(stock_price_gain, call_option_gain, sold_option_loss)`**: Calculates the net gain from trades.
- **`is_net_gain_reached(net_gain, take_profit_point, average_cost_per_share, premium_collected)`**: Checks if the net gain reaches the take profit point.
- **`validate_stock_data(stock_data)`**: Validates stock data.

## **Notes**
- Ensure that your Robinhood credentials are kept secure and not shared publicly.
