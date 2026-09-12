import re


KEYWORDS = [
    "pokemon",
    "pokémon",
    "restock",
    "restocked",
    "back in stock",
    "coming soon",
    "pre-order",
    "preorder",
    "available",
    "release"
]


def is_relevant_announcement(text):
    """Check if an announcement is relevant to Pokémon stock."""

    if not text:
        return False

    text = text.lower()

    return any(
        keyword in text
        for keyword in KEYWORDS
    )


def create_announcement(
    title,
    store,
    source,
    url,
    announcement_type="COMMUNITY",
    confidence="MEDIUM"
):
    """Create a standard announcement."""

    return {
        "title": title,
        "store": store,
        "source": source,
        "url": url,
        "type": announcement_type,
        "confidence": confidence
    }


def get_announcements():
    """
    Get Pokémon restock and release announcements.

    Sources will be added individually:
    - Official retailer announcements
    - Pokémon news
    - Restock communities
    - Local stock reports
    """

    announcements = []

    print("📢 Checking announcements...")

    return announcements
