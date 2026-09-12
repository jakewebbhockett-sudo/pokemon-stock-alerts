import os
import requests
from bs4 import BeautifulSoup


# Your Telegram details will be stored securely later
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_message(message):
    """Send an alert to your Telegram bot."""

    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Telegram details have not been added yet.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=data, timeout=10)
    print(response.text)


def check_product(name, url):
    """Check a product page for stock."""

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text(" ", strip=True).lower()

        out_of_stock_words = [
            "out of stock",
            "sold out",
            "currently unavailable"
        ]

        in_stock = not any(
            word in page_text
            for word in out_of_stock_words
        )

        return in_stock

    except Exception as error:
        print(f"Error checking {name}: {error}")
        return False


print("Pokémon Stock Alert Bot is running!")
