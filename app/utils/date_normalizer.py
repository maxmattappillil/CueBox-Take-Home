from datetime import datetime

def normalize_date(date_str: str) -> str:
    """Normalize date strings to YYYY-MM-DD format."""
    for fmt in ("%b %d, %Y", "%m/%d/%Y", "%m/%d/%Y %H:%M:%S"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""
