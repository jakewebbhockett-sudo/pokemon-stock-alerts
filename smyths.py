import requests
from bs4 import BeautifulSoup


SMYTHS_URL = (
    "https://www.smythstoys.com/"
    "uk/en-gb/toys/action-figures-and-playsets/"
    "pokemon-toys/pokemon-trading-card-game-tcg/"
    "c/SM0601011202"
)


def get_smyths_products():

    products = []

    try:

        response = requests.get(
            SMYTHS_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "Chrome/120.0 Safari/537.36"
                )
            },
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        print(
            "Smyths response:",
            response.status_code
        )

        # Find possible product links
        links = soup.find_all(
            "a",
            href=True
        )

        seen = set()

        for link in links:

            text = link.get_text(
                " ",
                strip=True
            )

            href = link["href"]

            if not text:
                continue

            # Only Pokémon / product-looking links
            if text in seen:
                continue

            if "pokemon" not in text.lower():
                continue

            seen.add(text)

            products.append({
                "name": text,
                "store": "Smyths Toys UK",
                "price": None,
                "url": href,
                "status": "FOUND"
            })

        print(
            f"Smyths: "
            f"{len(products)} products found"
        )

        return products

    except Exception as error:

        print(
            "Smyths error:",
            error
        )

        return []
