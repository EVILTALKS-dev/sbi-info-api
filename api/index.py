from fastapi import FastAPI, HTTPException, Request
import json
import os

app = FastAPI(
    title="SBI Info API",
    description="Admin: t.me/EVILTALKS"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# This list will hold EVERYTHING from the JSON files
ALL_RECORDS = []

def load_data():
    global ALL_RECORDS
    ALL_RECORDS.clear()
    
    if not os.path.exists(DATA_DIR):
        print("Error: data folder not found")
        return

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        ALL_RECORDS.extend(data)
                    elif isinstance(data, dict):
                        ALL_RECORDS.append(data)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

# Load data immediately when server starts
load_data()

@app.get("/")
def home():
    return {
        "status": "online",
        "admin": "t.me/EVILTALKS",
        "total_records_in_memory": len(ALL_RECORDS),
        "usage": "Go to /api/search?q=YOUR_QUERY"
    }

@app.get("/api/search")
def search_data(q: str):
    """
    Search any value (email, phone, name, password, id) across all JSON files.
    Returns ONLY the normal data (strips out database activity logs).
    """
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    
    query = q.lower()
    results = []
    
    for record in ALL_RECORDS:
        # Convert the entire record dict into a string to search everywhere
        record_string = json.dumps(record).lower()
        
        if query in record_string:
            # 🚨 CLEAN THE DATA: Remove nested database logs and tables
            clean_record = {}
            for k, v in record.items():
                # Skip massive history logs
                if k in ["database", "tables", "activity", "bpsi_pos_uat"]:
                    continue
                
                # Only keep normal text, numbers, and standard fields
                if isinstance(v, (str, int, float, bool, type(None))):
                    clean_record[k] = v
            
            results.append(clean_record)
            
            # Limit to 100 results so the API doesn't crash
            if len(results) >= 100:
                break
                
    return {
        "admin": "t.me/EVILTALKS",
        "query": q,
        "total_found": len(results),
        "data": results
    }

@app.get("/api/record/{record_id}")
def get_record_by_id(record_id: str):
    """
    Get a specific record by its exact 'id' field.
    Also cleans out the massive history logs.
    """
    for record in ALL_RECORDS:
        if str(record.get("id")) == str(record_id):
            clean_record = {}
            for k, v in record.items():
                if k in ["database", "tables", "activity", "bpsi_pos_uat"]:
                    continue
                if isinstance(v, (str, int, float, bool, type(None))):
                    clean_record[k] = v
                    
            return {
                "admin": "t.me/EVILTALKS",
                "data": clean_record
            }
    
    raise HTTPException(status_code=404, detail="Record ID not found")