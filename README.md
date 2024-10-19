# LinkedIn VC and Funds Table Crawler

This script crawls the Venture Capital (VC) and Funds tables from specified LinkedIn URLs and saves the extracted data into a CSV file. It resolves LinkedIn redirection URLs to follow external links and updates the CSV file with the resolved URLs.

## Requirements

To run this script, you need to have the following Python libraries installed:

- `pandas`
- `requests`
- `beautifulsoup4`
- `tqdm`

You can install these libraries using pip:

```bash
pip install pandas requests beautifulsoup4 tqdm
```

## Setup

Input CSV File: Ensure you have an input CSV file named `Complete_VC_and_Investor_Lists.csv` with a column named Link containing the LinkedIn URLs to be resolved.

Output CSV File: The script will generate an output CSV file named `Complete_VC_and_Investor_Lists_Resolved.csv` with the resolved URLs.

## Usage

Place the input CSV file in the same directory as the script.
Run the script using Python:

```bash
python resolve_linkedin_urls.py
```

### Script Overview

The script performs the following tasks:

Resolve LinkedIn Redirection URLs: The `resolve_linkedin_redirection` function handles the resolution of LinkedIn redirection URLs, following external links if necessary.
Update CSV with Resolved URLs: The `update_csv_with_resolved_urls` function reads the input CSV file, resolves the URLs, and saves the updated file with the resolved URLs.

## Notes

The script includes error handling for file not found, empty data, and other unexpected errors.

A progress bar is displayed using tqdm to indicate the progress of URL resolution.

A delay of 2 seconds is added between each request to avoid rate-limiting.
