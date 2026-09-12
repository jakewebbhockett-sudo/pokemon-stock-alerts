import requests

from config import TELEGRAM_TOKEN, CHAT_ID


def send_telegram_alert(
    product_name,
    store,
    price,
    status,
    score,
    reasons,
    product_url
):
    """Send a Pokémon product alert to Telegram."""

    message = f"""
🚨 <b>POKÉMON ALERT!</b>

📦 <b>{product_name}</b>

🏪 <b>STORE:</b> {store}
💷 <b>PRICE:</b> £{price}
📊 <b>STATUS:</b> {status}

⭐ <b>OPPORTUNITY SCORE:</b> {score}/10

🔥 <b>WHY IT'S INTERESTING:</b>
{reasons}

🛒 <b>BUY NOW:</b>
{product_url}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(
            url,
            data=data,
            timeout=15
        )

        response.raise_for_status()
        print(f"Alert sent: {product_name} - {store}")

    except Exception as error:
        print(f"Error sending Telegram alert: {error}")
