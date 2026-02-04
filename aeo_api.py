from fastapi import FastAPI
from pydantic import BaseModel
from aeo_analyzer import analyze_aeo
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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

@app.post("/audit")
def run_audit(request: AuditRequest):
    """
    Audit the given URL for AEO readiness.
    """
    print(f"🔎 Auditing URL: {request.url}")
    result = analyze_aeo(request.url)
    return result

@app.get("/")
def health_check():
    return {"status": "AEO Auditor Ready! 🫡"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
