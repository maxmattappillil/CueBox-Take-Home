from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.data_processor import process_csv_files

router = APIRouter()

@router.post("/upload/")
async def upload_files(
    constituents: UploadFile = File(...),
    donations: UploadFile = File(...),
    emails: UploadFile = File(...)
):
    # Save uploaded files to disk
    constituents_path = f"temp/{constituents.filename}"
    donations_path = f"temp/{donations.filename}"
    emails_path = f"temp/{emails.filename}"

    with open(constituents_path, "wb") as f:
        f.write(await constituents.read())
    with open(donations_path, "wb") as f:
        f.write(await donations.read())
    with open(emails_path, "wb") as f:
        f.write(await emails.read())

    # Process the CSV files
    process_csv_files(constituents_path, donations_path, emails_path)

    return {"message": "Files processed successfully"}

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
