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


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/120.0 Safari/537.36"
    )
}


# Generic links we NEVER want alerts for
GENERIC_TITLES = [
    "pokemon",
    "pokémon",
    "booster boxes",
    "booster box",
    "booster packs",
    "booster pack",
    "elite trainer boxes",
    "elite trainer box",
    "etb",
    "prerelease packs",
    "prerelease pack",
    "pokemon tcg sets",
    "boosters",
    "sleeved boosters",
    "booster bundles",
    "booster bundle",
    "japanese tcg",
    "simplified chinese tcg",
    "traditional chinese tcg",
    "korean tcg",
    "preorder",
    "pre-order",
    "preorders",
    "pre-orders",
    "restocks",
    "shop all restocks",
    "new releases",
    "new release"
]


def is_generic(title):
    """Reject generic category links."""

    if not title:
        return True

    title = title.lower().strip()

    return title in GENERIC_TITLES


def is_relevant(title, url=""):
    """
    Check whether this looks like a real
    Pokémon product or announcement.
    """

    if not title:
        return False

    title_lower = title.lower()

    # Reject generic category pages
    if is_generic(title):
        return False

    # Must contain Pokémon in title or URL
    combined = (
        title_lower + " " + url.lower()
    )

    pokemon_words = [
        "pokemon",
        "pokémon"
    ]

    if not any(
        word in combined
        for word in pokemon_words
    ):
        return False

    # Must contain useful product/news wording
    useful_words = [
        "30th",
        "celebration",
        "mega",
        "delta",
        "reign",
        "destined",
        "rivals",
        "ascended",
        "heroes",
        "surging",
        "sparks",
        "prismatic",
        "evolutions",
        "booster",
        "elite trainer",
        "collection",
        "premium",
        "box",
        "bundle",
        "tin",
        "officially revealed",
        "coming",
        "restock",
        "back in stock",
        "pre-order",
        "preorder",
        "release",
        "launch"
    ]

    return any(
        word in combined
        for word in useful_words
    )


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

            if not is_relevant(
                title,
                url
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

                url = urljoin(
                    page_url,
                    href
                )

                if url in seen_urls:
                    continue

                seen_urls.add(url)

                if not is_relevant(
                    title,
                    url
                ):
                    continue

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
                f"{len(announcements)} total alerts so far"
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
