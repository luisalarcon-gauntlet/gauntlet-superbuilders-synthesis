from fastapi import FastAPI

app = FastAPI(title="Math Tutor API")

@app.get("/")
def root():
    return {"message": "Math Tutor API"}

@app.get("/health")
def health():
    return {"status": "healthy"}
