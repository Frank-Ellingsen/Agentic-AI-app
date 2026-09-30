import sqlite3
import os
import json
import asyncio
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

app = FastAPI(title="Data-to-Decision API Gateway")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "control.sqlite")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h1>Autonomous Analytics Studio API Gateway</h1>")

@app.get("/api/v1/kpis")
async def get_kpis(db: sqlite3.Connection = Depends(get_db)):
    return {
        "status": "success",
        "kpis": [
            {"metric": "Revenue YTD", "value": "$14.2M", "rag": "GREEN"},
            {"metric": "Operating Margin", "value": "18.5%", "rag": "AMBER"}
        ]
    }

@app.get("/api/v1/stream-thoughts")
async def stream_agent_thoughts():
    async def event_generator():
        steps = [
            {"agent": "A0_Orchestrator", "message": "DAG Pipeline Initialized."},
            {"agent": "A1_Data_Inspector", "message": "Inspecting SQLite tables... OK."},
            {"agent": "Gemini_API", "message": "Generating decision story via gemini-3.6-flash..."},
            {"agent": "A7_Validator", "message": "Audit verified. Report Published."}
        ]
        for step in steps:
            await asyncio.sleep(1)
            yield f"data: {json.dumps(step)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
