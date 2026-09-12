import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


POKEMON_NEWS_URL = (
    "https://www.pokemon.com/uk/pokemon-news/"
)


RETAILER_SOURCES = [
    {
        "store": "Chaos Cards",
        "source": "Chaos Cards News",
        "url": "https://www.chaoscards.co.uk/blog"
    },
    {
        "store": "Magic Madhouse",
        "source": "Magic Madhouse",
        "url": "https://magicmadhouse.co.uk/"
    },
    {
        "store": "Total Cards",
        "source": "Total Cards",
        "url": "https://totalcards.net/"
    },
    {
        "store": "Zatu Games",
        "source": "Zatu Games",
        "url": "https://zatu.com/"
    }
]


KEYWORDS = [
    "pokemon",
    "pokémon",
    "restock",
    "restocked",
    "back in stock",
    "coming soon",
    "pre-order",
    "preorder",
    "product drop",
    "new release",
    "release",
    "booster",
    "elite trainer",
    "etb",
    "tcg"
]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120.0 Safari/537.36"
    )
}


def is_relevant(text):

    if not text:
        return False

    text = text.lower()

    pokemon_words = [
        "pokemon",
        "pokémon"
    ]

    stock_words = [
        "restock",
        "restocked",
        "back in stock",
        "coming soon",
        "pre-order",
        "preorder",
        "product drop",
        "release",
        "booster",
        "elite trainer",
        "etb",
        "tcg"
    ]

    has_pokemon = any(
        word in text
        for word in pokemon_words
    )

    has_stock_word = any(
        word in text
        for word in stock_words
    )

    return has_pokemon and has_stock_word


def get_pokemon_announcements():

    announcements = []

    print(
        "📢 Checking official Pokémon UK news..."
    )

    try:

        response = requests.get(
            POKEMON_NEWS_URL,
            headers=HEADERS,
            timeout=20
        )

        print(
            f"Pokémon News response: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        seen_urls = set()

        for link in soup.find_all(
            "a",
            href=True
        ):

            title = link.get_text(
                " ",
                strip=True
            )

            href = link["href"]

            if not title:
                continue

            if "/uk/news/" not in href:
                continue

            url = urljoin(
                "https://www.pokemon.com",
                href
            )

            if url in seen_urls:
                continue

            seen_urls.add(url)

            title_lower = title.lower()

            relevant_words = [
                "tcg",
                "trading card",
                "product",
                "release",
                "expansion",
                "booster",
                "elite trainer",
                "collection",
                "pokemon center"
            ]

            if not any(
                word in title_lower
                for word in relevant_words
            ):
                continue

            announcements.append({
                "title": title,
                "store": "Official Pokémon UK",
                "source": "Pokémon UK News",
                "url": url,
                "type": "OFFICIAL",
                "confidence": "HIGH"
            })

    except Exception as error:

        print(
            "Pokémon News error:",
            error
        )

    return announcements


def get_retailer_announcements():

    announcements = []

    print(
        "🏪 Checking retailer announcements..."
    )

    for retailer in RETAILER_SOURCES:

        store = retailer["store"]
        source = retailer["source"]
        page_url = retailer["url"]

        print(
            f"Checking {store}..."
        )

        try:

            response = requests.get(
                page_url,
                headers=HEADERS,
                timeout=20
            )

            print(
                f"{store} response: "
                f"{response.status_code}"
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            seen_urls = set()

            for link in soup.find_all(
                "a",
                href=True
            ):

                title = link.get_text(
                    " ",
                    strip=True
                )

                href = link["href"]

                if not title:
                    continue

                combined_text = (
                    title + " " + href
                )

                if not is_relevant(
                    combined_text
                ):
                    continue

                url = urljoin(
                    page_url,
                    href
                )

                if url in seen_urls:
                    continue

                seen_urls.add(url)

                announcements.append({
                    "title": title,
                    "store": store,
                    "source": source,
                    "url": url,
                    "type": "RETAILER",
                    "confidence": "MEDIUM"
                })

            print(
                f"{store}: "
                f"{len(seen_urls)} relevant links"
            )

        except Exception as error:

            print(
                f"{store} error:",
                error
            )

    return announcements


def get_announcements():

    announcements = []

    announcements.extend(
        get_pokemon_announcements()
    )

    announcements.extend(
        get_retailer_announcements()
    )

    print(
        f"📢 Total announcements: "
        f"{len(announcements)}"
    )

    return announcements
