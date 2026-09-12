from pokemon_center import get_pokemon_center_products
from smyths import get_smyths_products
from announcements import get_announcements

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

        # Get previous stock status
        old_status = get_product_status(
            products_database,
            store,
            name
        )

        # Only alert when stock changes
        # from NOT AVAILABLE to AVAILABLE
        if should_alert(
            old_status,
            status
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
                f"🚨 RESTOCK ALERT: "
                f"{name} | {store}"
            )

            send_telegram_alert(
                product_name=name,
                store=store,
                price=price if price else "Unknown",
                status="🟢 IN STOCK NOW",
                score=score,
                reasons=reasons_text,
                product_url=url
            )

        # Always save latest status
        add_product(
            products_database,
            store,
            name,
            price,
            url,
            status
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

        send_telegram_alert(
            product_name=title,
            store=store,
            price="N/A",
            status=(
                f"📢 {announcement_type} | "
                f"{confidence} CONFIDENCE"
            ),
            score="NEWS",
            reasons=(
                f"Source: "
                f"{announcement['source']}"
            ),
            product_url=url
        )

    # Save everything
    save_products(
        products_database
    )

    print("✅ Check complete!")


if __name__ == "__main__":
    run_bot()
