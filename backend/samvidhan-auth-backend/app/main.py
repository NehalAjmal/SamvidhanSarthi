from fastapi import FastAPI
from app.db import Base, engine
from app.routes import users

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Samvidhan Sarthi Auth API", version="1.0")

app.include_router(users.router, tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Authentication API is running"}
