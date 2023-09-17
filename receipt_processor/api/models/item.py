from decimal import Decimal, InvalidOperation

from pydantic import BaseModel, Field, validator


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

    @validator('price', always=True)
    def string_to_decimal(cls, value):
        try:
            return Decimal(value)
        except InvalidOperation:
            raise ValueError('Invalid decimal value')

    class Config:
        frozen = True
