from fastapi.testclient import TestClient

from receipt_processor.api.app import app
from receipt_processor.api.utils.json import read_json_file


def test_receipt_success():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file("receipt_processor/test/data/request/accepted.json"),
        )
        response_json = response.json()
        assert response.status_code == 200
        assert isinstance(response_json["id"], str)


def test_receipt_retailer_failed():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file("receipt_processor/test/data/request/retailer_regex_failed.json"),
        )
        response_json = response.json()
        assert response.status_code == 400
        assert response_json == read_json_file(
            "receipt_processor/test/data/response/retailer_regex_failed.json"
        )


def test_purchase_date_failed():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file("receipt_processor/test/data/request/purchaseDate_failed.json"),
        )
        response_json = response.json()
        assert response.status_code == 400
        assert response_json == read_json_file(
            "receipt_processor/test/data/response/purchaseDate_failed.json"
        )


def test_purchase_time_failed():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file("receipt_processor/test/data/request/purchaseTime_failed.json"),
        )
        response_json = response.json()
        assert response.status_code == 400
        assert response_json == read_json_file(
            "receipt_processor/test/data/response/purchaseTime_failed.json"
        )


def test_total_failed():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file("receipt_processor/test/data/request/total_failed.json"),
        )
        response_json = response.json()
        assert response.status_code == 400
        assert response_json == read_json_file(
            "receipt_processor/test/data/response/total_failed.json"
        )


def test_items_short_description_failed():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file(
                "receipt_processor/test/data/request/items_shortDescription_failed.json"
            ),
        )
        response_json = response.json()
        assert response.status_code == 400
        assert response_json == read_json_file(
            "receipt_processor/test/data/response/items_shortDescription_failed.json"
        )


def test_items_price_failed():
    with TestClient(app) as client:
        response = client.post(
            "/receipts/process",
            headers={"x-request-id": "52a5fb55-a58e-4977-bd10-ddb3da1bc45b"},
            json=read_json_file(
                "receipt_processor/test/data/request/items_price_failed.json"
            ),
        )
        response_json = response.json()
        assert response.status_code == 400
        assert response_json == read_json_file(
            "receipt_processor/test/data/response/items_price_failed.json"
        )
