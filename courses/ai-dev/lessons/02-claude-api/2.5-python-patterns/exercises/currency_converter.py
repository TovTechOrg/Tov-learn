# currency_converter.py
import requests

def get_usd_exchange_rate():
    url = "https://boi.org.il/PublicApi/GetExchangeRate?key=USD"
    x = requests.get(url=url)
    if x.status_code == 200:
        data = x.json()
        return float(data['currentExchangeRate'])
    else:
        print("Error fetching exchange rate:", x.status_code)
        return None


def convert_shekel_to_usd(amount_nis, rate):
    """Converts an amount from NIS to USD using a given rate."""
    return amount_nis / rate

# --- Main script ---
current_rate = get_usd_exchange_rate()
if current_rate:
    amount_in_nis = 15000
    amount_in_usd = convert_shekel_to_usd(amount_in_nis, current_rate)
    print(f"{amount_in_nis} ש\"ח שווים ל-${amount_in_usd:.2f}")
else:
    print("Failed to get the exchange rate.")
