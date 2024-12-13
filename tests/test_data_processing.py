import os
import pytest
import pandas as pd
from fastapi.testclient import TestClient
from main import app
from app.utils.utils import normalize_date, determine_constituent_type, extract_title, map_tags

client = TestClient(app)

def test_normalize_date():
    assert normalize_date("Jan 01, 2020") == "2020-01-01 00:00:00"
    assert normalize_date("01/01/2020") == "2020-01-01 00:00:00"
    assert normalize_date("01/01/2020 12:30:00") == "2020-01-01 12:30:00"
    assert normalize_date("") == ""

def test_determine_constituent_type():
    row_person = pd.Series({"First Name": "John", "Last Name": "Doe", "Title": None, "Gender": "Male", "Tags": ""})
    row_company = pd.Series({"First Name": None, "Last Name": None, "Title": None, "Gender": "Unknown", "Tags": ""})
    assert determine_constituent_type(row_person) == "Person"
    assert determine_constituent_type(row_company) == "Company"

def test_extract_title():
    assert extract_title("CEO and Founder") == "CEO"
    assert extract_title("Manager") == "Manager"
    assert extract_title(None) == ""

def test_map_tags():
    tag_mappings = {"VIP": "Very Important Person", "Donor": "Supporter"}
    assert set(map_tags("VIP, Donor", tag_mappings).split(", ")) == {"Very Important Person", "Supporter"}
    assert map_tags("", tag_mappings) == ""

def test_upload_files():
    try:
        constituents_file = ("constituents.csv", open("tests/data/constituents.csv", "rb"), "text/csv")
        donations_file = ("donations.csv", open("tests/data/donations.csv", "rb"), "text/csv")
        emails_file = ("emails.csv", open("tests/data/emails.csv", "rb"), "text/csv")
    except FileNotFoundError:
        pytest.skip("Test data files not found, skipping test_upload_files.")

    response = client.post("/upload/", files={"constituents": constituents_file, "donations": donations_file, "emails": emails_file})
    assert response.status_code == 200
    assert response.json()["message"] == "Files processed successfully"

    # Check if output files are created
    assert os.path.exists("output/output_constituents.csv")
    assert os.path.exists("output/output_tags.csv")

    # Clean up
    os.remove("output/output_constituents.csv")
    os.remove("output/output_tags.csv")
