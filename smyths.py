import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


SMYTHS_URL = (
    "https://www.smythstoys.com/"
    "uk/en-gb/toys/action-figures-and-playsets/"
    "pokemon-toys/pokemon-trading-card-game-tcg/"
    "c/SM0601011202"
)

BASE_URL = "https://www.smythstoys.com"


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
                    "(KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-GB,en;q=0.9"
            },
            timeout=20
        )

        print(
            f"Smyths response: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Find ALL links first
        links = soup.find_all(
            "a",
            href=True
        )

        seen_urls = set()

        for link in links:

            href = link.get("href", "")

            # Look for Smyths product pages
            if "/p/" not in href:
                continue

            product_url = urljoin(
                BASE_URL,
                href
            )

            if product_url in seen_urls:
                continue

            seen_urls.add(product_url)

            # Get product name
            name = link.get_text(
                " ",
                strip=True
            )

            # Sometimes product name is inside
            # an aria-label instead
            if not name:
                name = link.get(
                    "aria-label",
                    ""
                )

            if not name:
                continue

            # Only Pokémon products
            if "pokemon" not in name.lower():
                continue

            products.append({
                "name": name,
                "store": "Smyths Toys UK",
                "price": None,
                "url": product_url,
                "status": "FOUND"
            })

        print(
            f"Smyths: "
            f"{len(products)} products found"
        )

        # Debug information
        if len(products) == 0:
            print(
                "Smyths page loaded but "
                "no product links found"
            )

        return products

    except Exception as error:

        print(
            "Smyths error:",
            error
        )

        return []
