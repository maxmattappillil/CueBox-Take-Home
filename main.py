from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from app.routers import file_upload

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(file_upload.router)
