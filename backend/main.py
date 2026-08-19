from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from api import routes_upload, routes_status, routes_findings, routes_report

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Statement Audit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_upload.router)
app.include_router(routes_status.router)
app.include_router(routes_findings.router)
app.include_router(routes_report.router)


@app.get("/")
def root():
    return {"message": "Financial Statement Audit API is running"}
