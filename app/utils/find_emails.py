def get_emails(email_groups, patron_id, primary_email):
    """Determine primary and secondary emails for a patron."""
    emails = email_groups.get(patron_id, [])
    email_1 = primary_email
    email_2 = ""

    # Check if there is more than one email available
    if len(emails) > 1:
        # Assign the next available email as email_2
        email_2 = emails[0] if emails[0] != email_1 else emails[1]

    return email_1, email_2
