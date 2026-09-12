def is_in_stock(status):
    """
    Return True only when a product
    is genuinely available to buy.
    """

    if not status:
        return False

    status = str(status).lower()

    in_stock_words = [
        "in stock",
        "available",
        "add to basket",
        "buy now"
    ]

    out_of_stock_words = [
        "out of stock",
        "sold out",
        "unavailable",
        "coming soon"
    ]

    # Explicitly reject sold-out products
    if any(
        word in status
        for word in out_of_stock_words
    ):
        return False

    return any(
        word in status
        for word in in_stock_words
    )


def should_alert(old_status, new_status):
    """
    Alert only when something changes
    from NOT IN STOCK to IN STOCK.
    """

    was_in_stock = is_in_stock(
        old_status
    )

    is_now_in_stock = is_in_stock(
        new_status
    )

    return (
        not was_in_stock
        and is_now_in_stock
    )
