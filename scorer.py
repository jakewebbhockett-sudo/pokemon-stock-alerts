def score_product(product_name, store, price, product_type="", exclusive=False):
    """
    Give a Pokémon product an opportunity score out of 10.
    This is an estimate, not a guarantee of future value.
    """

    score = 5.0
    reasons = []

    name = product_name.lower()
    store_name = store.lower()
    product_type = product_type.lower()

    # Anniversary products
    if "30th" in name or "anniversary" in name:
        score += 2.0
        reasons.append("🎂 Anniversary product")

    # Pokémon Center exclusives
    if "pokemon center" in store_name or exclusive:
        score += 1.5
        reasons.append("⭐ Exclusive product")

    # Premium products
    premium_words = [
        "ultra-premium",
        "premium collection",
        "premium",
        "special collection"
    ]

    if any(word in name or word in product_type for word in premium_words):
        score += 1.0
        reasons.append("🎁 Premium collector product")

    # Popular Pokémon
    popular_pokemon = [
        "pikachu",
        "charizard",
        "eevee",
        "umbreon",
        "mew",
        "mewtwo",
        "lugia",
        "rayquaza",
        "gengar"
    ]

    if any(pokemon in name for pokemon in popular_pokemon):
        score += 1.0
        reasons.append("🔥 Popular Pokémon")

    # Booster boxes and ETBs tend to have sealed collector appeal
    collector_types = [
        "booster box",
        "booster bundle",
        "elite trainer box",
        "etb",
        "ultra-premium"
    ]

    if any(item in name or item in product_type for item in collector_types):
        score += 0.5
        reasons.append("📦 Strong sealed collector appeal")

    # Keep score between 1 and 10
    score = max(1.0, min(score, 10.0))

    # Default reason
    if not reasons:
        reasons.append("🆕 New Pokémon collectible")

    return round(score, 1), reasons
