from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from app.routers import hello

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(hello.router)
