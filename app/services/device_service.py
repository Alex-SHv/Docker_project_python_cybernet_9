"""In-memory device registry for Stage 2.

This module deliberately uses process memory instead of PostgreSQL.
The database integration is planned for the next development stage.
"""

from datetime import datetime, timezone
from threading import RLock

from app.schemas.measurement import DeviceResponse, MeasurementIn

# Key: device_id; value: latest accepted device state.
_devices: dict[str, dict] = {}
_devices_lock = RLock()


def register_or_update_device(measurement: MeasurementIn) -> DeviceResponse:
    """Create a device on first contact or update its latest measurement."""
    received_at = datetime.now(timezone.utc)
    record = measurement.model_dump()
    record["last_updated"] = received_at

    with _devices_lock:
        _devices[measurement.device_id] = record
        # Return a separate validated object, not the internal dictionary.
        return DeviceResponse.model_validate(record)


def list_devices() -> list[DeviceResponse]:
    """Return all known devices in identifier order."""
    with _devices_lock:
        records = [dict(item) for item in _devices.values()]

    records.sort(key=lambda item: item["device_id"])
    return [DeviceResponse.model_validate(item) for item in records]


def get_device(device_id: str) -> DeviceResponse | None:
    """Return one device, or None if it has not sent data yet."""
    with _devices_lock:
        record = _devices.get(device_id)
        if record is None:
            return None
        snapshot = dict(record)

    return DeviceResponse.model_validate(snapshot)


def clear_devices() -> None:
    """Clear the in-memory registry. Intended for automated tests only."""
    with _devices_lock:
        _devices.clear()
