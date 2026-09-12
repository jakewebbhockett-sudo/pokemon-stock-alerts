import re


# Stores we care about
RETAILERS = [
    "Smyths",
    "Smyths Toys",
    "Argos",
    "GAME",
    "Tesco",
    "The Entertainer",
    "Magic Madhouse",
    "Chaos Cards",
    "Total Cards",
    "Zatu",
    "Forbidden Planet",
    "Pokémon Center",
    "Pokemon Center",
    "John Lewis",
    "Very",
    "ASDA",
    "Currys",
    "HMV"
]


# Words that suggest useful stock information
RESTOCK_WORDS = [
    "restock",
    "restocked",
    "restocking",
    "back in stock",
    "in stock",
    "now in stock",
    "stocked",
    "stocking",
    "available now",
    "available today",
    "coming tomorrow",
    "restocking tomorrow",
    "restock tomorrow",
    "stock tomorrow",
    "delivery tomorrow",
    "delivery day",
    "arriving tomorrow",
    "arriving today",
    "expected tomorrow",
    "expected",
    "drops tomorrow",
    "drop tomorrow",
    "releasing tomorrow",
    "release tomorrow",
    "going live",
    "goes live",
    "preorder",
    "pre-order"
]


def contains_pokemon(text):
    """
    Check if text mentions Pokémon.
    """

    if not text:
        return False

    text = text.lower()

    return (
        "pokemon" in text
        or "pokémon" in text
        or "pokemon tcg" in text
        or "pokémon tcg" in text
    )


def find_retailer(text):
    """
    Find which retailer is mentioned.
    """

    if not text:
        return "Unknown"

    text_lower = text.lower()

    for retailer in RETAILERS:

        if retailer.lower() in text_lower:
            return retailer

    return "Unknown"


def find_restock_words(text):
    """
    Return stock/restock phrases found.
    """

    if not text:
        return []

    text_lower = text.lower()

    found_words = []

    for word in RESTOCK_WORDS:

        if word in text_lower:
            found_words.append(word)

    return found_words


def is_restock_post(text):
    """
    Decide whether text looks like
    useful Pokémon stock information.
    """

    if not text:
        return False

    # Must mention Pokémon
    if not contains_pokemon(text):
        return False

    # Must mention stock/restock information
    restock_words = find_restock_words(text)

    if not restock_words:
        return False

    return True


def analyse_post(
    text,
    source="Unknown",
    url=""
):
    """
    Analyse one post or announcement.

    Returns useful information if
    it looks like Pokémon restock news.
    """

    if not is_restock_post(text):
        return None

    retailer = find_retailer(text)

    keywords = find_restock_words(text)

    return {
        "text": text,
        "store": retailer,
        "keywords": keywords,
        "source": source,
        "url": url
    }


def test_posts():
    """
    TEST MODE.

    These are example posts so we can
    confirm the intelligence filter works.
    """

    example_posts = [

        {
            "text": (
                "Pokémon cards are being "
                "restocked at Smyths tomorrow!"
            ),
            "source": "Example Community Post",
            "url": "https://example.com/1"
        },

        {
            "text": (
                "Argos has Pokémon TCG "
                "back in stock now."
            ),
            "source": "Example Retailer Post",
            "url": "https://example.com/2"
        },

        {
            "text": (
                "Smyths are getting a "
                "Pokémon delivery tomorrow."
            ),
            "source": "Example Community Post",
            "url": "https://example.com/3"
        },

        {
            "text": (
                "New Pokémon artwork released!"
            ),
            "source": "Example News",
            "url": "https://example.com/4"
        }
    ]

    results = []

    print("")
    print("📱 TESTING SOCIAL RESTOCK FILTER")
    print("")

    for post in example_posts:

        result = analyse_post(
            text=post["text"],
            source=post["source"],
            url=post["url"]
        )

        if result:

            results.append(result)

            print("🚨 RESTOCK INTEL FOUND")
            print(
                f"Store: "
                f"{result['store']}"
            )

            print(
                f"Keywords: "
                f"{', '.join(result['keywords'])}"
            )

            print(
                f"Post: "
                f"{result['text']}"
            )

            print(
                f"Source: "
                f"{result['source']}"
            )

            print("")

        else:

            print(
                "❌ Ignored irrelevant post"
            )

    print(
        f"📊 Total useful posts: "
        f"{len(results)}"
    )

    return results
