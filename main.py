from pokemon_center import get_pokemon_center_products
from database import (
    load_products,
    save_products,
    is_new_product,
    add_product
)
from scorer import score_product
from alerts import send_telegram_alert


def run_bot():

    print("🤖 Pokémon Alert Bot starting...")

    # Load products we've already seen
    products_database = load_products()

    # Check Pokémon Center UK
    products = get_pokemon_center_products()

    print(f"Found {len(products)} products")

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

            # Score the product
            score, reasons = score_product(
                product_name=name,
                store=store,
                price=price
            )

            # Format reasons nicely
            reasons_text = "\n".join(
                f"• {reason}"
                for reason in reasons
            )

            print(
                f"NEW PRODUCT: "
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

            # Save it so we don't alert again
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
