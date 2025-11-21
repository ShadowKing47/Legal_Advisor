"""
FastAPI main application for Mini Legal Analyst System.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints
from utils.helpers import setup_logging
import logging

# Setup logging
setup_logging("INFO")
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Mini Legal Analyst API",
    description="Production-ready RAG-based legal document analysis system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(endpoints.router, prefix="/api", tags=["analysis"])


@app.on_event("startup")
async def startup_event():
    """Application startup event handler."""
    logger.info("Starting Mini Legal Analyst API")
    logger.info("API documentation available at: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    logger.info("Shutting down Mini Legal Analyst API")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "online",
        "service": "Mini Legal Analyst API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Mini Legal Analyst API"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
