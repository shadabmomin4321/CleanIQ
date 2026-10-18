
# CleanIQ — Data Quality & Cleaning Assistant

CleanIQ is a Python-based data quality and cleaning assistant built with Streamlit and Pandas. It helps users profile datasets, identify common data quality issues, review proposed cleaning operations, and validate results.

## Features

- Upload CSV and Excel datasets
- View dataset profiles and quality indicators
- Detect missing values, duplicates, date-format issues, and whitespace
- Review cleaning proposals before approving changes
- Track approved changes through an audit log
- Compare data quality before and after cleaning
- Export cleaned data and audit logs

## Technology Stack

- Python
- Streamlit
- Pandas and NumPy
- Plotly
- OpenPyXL

## Run Locally

1. Install Python 3.12 or a compatible version.
2. Clone or download this repository.
3. Create and activate a virtual environment.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Run the application:

   `python -m streamlit run CleanIQ_Aurora_Fixed.py`

## AI Disclaimer

The current application includes rule-based demo recommendations and AI-related context or prompt previews. A live AI API integration is not claimed as a verified feature of this version.

## Project Status

Personal portfolio project under development. Features should be tested before use with important or sensitive datasets.
