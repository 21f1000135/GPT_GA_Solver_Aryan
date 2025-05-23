from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional
from dotenv import load_dotenv  # Load environment variables

from app.utils.openai_client import get_openai_response
from app.utils.file_handler import save_upload_file_temporarily

# Load environment variables from .env file (if present)
load_dotenv()

app = FastAPI(title="IITM Assignment API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API proxy token from environment
API_PROXY_TOKEN = os.getenv("API_PROXY_TOKEN")

# Dependency to verify token
def verify_token(token: str = Form(...)):
    print("Incoming TOKEN:", repr(token))
    if token != API_PROXY_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Token")
    return token

@app.post("/api/")
async def process_question(
    token: str = Depends(verify_token),  # Ensure token is verified
    question: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        # Save file temporarily if provided
        temp_file_path = None
        if file:
            temp_file_path = await save_upload_file_temporarily(file)
        
        # Get answer from OpenAI
        answer = await get_openai_response(question, temp_file_path)
        
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
