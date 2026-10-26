from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
import time

app = FastAPI(
    title="SBI Data API",
    description="Powered by Admin: t.me/EVILTALKS",
    version="1.0"
)

# Get the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Global memory storage
agents = []
stages = []
main_data = []

def load_data():
    global agents, stages, main_data
    agents.clear()
    stages.clear()
    main_data.clear()

    if not os.path.exists(DATA_DIR):
        print("Data directory not found!")
        return

    # Load all json files in the data folder
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not data:
                        continue
                        
                    # Categorize based on keys present in the first item
                    if "stage" in str(data[0]):
                        stages.extend(data)
                    elif "agent_id" in str(data[0]):
                        agents.extend(data)
                    else:
                        main_data.extend(data)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

# Load data on server startup
load_data()

# Middleware for Branding Headers
@app.middleware("http")
async def add_branding_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Admin"] = "t.me/EVILTALKS"
    response.headers["X-Powered-By"] = "EVILTALKS SBI API"
    return response

@app.get("/")
def home():
    return {
        "status": "online",
        "admin": "t.me/EVILTALKS",
        "message": "Welcome to the SBI Data API",
        "loaded_records": {
            "agents": len(agents),
            "stages": len(stages),
            "main_data": len(main_data)
        },
        "endpoints": [
            "/api/agents/{phone}",
            "/api/stages",
            "/api/search?q={query}"
        ]
    }

@app.get("/api/agents/{phone}")
def get_agent_by_phone(phone: str):
    """Finds an agent by their mobile number (from sbi2.json)."""
    results = [a for a in agents if str(a.get("moblie_no")) == phone]
    if not results:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"admin": "t.me/EVILTALKS", "results": results}

@app.get("/api/stages")
def get_stages():
    """Returns all stages (from sbi4.json)."""
    return {"admin": "t.me/EVILTALKS", "stages": stages}

@app.get("/api/stages/{stage_id}")
def get_stage_by_id(stage_id: int):
    """Find a stage by its ID."""
    for s in stages:
        if s.get("id") == stage_id:
            return {"admin": "t.me/EVILTALKS", "result": s}
    raise HTTPException(status_code=404, detail="Stage not found")

@app.get("/api/search")
def search_main_data(q: str):
    """
    Search the massive dataset. 
    Matches any field containing the query (phone, email, name, user_id, etc.)
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query required")
    
    query = q.lower()
    results = []
    
    for record in main_data:
        # Convert record values to a single string for fuzzy searching
        record_str = " ".join(str(v) for v in record.values()).lower()
        if query in record_str:
            results.append(record)
            if len(results) >= 50: # Limit to 50 results per search
                break
                
    return {
        "admin": "t.me/EVILTALKS",
        "query": q, 
        "count": len(results), 
        "results": results
    }