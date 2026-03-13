"""
FastAPI main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth, lessons

app = FastAPI(
    title="Synthesis Math Tutor API",
    description="Backend API for fraction equivalence math tutor",
    version="0.1.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(lessons.router)


@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Synthesis Math Tutor API", "status": "running"}
