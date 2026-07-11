from fastapi import FastAPI

app = FastAPI(title="Business OSINT Search Engine")


@app.get("/")
def root():
    return {"message": "Backend is running successfully!"}