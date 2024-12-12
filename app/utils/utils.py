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

def get_emails(email_groups, patron_id, primary_email):
    """Determine primary and secondary emails for a patron."""
    emails = email_groups.get(patron_id, [])
    email_2 = next((email for email in emails if email != primary_email), "")
    return primary_email, email_2

def extract_emails(row, email_groups, constituents_df):
    """Helper function to extract emails for a given row."""
    patron_id = row["CB Constituent ID"]
    primary_email = constituents_df.loc[constituents_df["Patron ID"] == patron_id, "Primary Email"].values[0]
    return get_emails(email_groups, patron_id, primary_email)

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

def extract_title(title: str) -> str:
     """Extract the first title from a string, handling multiple titles separated by 'and'."""
     if isinstance(title, str):
         if "and" in title:
             return title.split(" and ")[0]
         return title
     return ""

def calculate_donation_info(donations_df: pd.DataFrame) -> dict:
    """Calculate donation-related information for all patrons."""
    donation_info = {}
    paid_donations = donations_df[donations_df["Status"] == "Paid"]

    for patron_id, group in paid_donations.groupby("Patron ID"):
        lifetime_donation = group["Donation Amount"].sum()
        most_recent_date, most_recent_amount = group.loc[group["Donation Date"].idxmax(), ["Donation Date", "Donation Amount"]]
        most_recent_date = pd.to_datetime(most_recent_date).strftime("%Y-%m-%d 00:00:00")

        donation_info[patron_id] = (
            f"${lifetime_donation:.2f}" if lifetime_donation else "",
            most_recent_date,
            f"${most_recent_amount:.2f}" if most_recent_amount else ""
        )

    return donation_info
