from decimal import Decimal

from pydantic import BaseModel, Field, validator, condecimal


class Item(BaseModel):
    short_description: str = Field(
        ...,
        example="Mountain Dew 12PK",
        pattern=r"^[\w\s\-]+$",
        description="The Short Product Description for the item."
    )
    price: str = Field(
        ...,
        example="6.49",
        pattern=r"^\d+\.\d{2}$",
        description="The total price payed for this item."
    )

    @validator("price", always=True)
    def validate_price(cls, value):
        return Decimal(value)
