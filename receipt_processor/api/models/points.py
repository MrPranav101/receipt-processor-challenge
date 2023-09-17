from decimal import Decimal

from pydantic import BaseModel, Field, validator


class Points(BaseModel):
    points: int = Field(
        ...,
        example=100,
        description="The number of points awarded"
    )
