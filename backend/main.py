"""
FastAPI backend for Synthesis Math Tutor
Minimal placeholder implementation for infrastructure setup
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Synthesis Math Tutor API",
    description="Backend API for fraction equivalence lesson",
    version="0.1.0"
)


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return JSONResponse(content={"status": "healthy"})


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(content={
        "message": "Synthesis Math Tutor API",
        "status": "Infrastructure setup complete. Application code will be implemented by subsequent agents."
    })
