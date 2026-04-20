from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db import engine, Base
from backend.routers import (
    gmail,
    telegram,
    linkedin,
    whatsapp,
    resume,
    truthgrid,
    dashboard,
    content_scheduler,
    auto_responder,
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

# Initialize DB
init_db()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Register routers
app.include_router(gmail.router)
app.include_router(telegram.router)
app.include_router(linkedin.router)
app.include_router(whatsapp.router)
app.include_router(content_scheduler.router)
app.include_router(auto_responder.router)
app.include_router(resume.router)
app.include_router(truthgrid.router)
app.include_router(dashboard.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
