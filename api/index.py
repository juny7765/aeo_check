from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# Since Vercel runs this file, and aeo_analyzer is in the same dir
from .aeo_analyzer import analyze_aeo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditRequest(BaseModel):
    url: str

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/audit")
def run_audit(request: AuditRequest):
    result = analyze_aeo(request.url)
    return result
