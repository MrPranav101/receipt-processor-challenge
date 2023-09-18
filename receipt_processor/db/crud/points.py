from sqlalchemy import select

from receipt_processor.db import get_db_session
from receipt_processor.db.models.receipt_points import Points


async def get_points_sum(id: str) -> int:
    async with get_db_session() as session:
        stmt = select(Points).where(Points.id == id)
        result = await session.execute(stmt)
        record = result.scalars().first()
        if not record:
            raise ValueError(f'No record found for id: {id}')
        return sum(
            [
                record.retailer_name_points,
                record.round_dollar_points,
                record.multiple_25_points,
                record.line_items_len_points,
                record.all_description_points,
                record.day_purchased_points,
                record.time_purchased_points
            ]
        )


async def save_points(points: Points) -> str:
    async with get_db_session() as session:
        session.add(points)
        await session.commit()
        await session.refresh(points)
        return points.id
