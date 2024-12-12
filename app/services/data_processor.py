import pandas as pd
from app.utils.date_normalizer import normalize_date
from app.utils.constituent_type_finder import determine_constituent_type

def process_csv_files(constituents_file: str, donations_file: str, emails_file: str):
    # Read input CSV files
    constituents_df = pd.read_csv(constituents_file)
    donations_df = pd.read_csv(donations_file)
    emails_df = pd.read_csv(emails_file)

    # Process data to create the output CSVs
    # Example: Transform data according to the requirements
    # This is a placeholder for the actual transformation logic
    output_constituents_df = transform_constituents(constituents_df, donations_df, emails_df)
    output_tags_df = transform_tags(constituents_df)

    # Write the output CSV files
    output_constituents_df.to_csv('output_constituents.csv', index=False)
    output_tags_df.to_csv('output_tags.csv', index=False)

from datetime import datetime

def transform_constituents(constituents_df, donations_df, emails_df):
    # Normalize the "Date Entered" column to YYYY-MM-DD format
    constituents_df['Date Entered'] = constituents_df['Date Entered'].apply(normalize_date)

    # Initialize the output DataFrame with the required columns
    output_df = pd.DataFrame(columns=[
        "CB Constituent ID",
        "CB Constituent Type",
        "CB First Name",
        "CB Last Name",
        "CB Company Name",
        "CB Created At",
        "CB Email 1 (Standardized)",
        "CB Email 2 (Standardized)",
        "CB Title",
        "CB Tags",
        "CB Background Information",
        "CB Lifetime Donation Amount",
        "CB Most Recent Donation Date",
        "CB Most Recent Donation Amount"
    ])

    # Determine "CB Constituent Type"
    output_df["CB Constituent Type"] = constituents_df.apply(determine_constituent_type, axis=1)

    # Populate other columns
    output_df["CB Constituent ID"] = constituents_df["Patron ID"]
    output_df["CB Created At"] = constituents_df["Date Entered"].apply(normalize_date)
    output_df["CB First Name"] = constituents_df["First Name"].str.title()
    output_df["CB Last Name"] = constituents_df["Last Name"].str.title()

    # Populate "CB Company Name"
    output_df["CB Company Name"] = constituents_df.apply(
        lambda row: row["Company Name"] if row["CB Constituent Type"] == "Company" and pd.notna(row["Company Name"]) else "N/A",
        axis=1
    )

    # Standardize and populate emails
    email_groups = emails_df.groupby("Patron ID")["Email"].apply(list).to_dict()

    def get_emails(patron_id, primary_email):
        emails = email_groups.get(patron_id, [])
        email_1 = primary_email
        email_2 = ""

        # Check if there is more than one email available
        if len(emails) > 1:
            # Assign the next available email as email_2
            email_2 = emails[0] if emails[0] != email_1 else emails[1]

        return email_1, email_2

    output_df["CB Email 1 (Standardized)"], output_df["CB Email 2 (Standardized)"] = zip(
        *output_df.apply(lambda row: get_emails(row["CB Constituent ID"], row["Primary Email"]), axis=1)
    )

    return output_df

def transform_tags(constituents_df):
    # Implement transformation logic for tags
    # Placeholder for actual logic
    return constituents_df[['Tags']].drop_duplicates()
