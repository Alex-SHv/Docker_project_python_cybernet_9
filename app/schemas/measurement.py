"""Pydantic schemas for measurements and device API responses."""

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MeasurementIn(BaseModel):
    """Measurement payload sent by Device Simulator."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    device_id: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$",
        examples=["SENSOR-001"],
    )
    type: str = Field(min_length=1, max_length=50, examples=["temperature"])
    location: str = Field(min_length=1, max_length=100, examples=["Sector-A"])
    value: float = Field(allow_inf_nan=False, examples=[42.5])
    unit: str = Field(min_length=1, max_length=20, examples=["C"])
    status: Literal["active", "inactive", "off", "maintenance"] = "active"
    measured_at: datetime

    @field_validator("measured_at")
    @classmethod
    def measured_at_must_include_timezone(cls, value: datetime) -> datetime:
        """Require an explicit timezone and normalize timestamps to UTC."""
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("measured_at must include a timezone, for example Z")
        return value.astimezone(timezone.utc)


class DeviceResponse(BaseModel):
    """Latest known state of a device held by this service instance."""

    device_id: str
    type: str
    location: str
    value: float
    unit: str
    status: str
    measured_at: datetime
    last_updated: datetime


class MeasurementAccepted(BaseModel):
    """Response returned after a measurement has been accepted."""

    status: Literal["success"]
    message: str
    device: DeviceResponse
    server_instance: str
