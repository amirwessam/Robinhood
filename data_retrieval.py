import robin_stocks as rh


def get_option_data(symbol, expiration_date):
    try:
        # Retrieve option chain data for the specified symbol and expiration date
        option_chain = rh.options.find_tradable_options(symbol, expirationDate=expiration_date)
        return option_chain
    except Exception as e:
        print(f"Error retrieving option data: {str(e)}")
        return None


def get_share_price(symbol):
    try:
        # Retrieve the current share price for the specified symbol
        price = rh.stocks.get_latest_price(symbol)
        if price:
            return float(price[0])
        else:
            print(f"Error retrieving share price for symbol: {symbol}")
            return None
    except Exception as e:
        print(f"Error retrieving share price: {str(e)}")
        return None


def process_option_data(option_chain):
    try:
        # Process and transform the option chain data as needed
        # For example, filter options based on certain criteria or extract specific attributes
        processed_data = option_chain  # Placeholder, replace with your actual processing logic
        return processed_data
    except Exception as e:
        print(f"Error processing option data: {str(e)}")
        return None


if __name__ == "__main__":
    # Example usage:
    symbol = input("Enter the stock symbol: ")
    expiration_date = input("Enter the expiration date of the option (YYYY-MM-DD): ")

    # Retrieve option data
    option_chain = get_option_data(symbol, expiration_date)
    if option_chain:
        processed_option_data = process_option_data(option_chain)
        if processed_option_data:
            print("Option data retrieved and processed successfully.")
            print(processed_option_data)
    else:
        print("Failed to retrieve option data.")

    # Retrieve share price
    share_price = get_share_price(symbol)
    if share_price:
        print(f"Current share price of {symbol}: {share_price}")
    else:
        print(f"Failed to retrieve share price for symbol: {symbol}")

