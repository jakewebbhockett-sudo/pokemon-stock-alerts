from pokemon_center import get_pokemon_center_products
from smyths import get_smyths_products

from database import (
    load_products,
    save_products,
    get_product_status,
    add_product
)

from stock_monitor import should_alert
from scorer import score_product
from alerts import send_telegram_alert


def run_bot():

    print("🤖 Pokémon Stock Alert Bot starting...")

    # Load previously saved products
    products_database = load_products()

    # =========================
    # CHECK PRODUCTS
    # =========================

    products = []

    print("Checking Pokémon Center UK...")

    try:
        products.extend(
            get_pokemon_center_products()
        )

    except Exception as error:

        print(
            "Pokémon Center check error:",
            error
        )

    print("Checking Smyths Toys UK...")

    try:
        products.extend(
            get_smyths_products()
        )

    except Exception as error:

        print(
            "Smyths check error:",
            error
        )

    print(
        f"Total products found: "
        f"{len(products)}"
    )

    # =========================
    # CHECK STOCK CHANGES
    # =========================

    for product in products:

        name = product.get("name")
        store = product.get("store")
        price = product.get("price")
        url = product.get("url")
        status = product.get("status")

        # Skip incomplete products
        if not name or not store:
            continue

        # Get previously saved status
        old_status = get_product_status(
            products_database,
            store,
            name
        )

        print(
            f"Checking: {name} | "
            f"Old: {old_status} | "
            f"New: {status}"
        )

        # Alert ONLY when:
        # NOT IN STOCK -> IN STOCK
        if should_alert(
            old_status,
            status
        ):

            print(
                f"🚨 RESTOCK ALERT: "
                f"{name} | {store}"
            )

            try:

                score, reasons = score_product(
                    product_name=name,
                    store=store,
                    price=price
                )

                reasons_text = "\n".join(
                    f"• {reason}"
                    for reason in reasons
                )

            except Exception as error:

                print(
                    "Scoring error:",
                    error
                )

                score = "N/A"
                reasons_text = (
                    "Product is back in stock"
                )

            # SEND TELEGRAM ALERT
            send_telegram_alert(
                product_name=name,
                store=store,
                price=(
                    price
                    if price
                    else "Unknown"
                ),
                status="🟢 IN STOCK NOW",
                score=score,
                reasons=reasons_text,
                product_url=url
            )

        # Always save the latest product status
        add_product(
            products_database,
            store,
            name,
            price,
            url,
            status
        )

    # =========================
    # SAVE DATABASE
    # =========================

    save_products(
        products_database
    )

    print("✅ Stock check complete!")


if __name__ == "__main__":
    run_bot()
