from fastapi import FastAPI
from pydantic import BaseModel
from marketing_agent import generate_proposal
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow CORS for development (Expo web/emulator)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProposalRequest(BaseModel):
    name: str
    target: str
    benefit: str

@app.post("/generate")
def create_proposal(request: ProposalRequest):
    """
    Generate a formatted marketing proposal using the underlying agent logic.
    """
    print(f"😎 Incoming Request: {request}")
    proposal = generate_proposal(request.name, request.target, request.benefit)
    return {"result": proposal}

@app.get("/")
def health_check():
    return {"status": "Kim Dae-ri is ready! 🫡"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
