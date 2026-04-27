from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db import engine, Base
from backend.routers import (
    dashboard,
    gmail,
    leads,
    linkedin,
    resume,
    sheets,
    telegram,
    truthgrid,
    whatsapp,
)

# Initialize database tables on startup
def init_db():
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ridhi Command Center API")

# CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Register routers
app.include_router(gmail.router)
app.include_router(telegram.router)
app.include_router(linkedin.router)
app.include_router(whatsapp.router)
app.include_router(resume.router)
app.include_router(truthgrid.router)
app.include_router(dashboard.router)
app.include_router(leads.router)
app.include_router(sheets.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
