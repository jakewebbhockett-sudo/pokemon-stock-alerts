from pokemon_center import get_pokemon_center_products
from smyths import get_smyths_products
from announcements import get_announcements

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

    # Load previously seen products
    products_database = load_products()

    # =========================
    # CHECK PRODUCTS
    # =========================

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

    # Process products
    for product in products:

        name = product["name"]
        store = product["store"]
        price = product["price"]
        url = product["url"]
        status = product["status"]

        if is_new_product(
            products_database,
            store,
            name
        ):

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
                f"{name}"
            )

            send_telegram_alert(
                product_name=name,
                store=store,
                price=price if price else "Unknown",
                status=status,
                score=score,
                reasons=reasons_text,
                product_url=url
            )

            add_product(
                products_database,
                store,
                name,
                price,
                url
            )

    # =========================
    # CHECK ANNOUNCEMENTS
    # =========================

    announcements = get_announcements()

    print(
        f"Total announcements found: "
        f"{len(announcements)}"
    )

    for announcement in announcements:

        title = announcement["title"]
        store = announcement["store"]
        url = announcement["url"]
        announcement_type = announcement["type"]
        confidence = announcement["confidence"]

        print(
            f"📢 {announcement_type}: "
            f"{title}"
        )

        # Use existing Telegram alert system
        send_telegram_alert(
            product_name=title,
            store=store,
            price="N/A",
            status=(
                f"{announcement_type} | "
                f"{confidence} CONFIDENCE"
            ),
            score="NEW",
            reasons=(
                "Official Pokémon news or "
                "announcement detected"
            ),
            product_url=url
        )

    # Save database
    save_products(products_database)

    print("✅ Check complete!")


if __name__ == "__main__":
    run_bot()
