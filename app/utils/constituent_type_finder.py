import pandas as pd

def determine_constituent_type(row: pd.Series) -> str:
    """Determine the constituent type based on the given rules."""
    if pd.notna(row["First Name"]) and pd.notna(row["Last Name"]):
        return "Person"
    if pd.notna(row["Title"]):
        return "Person"
    if row["Gender"] != "Unknown" and pd.notna(row["Gender"]):
        return "Person"
    if "Student Scholar" in str(row["Tags"]):
        return "Person"
    return "Company"
