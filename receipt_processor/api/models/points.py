from pydantic import BaseModel, Field


class Points(BaseModel):
    points: int = Field(
        ...,
        example=100,
        description="The number of points awarded"
    )
