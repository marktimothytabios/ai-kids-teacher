"""ASGI entry point: ``uvicorn webapp.main:app`` (used by ``python -m webapp --reload``)."""
import os

from .app import create_app

app = create_app(warm=os.environ.get("LITTLE_WHYS_WARM", "1") == "1")
