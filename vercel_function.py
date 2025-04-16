import os
from fastapi import FastAPI
from app.main import app  # Import your FastAPI app from main.py
from uvicorn import Config, Server

def handler(event, context):
    """Handles serverless request"""
    config = Config(app=app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    server = Server(config=config)
    return server.handle(event, context)
