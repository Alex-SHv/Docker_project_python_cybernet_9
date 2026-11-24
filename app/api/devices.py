"""HTTP endpoints for receiving measurements and reading devices."""

from fastapi import APIRouter, HTTPException, status

from app.core.config import INSTANCE_ID
from app.schemas.measurement import (
    DeviceResponse,
    MeasurementAccepted,
    MeasurementIn,
)
from app.services.device_service import (
    get_device,
    list_devices,
    register_or_update_device,
)

router = APIRouter()


@router.post(
    "/data",
    response_model=MeasurementAccepted,
    status_code=status.HTTP_201_CREATED,
    summary="Receive a measurement from a virtual device",
)
def receive_measurement(payload: MeasurementIn) -> MeasurementAccepted:
    """Validate and temporarily store the latest measurement in memory.

    PostgreSQL persistence will be added at the database stage. For now,
    the data remains available while this Python process is running.
    """
    device = register_or_update_device(payload)
    return MeasurementAccepted(
        status="success",
        message="Measurement received and stored in application memory",
        device=device,
        server_instance=INSTANCE_ID,
    )


@router.get(
    "",
    response_model=list[DeviceResponse],
    summary="List registered devices",
)
def read_devices() -> list[DeviceResponse]:
    """Return all devices that have sent at least one measurement."""
    return list_devices()


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Get a device by its identifier",
)
def read_device(device_id: str) -> DeviceResponse:
    """Return the latest known information about one device."""
    device = get_device(device_id)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device '{device_id}' has not sent any measurements",
        )
    return device
