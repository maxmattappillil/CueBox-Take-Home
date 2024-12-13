# Constituent Donation Activity Tracking

This project is designed to process constituent and donation data for a theater organization. It transforms input CSV files into a format suitable for import into the CueBox system, providing insights into donors and their giving history.

## Project Flow

1. **User Input**: Users upload three CSV files (Constituents, Donations, and Emails) through the web interface.
2. **Data Processing**: The uploaded files are processed on the server. This involves:
   - Normalizing and transforming data fields.
   - Resolving duplicate entries.
   - Calculating donation-related information.
   - Mapping tags and extracting relevant information.
3. **Output Generation**: The processed data is compiled into new CSV files, which include:
   - Transformed constituent data.
   - Mapped tags.
   - Any unresolved data to due duplicate Patron IDs for further inspection.
4. **File Download**: The processed CSV files are automatically downloaded to the user's system once processing is complete.

## Assumptions and Decisions

- **CB Constituent ID**: Directly mapped from the "Patron ID" in the input data.
- **CB Created At**: Mapped to the "Date Entered" field. If a timestamp is missing, the default time is set to 00:00:00.
- **CB Constituent Type**:
  - Marked as "Person" if:
    - Both First Name and Last Name are present.
    - Title field is present.
    - Gender is present and not "Unknown".
    - Tags contain "Student Scholar".
  - Otherwise, marked as "Company". Rows with only "Patron ID" and "Date Entered" are assumed to be companies.
- **CB Title**: If the "Title" column contains multiple titles separated by "and", the first title is selected.
- **CB Email 1 and 2**:
  - Primary email is assumed to be "CB Email 1".
  - The email CSV may not be ordered by patron ID with the primary email first, so this is handled accordingly.
- **Duplicate Patron IDs**:
  - Duplicates are identified by repeated Patron IDs.
  - Resolved by matching primary emails from the emails dataframe.
  - If a match is found, the duplicate with the matching primary email is retained.
  - Unresolved duplicates are output to a CSV file for further inspection.
- **Donation Information**:
  - "CB Lifetime Donation Amount" is the total of all donations with a status of "Paid".
  - "CB Most Recent Donation Date" and "CB Most Recent Donation Amount" are based on the most recent donation with a status of "Paid".
  - Donations with a status of "Refunded" are not considered.
- **Tag Mapping**: Only unique mapped tag values are returned to avoid duplicates.

## Questions for Client Success Manager

- Why are there empty rows with only a patron id and date entered?
- How can a donation be recorded for Patron ID 1288 that occurred before the patron was entered into the system according to the constituents file?

## Running the Project

To run the project, follow these steps:

1. Ensure you have Python and the necessary dependencies installed.
2. Start the FastAPI server by running the following command in your terminal:

   ```bash
   uvicorn main:app --reload
   ```

   This command will start the server on `http://127.0.0.1:8000` by default. The `--reload` flag enables auto-reloading of the server when code changes are detected.

3. Access the web interface by navigating to `http://127.0.0.1:8000` in your web browser to upload your CSV files and download the processed results.

The processed files will be downloaded to the root directory of the project in the folder named "output".

## Use of AI Tools

In the development of this project, AI tools were utilized to enhance productivity and efficiency:

- **Aider**: Assisted in backend development, providing suggestions and improvements for Python code, especially in data processing and API integration.
- **Cursor**: Used for frontend development, helping to streamline the creation of HTML, CSS, and JavaScript components for the user interface.

These tools contributed to faster development cycles and improved code quality.
