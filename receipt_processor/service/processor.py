import datetime
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from receipt_processor.api.models.receipt import Receipt
from receipt_processor.db.models.receipt_points import Points
from receipt_processor.db.crud.points import save_points


class ReceiptProcessor:
    def __init__(self, receipt: Receipt):
        self.receipt = receipt
        self.db_obj = None

    def points_retailer_name(self) -> int:
        """One point for every alphanumeric character in the retailer name."""
        retailer_name = self.receipt.retailer
        points = 0
        for char in retailer_name:
            if char.isalnum():
                points += 1
        return points

    def points_round_dollar(self) -> int:
        """50 points if the total is a round dollar amount with no cents."""
        total = self.receipt.total
        normalized_value = total.normalize()
        decimal_part = normalized_value % 1
        return 50 if decimal_part == 0 else 0

    def points_multiple_25(self):
        """25 points if the total is a multiple of 0.25"""
        total = self.receipt.total
        remainder = total % Decimal('0.25')
        return 25 if remainder == 0 else 0

    def points_line_items_len(self):
        """5 points for every two items on the receipt."""
        return 5 * (len(self.receipt.items) // 2)

    def points_description(self, description: str, price: Decimal):
        """
        If the trimmed length of the item description
        is a multiple of 3, multiply the price by 0.2
        and round up to the nearest integer. The result
        is the number of points earned.
        """
        trimmed_description = description.strip()
        trimmed_description_len = len(trimmed_description)
        if trimmed_description_len % 3 == 0:
            product = Decimal('0.2') * price
            return int(Decimal(product).to_integral_value(rounding=ROUND_HALF_UP))
        return 0

    def points_all_descriptions(self):
        points = 0
        for item in self.receipt.items:
            points += self.points_description(item.short_description, item.price)
        return points

    def points_day_purchased(self):
        """6 points if the day in the purchase date is odd."""
        purchase_date = self.receipt.purchase_date
        return 6 if purchase_date.day % 2 == 1 else 0

    def points_time_purchased(self):
        """10 points if the time of purchase is after 2:00pm and before 4:00pm."""
        purchase_time = self.receipt.purchase_time
        time_2_pm = datetime.time(14, 0)
        time_4_pm = datetime.time(16, 0)
        return 10 if time_2_pm < purchase_time < time_4_pm else 0

    def create_db_obj(self) -> str:
        id_ = str(uuid4())
        self.db_obj = Points(
            id=id_,
            retailer_name_points=self.points_retailer_name(),
            round_dollar_points=self.points_round_dollar(),
            multiple_25_points=self.points_multiple_25(),
            line_items_len_points=self.points_line_items_len(),
            all_description_points=self.points_all_descriptions(),
            day_purchased_points=self.points_day_purchased(),
            time_purchased_points=self.points_time_purchased(),
        )

    async def process(self) -> str:
        self.create_db_obj()
        return await save_points(self.db_obj)
