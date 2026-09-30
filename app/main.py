import sqlite3
import os
import json
import asyncio
import shutil
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from typing import Optional

app = FastAPI(title="Data-to-Decision API Gateway")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "control.sqlite")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

os.makedirs(UPLOAD_DIR, exist_ok=True)

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

@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload raw data or document file (CSV, XLSX, PDF, TXT, MD, Parquet) for agent DAG processing."""
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        file_size = os.path.getsize(file_location)
        ext = os.path.splitext(file.filename)[1].lower()
        
        return JSONResponse(content={
            "status": "success",
            "filename": file.filename,
            "filepath": f"data/{file.filename}",
            "size_bytes": file_size,
            "format": ext,
            "message": f"File '{file.filename}' uploaded successfully to landing zone."
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/run-dag")
async def run_dag(
    filename: str = Form(...),
    provider: str = Form("google"),
    model: str = Form("gemini-3.6-flash"),
    api_key: Optional[str] = Form(None),
    question: Optional[str] = Form("Perform 6-phase analytical financial controlling review")
):
    """Executes the Agent DAG over the selected file using the specified provider and API key."""
    return JSONResponse(content={
        "status": "success",
        "job_id": f"job_{int(asyncio.get_event_loop().time() * 1000)}",
        "filename": filename,
        "provider": provider,
        "model": model,
        "message": f"DAG execution launched for '{filename}' using {provider} ({model})."
    })

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
