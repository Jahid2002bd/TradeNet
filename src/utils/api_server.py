"""
api_server.py

Simple FastAPI server for testing endpoints.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_check() -> dict:
    """
    Returns service status.
    """
    return {"status": "ok"}
