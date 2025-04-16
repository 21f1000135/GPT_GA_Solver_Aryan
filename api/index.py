from fastapi import FastAPI
from mangum import Mangum
from app.main import app  # Import your FastAPI app

handler = Mangum(app)
