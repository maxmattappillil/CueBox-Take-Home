import os
from fastapi import APIRouter, UploadFile, File, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.services.data_processor import process_csv_files

router = APIRouter()

@router.post("/upload/")
async def upload_files(
    constituents: UploadFile = File(...),
    donations: UploadFile = File(...),
    emails: UploadFile = File(...)
):
    # # Save uploaded files to disk
    # constituents_path = f"temp/{constituents.filename}"
    # donations_path = f"temp/{donations.filename}"
    # emails_path = f"temp/{emails.filename}"

    # with open(constituents_path, "wb") as f:
    #     f.write(await constituents.read())
    # with open(donations_path, "wb") as f:
    #     f.write(await donations.read())
    # with open(emails_path, "wb") as f:
    #     f.write(await emails.read())

    # Process the CSV files
    output_constituents_df, output_tags_df, duplicates_df = process_csv_files(constituents.file, donations.file, emails.file)

    # Convert DataFrames to CSV strings
    constituents_csv = output_constituents_df.to_csv(index=False)
    tags_csv = output_tags_df.to_csv(index=False)
    duplicates_csv = duplicates_df.to_csv(index=False) if not duplicates_df.empty else None

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save CSV strings to temporary files
    with open(CONSTITUENTS_CSV, 'w') as f:
        f.write(constituents_csv)
    with open(TAGS_CSV, 'w') as f:
        f.write(tags_csv)
    if duplicates_csv:
        with open(DUPLICATES_CSV, 'w') as f:
            f.write(duplicates_csv)

    return {
        "message": "Files processed successfully",
        "constituents_csv_url": "/download/constituents",
        "tags_csv_url": "/download/tags",
        "duplicates_csv_url": "/download/duplicates" if duplicates_csv else None
    }

@router.get("/download/constituents", response_class=FileResponse)
async def download_constituents():
    return FileResponse(CONSTITUENTS_CSV, media_type='text/csv', filename="output_constituents.csv", headers={"Content-Disposition": "attachment; filename=output_constituents.csv"})

@router.get("/download/tags", response_class=FileResponse)
async def download_tags():
    return FileResponse(TAGS_CSV, media_type='text/csv', filename="output_tags.csv", headers={"Content-Disposition": "attachment; filename=output_tags.csv"})

@router.get("/download/duplicates", response_class=FileResponse)
async def download_duplicates():
    if os.path.exists(DUPLICATES_CSV):
        return FileResponse(DUPLICATES_CSV, media_type='text/csv', filename="unresolved_duplicates.csv", headers={"Content-Disposition": "attachment; filename=unresolved_duplicates.csv"})
    else:
        raise HTTPException(status_code=404, detail="No unresolved duplicates found.")

import os

templates = Jinja2Templates(directory="app/templates")

# Define paths for output files
OUTPUT_DIR = "output"
CONSTITUENTS_CSV = os.path.join(OUTPUT_DIR, "output_constituents.csv")
TAGS_CSV = os.path.join(OUTPUT_DIR, "output_tags.csv")
DUPLICATES_CSV = os.path.join(OUTPUT_DIR, "unresolved_duplicates.csv")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
