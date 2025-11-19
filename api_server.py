from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
import uvicorn
from datetime import datetime
import os

from agent import initialize_agent_system, CustomerInquiry


class SupportInquiryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000)
    email: EmailStr


class SupportInquiryResponse(BaseModel):
    success: bool
    category: str
    response: str
    faq_count: int
    validation_status: str
    processing_time_ms: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    agents_loaded: bool


class StatsResponse(BaseModel):
    total_inquiries: int
    categories: Dict[str, int]
    avg_response_length: int
    uptime_seconds: int


app = FastAPI(
    title="Customer Support AI Agent API",
    description="Multi-agent customer support system powered by Google ADK",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


orchestrator = None
stats = {
    "total_inquiries": 0,
    "categories": {},
    "total_response_length": 0,
    "start_time": datetime.now()
}


@app.on_event("startup")
async def startup_event():
    global orchestrator
    
    print("=" * 80)
    print("Starting Customer Support AI Agent API Server...")
    print("=" * 80)
    
    try:
        orchestrator = initialize_agent_system()
        print("✓ Agent system initialized successfully")
        print("✓ API server ready to accept requests")
        print("=" * 80)
    except Exception as e:
        print(f"✗ Failed to initialize agent system: {e}")
        print("=" * 80)
        raise


@app.on_event("shutdown")
async def shutdown_event():
    print("\nShutting down API server...")
    print(f"Total inquiries processed: {stats['total_inquiries']}")


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Customer Support AI Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/support/health",
        "submit_inquiry": "POST /api/support/inquiry"
    }


@app.get("/api/support/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    return {
        "status": "healthy" if orchestrator else "degraded",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "agents_loaded": orchestrator is not None
    }


@app.get("/api/support/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_stats():
    uptime = (datetime.now() - stats['start_time']).total_seconds()
    avg_length = (stats['total_response_length'] // stats['total_inquiries'] 
                  if stats['total_inquiries'] > 0 else 0)
    
    return {
        "total_inquiries": stats['total_inquiries'],
        "categories": stats['categories'],
        "avg_response_length": avg_length,
        "uptime_seconds": int(uptime)
    }


@app.post("/api/support/inquiry", response_model=SupportInquiryResponse, tags=["Support"])
async def submit_inquiry(request: SupportInquiryRequest):
    if not orchestrator:
        raise HTTPException(
            status_code=503,
            detail="Agent system not initialized. Please try again later."
        )
    
    try:
        start_time = datetime.now()
        
        result: CustomerInquiry = orchestrator.process_inquiry(
            question=request.question,
            customer_email=request.email
        )
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        stats['total_inquiries'] += 1
        stats['categories'][result.category] = stats['categories'].get(result.category, 0) + 1
        stats['total_response_length'] += len(result.final_response)
        
        return {
            "success": True,
            "category": result.category,
            "response": result.final_response,
            "faq_count": len(result.faq_results.get('raw_results', [])),
            "validation_status": result.validation_status,
            "processing_time_ms": int(processing_time)
        }
        
    except Exception as e:
        print(f"Error processing inquiry: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process inquiry: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    print(f"\nCUSTOMER SUPPORT AI AGENT - REST API SERVER")
    print(f"Server: http://{host}:{port}")
    print(f"API Docs: http://{host}:{port}/docs")
    print(f"Redoc: http://{host}:{port}/redoc\n")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "false").lower() == "true"
    
    run_server(host=host, port=port, reload=reload)
