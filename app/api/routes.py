"""
API route definitions for PulseAPI.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    """
    Health check endpoint.

    Returns a simple status to confirm the API is running.
    Used by monitoring tools, load balancers, or just you,
    to verify the service is alive.
    """
    return {"status": "ok"}