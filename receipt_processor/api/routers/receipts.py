from fastapi import APIRouter, Depends, Request

from receipt_processor.api.models import receipt, points
from receipt_processor.api.utils.headers import optional_headers
from receipt_processor.api.utils.errors import server_error, user_error
from receipt_processor.service.processor import ReceiptProcessor
from receipt_processor.db.crud.points import get_points_sum


router = APIRouter(
    prefix="/receipts",
    tags=["Main"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(optional_headers)]
)


@router.post(
    "/process",
    description="Submits a receipt for processing",
    response_model=receipt.ReceiptResponse,
)
async def process(request: Request, receipt_obj: receipt.Receipt):
    try:
        print(receipt_obj)
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
)
async def result(request: Request, id: str):
    try:
        return {'points': await get_points_sum(id)}
    except ValueError as e:
        request.app.state.logger.error(f'An error occurred while trying to pull the results for task_id {id}, error: {e}')
        return user_error(
            status_code=404,
            message=f'No receipt found by: {id}'
        )
    except Exception as e:
        request.app.state.logger.error(f'An error occurred while trying to pull the results for task_id {id}, error: {e}')
        return server_error(
            message=f'Unable to get the results of id: {id}'
        )
