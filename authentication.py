

import robin_stocks.authentication as auth


def authenticate(username, password):
    try:
        # The auth.login function might be returning a dictionary or some other data structure.
        # You would need to check the documentation or the function's source code to know for sure.
        response = auth.login(username=username, password=password)

        # If response is a dictionary containing the access_token and refresh_token, you could extract them like this:
        access_token = response.get('access_token')
        refresh_token = response.get('refresh_token')

        return access_token, refresh_token

    except Exception as e:
        print(f"Authentication failed: {str(e)}")

    return None, None


