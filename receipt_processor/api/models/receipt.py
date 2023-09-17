from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator
from decimal import Decimal

from receipt_processor.api.models.item import Item


class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        example="Target",
        pattern=r"^\S+$",
        description="The name of the retailer or store the receipt is from."
    )
    puchase_date: str = Field(
        ...,
        example="2021-01-01",
        alias="purchaseDate",
        description="The date of the purchase printed on the receipt.",
    )
    purchase_time: str = Field(
        ...,
        example="12:00:00",
        alias="purchaseTime",
        pattern=r'^([01]\d|2[0-3]):([0-5]\d)$',
        description="The time of the purchase printed on the receipt. 24-hour time expected.",
    )
    items: List[Item] = Field(
        ...,
        example=[Item(short_description="Mountain Dew 12PK", price="6.49")],
        description="A list of items purchased on the receipt."
    )
    total: str = Field(
        ...,
        example="6.49",
        pattern=r"^\d+\.\d{2}$",
        description="The total price payed for this receipt."
    )

    @validator("puchase_date", pre=True, always=True)
    def parse_purchase_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    @validator("purchase_time", pre=True, always=True)
    def parse_purchase_time(cls, value):
        return datetime.strptime(
            value,
            "%H:%M"
        ).time()

    @validator("total", pre=True, always=True)
    def validate_total(cls, value):
        return Decimal(value)


class ReceiptResponse(BaseModel):
    id: str = Field(
        ...,
        example="adb6b560-0eef-42bc-9d16-df48f30e89b2",
        description="The UUID of the receipt."
    )
