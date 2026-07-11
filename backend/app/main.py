from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import search

app = FastAPI(title="Business OSINT Search Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}