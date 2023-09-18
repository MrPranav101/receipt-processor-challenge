from receipt_processor.api.models.receipt import Receipt
from receipt_processor.api.models.item import Item


def get_valid_receipt():
    valid_receipt = Receipt(
        retailer="Walmart",
        purchaseDate="2021-01-01",
        purchaseTime="15:00",
        total="2.00",
        items=[
            Item(
                price="1.00",
                shortDescription="Item 1",
            ),
            Item(
                price="1.00",
                shortDescription="Item 2",
            ),
            Item(
                price="1.00",
                shortDescription="Item 3",
            )
        ]
    )
    return valid_receipt
