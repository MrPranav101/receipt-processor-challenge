import json

from fastapi import APIRouter, Depends, Request

from receipt_processor.api.models import receipt, points
from receipt_processor.api.utils.headers import optional_headers
from receipt_processor.api.utils.errors import server_error


router = APIRouter(
    prefix="/receipts",
    tags=["Main"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(optional_headers)]
)


@router.post(
    "/process",
    description="Starts a celery task",
    response_model=receipt.ReceiptResponse,
)
async def process(request: Request, receipt_obj: receipt.Receipt):
    try:
        pass
    except Exception as e:
        request.app.state.logger.info(f"logging exception: {e}")
        return server_error(
            f"Failed to take in parmeters \n{json.dumps(receipt_obj.__dict__, indent=4)}"
        )


@router.get(
    "/{id}/points",
    description="This is a description",
    summary="this is a summary",
    response_model=points.Points,
)
def result(request: Request, id: str):
    try:
        pass

    except Exception as e:
        request.app.state.logger.error(f'An error occurred while trying to pull the results for task_id {id}, error: {e}')
        return server_error(
            message=f'Unable to get the results of id: {id}'
        )
