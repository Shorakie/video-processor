from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

router = APIRouter(default_response_class=JSONResponse, prefix="/api")


# Api Healthcheck
class HealthCheckResponse(BaseModel):
    status: Literal["ok"] = "ok"


@router.get("/healthcheck", tags=["monitoring"])
def healthcheck() -> HealthCheckResponse:
    """Simple healthcheck endpoint."""
    return HealthCheckResponse()
