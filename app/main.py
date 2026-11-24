"""FastAPI application entry point for CyberNet Device Service."""

from fastapi import FastAPI

from app.api.devices import router as devices_router
from app.core.config import INSTANCE_ID, SERVICE_NAME

app = FastAPI(
    title=SERVICE_NAME,
    description=(
        "Receives measurements from the CyberNet Device Simulator. "
        "At Stage 2, the latest device states are kept in process memory."
    ),
    version="0.2.0",
)

app.include_router(
    devices_router,
    prefix="/api/devices",
    tags=["Devices"],
)


@app.get("/api/health", tags=["Health"], summary="Check service health")
def health_check() -> dict[str, str]:
    """Return a simple health response and this server's instance ID."""
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "server_instance": INSTANCE_ID,
    }


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    """Provide a convenient landing response with a link to API docs."""
    return {
        "service": SERVICE_NAME,
        "message": "CyberNet Device Service is running",
        "docs": "/docs",
    }
