import pandas as pd
from app.utils.date_normalizer import normalize_date

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

    # Placeholder logic to populate the DataFrame
    # This will be replaced with actual transformation logic
    output_df["CB Constituent ID"] = constituents_df["Patron ID"]
    output_df["CB Created At"] = constituents_df["Date Entered"].apply(normalize_date)

    return output_df

def transform_tags(constituents_df):
    # Implement transformation logic for tags
    # Placeholder for actual logic
    return constituents_df[['Tags']].drop_duplicates()
