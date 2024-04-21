from typing import List
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from chain import get_facts
import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

jobs = {}

class RequestPayload(BaseModel):
    question: str
    documents: List[str]

app = FastAPI()


async def process_request(job_identifier, payload: RequestPayload):
    job_info = jobs[job_identifier]
    job_info["response_payload"] = {
        "question": payload.question,
        "facts": None,
        "status": "processing"
    }
   
    results = await get_facts(payload.question, payload.documents)
    job_info["response_payload"]["facts"] = results["facts"]
    job_info["response_payload"]['status'] = 'done'

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
async def submit_question_and_documents(payload: RequestPayload):
    global jobs
    request_id = "44fefa65-8c54-4d37-92ef-314bfc977776"
    # request_id = str(uuid.uuid4())
    logger.info(request_id)
    jobs[request_id] = {}
    asyncio.run_coroutine_threadsafe(process_request(request_id, payload), loop=asyncio.get_running_loop())

    return {"request_id": request_id}

@app.get("/get_question_and_facts")
async def get_question_and_facts():
    request_id = "44fefa65-8c54-4d37-92ef-314bfc977776"
    job_info = jobs[request_id]

    return job_info["response_payload"]


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
