import pandas as pd
from app.utils.utils import normalize_date, determine_constituent_type, extract_emails, extract_title, \
    format_background_info, calculate_donation_info, fetch_tag_mappings, map_tags

from app.utils.resolve_duplicates import resolve_duplicate_patron_ids

def process_csv_files(constituents_file: str, donations_file: str, emails_file: str):
    # Read input CSV files
    constituents_df = pd.read_csv(constituents_file)
    donations_df = pd.read_csv(donations_file)
    emails_df = pd.read_csv(emails_file)

    # Resolve duplicate patron IDs in constituents_df
    constituents_df, duplicates_df = resolve_duplicate_patron_ids(constituents_df, emails_df)

    # Example: Transform data according to the requirements
    # This is a placeholder for the actual transformation logic
    output_constituents_df = transform_constituents(constituents_df, donations_df, emails_df)
    # output_tags_df = transform_tags(constituents_df)

    # Write the output CSV files
    output_constituents_df.to_csv('output_constituents.csv', index=False)
    # output_tags_df.to_csv('output_tags.csv', index=False)

    # Output unresolved duplicates to a CSV
    if not duplicates_df.empty:
        duplicates_df.to_csv('unresolved_duplicates.csv', index=False)

def transform_constituents(constituents_df, donations_df, emails_df):
    # Fetch tag mappings once
    tag_mappings = fetch_tag_mappings()

    # # Normalize the "Date Entered" column to YYYY-MM-DD format
    # constituents_df['Date Entered'] = constituents_df['Date Entered'].apply(normalize_date)

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
    output_df["CB First Name"] = constituents_df["First Name"].str.title().fillna("")
    output_df["CB Last Name"] = constituents_df["Last Name"].str.title().fillna("")
    output_df["CB Company Name"] = constituents_df["Company"].fillna("")

    # Populate "CB Title"
    output_df["CB Title"] = constituents_df["Title"].apply(extract_title)

    # Populate "CB Email 1 and CB Email 2"
    email_groups = emails_df.groupby("Patron ID")["Email"].apply(list).to_dict()
    output_df["CB Email 1 (Standardized)"], output_df["CB Email 2 (Standardized)"] = zip(
        *output_df.apply(extract_emails, axis=1, args=(email_groups, constituents_df))
    )

    # Populate "CB Background Information"
    output_df["CB Background Information"] = constituents_df.apply(format_background_info, axis=1)

    # Populate "CB Tags"
    output_df["CB Tags"] = constituents_df["Tags"].apply(map_tags, args=(tag_mappings,))

    # Calculate donation-related columns
    donation_info = calculate_donation_info(donations_df)
    output_df[["CB Lifetime Donation Amount", "CB Most Recent Donation Date", "CB Most Recent Donation Amount"]] = \
    output_df["CB Constituent ID"].apply(
        lambda patron_id: donation_info.get(patron_id, ("", "", ""))
    ).apply(pd.Series)

    return output_df

def transform_tags(constituents_df):
    # Implement transformation logic for tags
    # Placeholder for actual logic
    return constituents_df[['Tags']].drop_duplicates()
