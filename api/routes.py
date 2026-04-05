from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.stock_analyst.crew import StockAnalystCrew

router = APIRouter()

jobs = {}

class AnalysisResponse(BaseModel):
    job_id: str
    ticker: str
    status: str
    message: str

class JobStatus(BaseModel):
    job_id: str
    ticker: str
    status: str
    result: str | None = None
    error: str | None = None
    created_at: str
    completed_at: str | None = None

def run_analysis(job_id: str, ticker: str):
    try:
        jobs[job_id]["status"] = "running"
        crew = StockAnalystCrew(ticker)
        result = crew.kickoff()
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = str(result)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()

        os.makedirs("reports", exist_ok=True)
        with open(f"reports/{ticker}_report.txt", "w") as f:
            f.write(str(result))

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()

@router.post("/analyze/{ticker}", response_model=AnalysisResponse)
async def analyze_stock(ticker: str, background_tasks: BackgroundTasks):
    ticker = ticker.upper()

    job_id = str(uuid4())
    jobs[job_id] = {
        "job_id":       job_id,
        "ticker":       ticker,
        "status":       "queued",
        "result":       None,
        "error":        None,
        "created_at":   datetime.now().isoformat(),
        "completed_at": None
    }

    background_tasks.add_task(run_analysis, job_id, ticker)

    return AnalysisResponse(
        job_id=job_id,
        ticker=ticker,
        status="queued",
        message=f"Analysis started for {ticker}. Poll /report/{job_id} for results."
    )

@router.get("/report/{job_id}", response_model=JobStatus)
async def get_report(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatus(**jobs[job_id])

@router.get("/jobs")
async def list_jobs():
    return {
        "total": len(jobs),
        "jobs": [
            {
                "job_id":     j["job_id"],
                "ticker":     j["ticker"],
                "status":     j["status"],
                "created_at": j["created_at"]
            }
            for j in jobs.values()
        ]
    }