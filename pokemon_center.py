import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


BASE_URL = "https://www.pokemoncenter.com/en-gb/"


def get_pokemon_center_products():
    """
    Discover Pokémon products from Pokémon Center UK.
    Returns a list of products found.
    """

    products = []

    try:
        response = requests.get(
            BASE_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 "
                    "like Mac OS X)"
                )
            },
            timeout=20
        )

        print(f"Pokémon Center response: {response.status_code}")
print(f"Response URL: {response.url}")

if response.status_code != 200:
    print(f"Response preview: {response.text[:500]}")
    return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all("a", href=True)

        seen_urls = set()

        for link in links:

            href = link["href"]
            text = link.get_text(
                " ",
                strip=True
            )

            if not text:
                continue

            # Only look at possible product links
            if "/product/" not in href:
                continue

            product_url = urljoin(
                BASE_URL,
                href
            )

            if product_url in seen_urls:
                continue

            seen_urls.add(product_url)

            products.append({
                "name": text,
                "store": "Pokémon Center UK",
                "url": product_url,
                "price": None,
                "status": "FOUND"
            })

        print(
            f"Pokémon Center: "
            f"{len(products)} products found"
        )

        return products

    except Exception as error:

        print(
            "Pokémon Center error:",
            error
        )

        return []
