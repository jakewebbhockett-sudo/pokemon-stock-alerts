RETAILERS = [
    {
        "name": "Pokémon Center UK",
        "type": "official",
        "url": "https://www.pokemoncenter.com/en-gb/"
    },
    {
        "name": "Smyths Toys",
        "type": "major_retailer",
        "url": "https://www.smythstoys.com/uk/"
    },
    {
        "name": "Argos",
        "type": "major_retailer",
        "url": "https://www.argos.co.uk/"
    },
    {
        "name": "GAME",
        "type": "major_retailer",
        "url": "https://www.game.co.uk/"
    },
    {
        "name": "Magic Madhouse",
        "type": "specialist",
        "url": "https://magicmadhouse.co.uk/"
    },
    {
        "name": "Chaos Cards",
        "type": "specialist",
        "url": "https://www.chaoscards.co.uk/"
    },
    {
        "name": "Total Cards",
        "type": "specialist",
        "url": "https://totalcards.net/"
    },
    {
        "name": "Zatu Games",
        "type": "specialist",
        "url": "https://www.board-game.co.uk/"
    },
    {
        "name": "The Brotherhood Games",
        "type": "specialist",
        "url": "https://thebrotherhoodgames.co.uk/"
    },
    {
        "name": "Forbidden Planet",
        "type": "collectibles",
        "url": "https://forbiddenplanet.com/"
    },
    {
        "name": "LEGO",
        "type": "collectibles",
        "url": "https://www.lego.com/en-gb/"
    }
]


def get_retailer_names():
    """Return all retailer names."""
    return [retailer["name"] for retailer in RETAILERS]
