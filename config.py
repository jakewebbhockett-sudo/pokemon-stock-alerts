import os


# Telegram - these stay private in Railway
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


# Bot settings
CHECK_INTERVAL_MINUTES = 15

# Only alert immediately for scores at or above this
HIGH_PRIORITY_SCORE = 8.0

# Country
COUNTRY = "UK"
CURRENCY = "GBP"
