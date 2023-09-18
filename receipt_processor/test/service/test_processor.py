from receipt_processor.service.processor import ReceiptProcessor
from receipt_processor.test.service.receipt_objects import get_valid_receipt
from decimal import Decimal
from datetime import time, date


def test_points_retailer_name():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_retailer_name() == 7


def test_points_round_dollar_round():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_round_dollar() == 50


def test_points_round_dollar_not_round():
    valid_receipt = get_valid_receipt()
    valid_receipt.total = Decimal('2.01')
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_round_dollar() == 0


def test_points_multiple_25():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_multiple_25() == 25


def test_points_line_items_len_3():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_line_items_len() == 5


def test_points_line_items_len_1():
    valid_receipt = get_valid_receipt()
    valid_receipt.items.pop()
    valid_receipt.items.pop()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_line_items_len() == 0


def test_points_description():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    items = valid_receipt.items
    assert receipt.points_description(items[0].short_description, items[0].price) == 0
    assert receipt.points_description(items[1].short_description, items[1].price) == 0
    assert receipt.points_description(items[2].short_description, items[2].price) == 0


def test_points_description_not_multiple():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_description("Walmart", Decimal('1.0')) == 0


def test_points_description_multiple_round_down():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_description("Walmar", Decimal('1.0')) == 0


def test_points_description_multiple_round_up():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_description("Walmar", Decimal('3.0')) == 1


def test_points_description_trim_multiple_round_up():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_description("  Walm r  ", Decimal('3.0')) == 1


def test_points_time_purchased_between():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_time_purchased() == 10


def test_points_time_purchased_before():
    valid_receipt = get_valid_receipt()
    valid_receipt.purchase_time = time(13, 59)
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_time_purchased() == 0


def test_points_time_purchased_after():
    valid_receipt = get_valid_receipt()
    valid_receipt.purchase_time = time(16, 1)
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_time_purchased() == 0


def test_points_time_purchased_equal_2pm():
    valid_receipt = get_valid_receipt()
    valid_receipt.purchase_time = time(14, 0)
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_time_purchased() == 0


def test_points_time_purchased_equal_4pm():
    valid_receipt = get_valid_receipt()
    valid_receipt.purchase_time = time(16, 0)
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_time_purchased() == 0


def test_points_day_purchased_odd():
    valid_receipt = get_valid_receipt()
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_day_purchased() == 6


def test_points_day_purchased_even():
    valid_receipt = get_valid_receipt()
    valid_receipt.purchase_date = date(2021, 1, 2)
    receipt = ReceiptProcessor(valid_receipt)
    assert receipt.points_day_purchased() == 0
