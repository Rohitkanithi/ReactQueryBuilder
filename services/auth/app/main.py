from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(title="Auth Service")
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.get("/health")
def health():
    return {"status": "ok"}
