"""
PulseAPI entry point.

This file creates the FastAPI application instance and includes
all the API routes defined elsewhere in the app.
"""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="PulseAPI",
    description="A machine learning model-serving API",
    version="1.0.0",
)

app.include_router(router)