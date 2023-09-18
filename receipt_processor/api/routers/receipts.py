from fastapi import APIRouter, Depends, Request

from receipt_processor.api.models import receipt, points
from receipt_processor.api.utils.json import read_json_file
from receipt_processor.api.utils.headers import optional_headers
from receipt_processor.api.utils.errors import server_error, user_error
from receipt_processor.service.processor import ReceiptProcessor
from receipt_processor.db.crud.points import get_points_sum


router = APIRouter(
    prefix="/receipts",
    tags=["default"],
    dependencies=[Depends(optional_headers)]
)


@router.post(
    "/process",
    description="Submits a receipt for processing",
    response_model=receipt.ReceiptResponse,
    responses={400: {
        "description": "Bad Request",
        "content": {
                "application/json": {
                    "example": read_json_file(
                        'receipt_processor/api/data/receipt/bad_request.json'
                    )
                }
        }
    }},
)
async def process(request: Request, receipt_obj: receipt.Receipt):
    try:
        id = await ReceiptProcessor(receipt_obj).process()
        return {
            "id": id
        }
    except Exception as e:
        request.app.state.logger.exception(f"logging exception: {e}")
        return server_error(
            message="Server Error"
        )


@router.get(
    "/{id}/points",
    description="Returns the points awarded for the receipt",
    summary="Returns the points awarded for the receipt",
    response_model=points.Points,
    responses={404: {
        "description": "Receipt id Not Found",
        "content": {
                "application/json": {
                    "example": {
                        "message": "No receipt ID: adb6b560-0eef-42bc-9d16-df48f30e89b2"
                    }
                }
        }
    }}
)
async def result(request: Request, id: str):
    try:
        return {'points': await get_points_sum(id)}
    except ValueError as e:
        request.app.state.logger.error('An error occurred while trying'
                                       f' to pull the results for task_id {id}, error: {e}')
        return user_error(
            status_code=404,
            message=f'No receipt ID: {id}'
        )
    except Exception as e:
        request.app.state.logger.error('An error occurred while trying'
                                       f' to pull the results for task_id {id}, error: {e}')
        return server_error(
            message=f'Unable to get the results of id: {id}'
        )
