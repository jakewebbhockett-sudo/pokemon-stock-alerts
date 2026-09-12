from pokemon_center import get_pokemon_center_products
from smyths import get_smyths_products

from database import (
    load_products,
    save_products,
    is_new_product,
    add_product
)

from scorer import score_product
from alerts import send_telegram_alert


def run_bot():

    print("🤖 Pokémon Stock Alert Bot starting...")

    # Load products we've already seen
    products_database = load_products()

    # Get products from all stores
    products = []

    print("Checking Pokémon Center UK...")
    products.extend(
        get_pokemon_center_products()
    )

    print("Checking Smyths Toys UK...")
    products.extend(
        get_smyths_products()
    )

    print(
        f"Total products found: "
        f"{len(products)}"
    )

    # Go through each discovered product
    for product in products:

        name = product["name"]
        store = product["store"]
        price = product["price"]
        url = product["url"]
        status = product["status"]

        # Only alert if we've never seen it before
        if is_new_product(
            products_database,
            store,
            name
        ):

            # Score product
            score, reasons = score_product(
                product_name=name,
                store=store,
                price=price
            )

            reasons_text = "\n".join(
                f"• {reason}"
                for reason in reasons
            )

            print(
                f"🚨 NEW PRODUCT: "
                f"{name} | "
                f"{store} | "
                f"Score: {score}"
            )

            # Send Telegram alert
            send_telegram_alert(
                product_name=name,
                store=store,
                price=price if price else "Unknown",
                status=status,
                score=score,
                reasons=reasons_text,
                product_url=url
            )

            # Save product
            add_product(
                products_database,
                store,
                name,
                price,
                url
            )

    # Save database
    save_products(products_database)

    print("✅ Check complete!")


if __name__ == "__main__":
    run_bot()
