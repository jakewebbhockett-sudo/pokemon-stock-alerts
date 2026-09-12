import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


POKEMON_NEWS_URL = (
    "https://www.pokemon.com/uk/pokemon-news/"
)

BASE_URL = "https://www.pokemon.com"


def get_announcements():

    announcements = []

    print("📢 Checking official Pokémon UK news...")

    try:

        response = requests.get(
            POKEMON_NEWS_URL,
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

        print(
            f"Pokémon News response: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        links = soup.find_all(
            "a",
            href=True
        )

        seen_urls = set()

        for link in links:

            title = link.get_text(
                " ",
                strip=True
            )

            href = link.get(
                "href",
                ""
            )

            if not title:
                continue

            if "/uk/news/" not in href:
                continue

            url = urljoin(
                BASE_URL,
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

        print(
            f"Official Pokémon announcements: "
            f"{len(announcements)} found"
        )

        return announcements

    except Exception as error:

        print(
            "Pokémon News error:",
            error
        )

        return []
