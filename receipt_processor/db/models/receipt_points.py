from sqlalchemy import Column, Integer, String
from receipt_processor.db import Base


class Points(Base):
    __tablename__ = 'points'
    id = Column(String(100), primary_key=True, index=True)
    retailer_name_points = Column(Integer, nullable=True)
    round_dollar_points = Column(Integer, nullable=True)
    multiple_25_points = Column(Integer, nullable=True)
    line_items_len_points = Column(Integer, nullable=True)
    all_description_points = Column(Integer, nullable=True)
    day_purchased_points = Column(Integer, nullable=True)
    time_purchased_points = Column(Integer, nullable=True)
