from pydantic import BaseModel, Field


class Points(BaseModel):
    points: int = Field(
        ...,
        json_schema_extra={"example": 100},
        description="The number of points awarded"
    )
