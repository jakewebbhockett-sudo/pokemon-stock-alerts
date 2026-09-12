import json
import os


DATABASE_FILE = "products.json"


def load_products():
    """Load previously discovered products."""

    if not os.path.exists(DATABASE_FILE):
        return {}

    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return {}


def save_products(products):
    """Save discovered products."""

    with open(DATABASE_FILE, "w") as file:
        json.dump(products, file, indent=2)


def product_key(store, product_name):
    """Create a unique ID for a product."""

    clean_store = store.lower().replace(" ", "_")
    clean_name = product_name.lower().replace(" ", "_")

    return f"{clean_store}_{clean_name}"


def is_new_product(products, store, product_name):
    """Check whether we've seen this product before."""

    key = product_key(store, product_name)
    return key not in products


def add_product(products, store, product_name, price, url):
    """Add or update a product."""

    key = product_key(store, product_name)

    products[key] = {
        "name": product_name,
        "store": store,
        "price": price,
        "url": url
    }

    return products
