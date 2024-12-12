import pandas as pd

def resolve_duplicates(constituents_df: pd.DataFrame, emails_df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """Resolve duplicate Patron IDs in constituents_df using primary email matching."""
    duplicates = constituents_df[constituents_df.duplicated(subset='Patron ID', keep=False)]
    duplicates['Resolved'] = False
    resolved_df = pd.DataFrame()

    for patron_id, group in duplicates.groupby('Patron ID'):
        primary_emails = group['Primary Email'].unique()
        email_matches = emails_df[emails_df['Email'].isin(primary_emails) & (emails_df['Patron ID'] == patron_id)]
        chosen_email = email_matches['Email'].iloc[0]

        updated_row = group[group['Primary Email'] == chosen_email].index
        duplicates.loc[updated_row, 'Resolved'] = True

        resolved_df = pd.concat([resolved_df, group[group['Primary Email'] == chosen_email]])
    constituents_df = pd.concat([constituents_df.drop(duplicates.index), resolved_df.drop(columns=['Resolved'])]).reset_index(drop=True)

    return constituents_df, duplicates