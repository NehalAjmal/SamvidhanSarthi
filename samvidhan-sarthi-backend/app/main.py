from fastapi import FastAPI
from app.routes import user_routes, article_routes, bail_routes, rti_routes

app = FastAPI(
    title="Samvidhan Sarthi Backend",
    description="Digital platform for legal and constitutional literacy",
    version="1.0.0"
)

app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(article_routes.router, prefix="/articles", tags=["Articles"])
app.include_router(bail_routes.router, prefix="/bail", tags=["Bail Reckoner"])
app.include_router(rti_routes.router, prefix="/rti", tags=["RTI Helper"])

@app.get("/")
def root():
    return {"message": "Welcome to Samvidhan Sarthi API"}
