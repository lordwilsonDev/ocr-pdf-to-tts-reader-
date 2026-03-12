from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from .whisper_reader.agent import WhisperAgent
from .database import init_db, SessionLocal, Document

app = FastAPI(title="Sovereign Whisper Reader API")

# Setup
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = WhisperAgent()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Store metadata in DB
    db = SessionLocal()
    new_doc = Document(filename=file.filename, path=file_path)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    db.close()
    
    return {"id": new_doc.id, "filename": file.filename}

@app.get("/read/{doc_id}")
async def start_reading(doc_id: int, background_tasks: BackgroundTasks):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == doc_id).first()
    db.close()
    
    if not doc:
        return {"error": "Document not found"}
    
    # Trigger agent in background
    background_tasks.add_task(agent.process_document, doc.path)
    return {"status": "reading started", "filename": doc.filename}

@app.get("/query")
async def query_agent(q: str):
    response = agent.query(q)
    return {"answer": response}

@app.get("/status")
async def get_status():
    return {"status": agent.status}

# Mount UI
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
