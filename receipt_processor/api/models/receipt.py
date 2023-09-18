from datetime import date, time
from decimal import Decimal, InvalidOperation
from typing import List

from pydantic import BaseModel, Field, validator

from receipt_processor.api.models.item import Item


class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        json_schema_extra={"example": "Target"},
        pattern=r"^\S+$",
        description="The name of the retailer or store the receipt is from."
    )
    purchase_date: date = Field(
        ...,
        json_schema_extra={"example": "2021-01-01"},
        alias="purchaseDate",
        description="The date of the purchase printed on the receipt.",
    )
    purchase_time: time = Field(
        ...,
        json_schema_extra={"example": "12:00"},
        alias="purchaseTime",
        description="The time of the purchase printed on the receipt. 24-hour time expected.",
    )
    items: List[Item] = Field(
        ...,
        json_schema_extra={"example": [Item(shortDescription="Mountain Dew 12PK", price="6.49")]},
        description="A list of items purchased on the receipt."
    )
    total: str = Field(
        ...,
        json_schema_extra={"example": "6.49"},
        pattern=r"^\d+\.\d{2}$",
        description="The total price payed for this receipt."
    )

    @validator("total", always=True)
    def string_to_decimal(cls, value):
        try:
            return Decimal(value)
        except InvalidOperation:
            raise ValueError('Invalid decimal value')


class ReceiptResponse(BaseModel):
    id: str = Field(
        ...,
        json_schema_extra={"example": "adb6b560-0eef-42bc-9d16-df48f30e89b2"},
        description="The UUID of the receipt."
    )
