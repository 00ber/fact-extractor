from typing import List
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
# from chain_v1 import get_facts
from chain_v2 import get_facts
from logger import logger

jobs = {}

class RequestPayload(BaseModel):
    question: str
    documents: List[str]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def process_request(job_identifier, payload: RequestPayload):
    job_info = jobs[job_identifier]
    results = await get_facts(payload.question, payload.documents)
    job_info["facts"] = results["facts"]
    job_info["errors"] = results["errors"]
    job_info['status'] = 'done'
    return

@app.get('/status')
def status():
    return {
        'all': list(jobs.values()),
    }

@app.get('/status/{identifier}')
async def status(identifier):
    return {
        "status": jobs.get(identifier, 'job with that identifier is undefined'),
    }

@app.post("/submit_question_and_documents")
async def submit_question_and_documents_static(payload: RequestPayload):
    request_id = "44fefa65-8c54-4d37-92ef-314bfc977776"
    # request_id = str(uuid.uuid4())
    logger.info(request_id)
    jobs[request_id] = {
        "question": payload.question,
        "facts": [],
        "errors": [],
        "status": "processing"
    }
    asyncio.create_task(process_request(request_id, payload))

    return {"request_id": request_id}

@app.get("/get_question_and_facts")
async def get_question_and_facts_static():
    request_id = "44fefa65-8c54-4d37-92ef-314bfc977776"
    if request_id not in jobs:
        raise HTTPException(status_code=404, detail=f"Job for request {request_id} not found")
    logger.info(jobs[request_id]["status"])
    return jobs[request_id]

@app.get("/test")
async def test():
    response = await get_facts(
        "What are our product design decisions?", 
        [
            "http://test-fileserver:8081/call_log_sdfqwer.txt",
            "http://test-fileserver:8081/call_log_fdadweq.txt"
        ]
    )
    return response
