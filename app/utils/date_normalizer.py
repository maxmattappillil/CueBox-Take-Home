from datetime import datetime
import pandas as pd

def normalize_date(date_str: str) -> str:
    """Normalize date strings to YYYY-MM-DD HH:MM:SS format."""
    if not date_str or pd.isna(date_str):
        return ""

    for fmt in ("%b %d, %Y", "%m/%d/%Y", "%m/%d/%Y %H:%M:%S"):
        try:
            date_obj = datetime.strptime(date_str, fmt)
            # If the time is not provided, default to "00:00:00"
            if date_obj.time() == datetime.min.time():
                return date_obj.strftime("%Y-%m-%d 00:00:00")
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
    return ""
