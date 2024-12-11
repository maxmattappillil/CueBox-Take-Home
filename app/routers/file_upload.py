from fastapi import APIRouter, UploadFile, File
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

@router.get("/")
async def root():
    return {"message": "Welcome to the CSV Processing Service"}

@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
