import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


SMYTHS_URL = (
    "https://www.smythstoys.com/"
    "uk/en-gb/toys/action-figures-and-playsets/"
    "pokemon-toys/pokemon-trading-card-game-tcg/"
    "c/SM0601011202"
)

BASE_URL = "https://www.smythstoys.com"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9"
}


def get_stock_status(item):

    availability = str(
        item.get("availability", "")
    ).lower()

    if "instock" in availability:
        return "IN STOCK"

    if "outofstock" in availability:
        return "OUT OF STOCK"

    return "UNKNOWN"


def get_smyths_products():

    products = []

    try:

        response = requests.get(
            SMYTHS_URL,
            headers=HEADERS,
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

        # Look for structured product data
        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        print(
            f"Smyths structured data blocks: "
            f"{len(scripts)}"
        )

        seen_urls = set()

        for script in scripts:

            try:

                data = json.loads(
                    script.string
                )

            except Exception:
                continue

            # JSON-LD can contain one item
            # or a list of items
            if isinstance(data, list):
                items = data

            else:
                items = [data]

            for item in items:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                # Look for product lists
                if item.get("@type") == "ItemList":

                    elements = item.get(
                        "itemListElement",
                        []
                    )

                    for element in elements:

                        product = element.get(
                            "item",
                            element
                        )

                        add_smyths_product(
                            products,
                            product,
                            seen_urls
                        )

                # Individual product
                elif item.get("@type") == "Product":

                    add_smyths_product(
                        products,
                        item,
                        seen_urls
                    )

        print(
            f"Smyths: "
            f"{len(products)} products found"
        )

        if len(products) == 0:

            print(
                "Smyths product data not found "
                "in JSON-LD"
            )

            print(
                "HTML length: "
                f"{len(response.text)}"
            )

            print(
                "Checking page for Pokémon text: "
                f"{'pokemon' in response.text.lower()}"
            )

        return products

    except Exception as error:

        print(
            "Smyths error:",
            error
        )

        return []


def add_smyths_product(
    products,
    item,
    seen_urls
):

    if not isinstance(item, dict):
        return

    name = item.get(
        "name",
        ""
    )

    if not name:
        return

    # Only Pokémon products
    if "pokemon" not in name.lower():
        return

    url = item.get(
        "url",
        ""
    )

    if not url:
        return

    url = urljoin(
        BASE_URL,
        url
    )

    if url in seen_urls:
        return

    seen_urls.add(url)

    offers = item.get(
        "offers",
        {}
    )

    if isinstance(offers, list):

        if offers:
            offers = offers[0]

        else:
            offers = {}

    if not isinstance(
        offers,
        dict
    ):
        offers = {}

    price = offers.get(
        "price",
        None
    )

    availability = offers.get(
        "availability",
        ""
    )

    status = "UNKNOWN"

    availability_lower = str(
        availability
    ).lower()

    if "instock" in availability_lower:

        status = "IN STOCK"

    elif "outofstock" in availability_lower:

        status = "OUT OF STOCK"

    products.append({

        "name": name,

        "store": "Smyths Toys UK",

        "price": (
            f"£{price}"
            if price
            else None
        ),

        "url": url,

        "status": status

    })

    print(
        f"Smyths product: "
        f"{name} | "
        f"{status}"
    )
