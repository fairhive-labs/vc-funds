"""
    Crawl the Venture Capital (VC) and Funds tables from the specified LinkedIn URLs and save the extracted data into a CSV file.
"""

import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Function to resolve the LinkedIn redirection URL and follow external link


def resolve_linkedin_redirection(url):
    """
    Resolve the final URL from either a direct LinkedIn redirection URL 
    or the intermediate page that contains the external link.
    Args:
        url (str): LinkedIn redirection URL.
    Returns:
        str: The final resolved URL or the original URL if it fails.
    """
    max_retries = 3  # Retry up to 3 times if there are failures
    retries = 0
    timeout = 20  # Increase timeout to 20 seconds to allow more time for responses

    while retries < max_retries:
        try:
            print(f"Resolving URL: {url} (Attempt {
                  retries + 1}/{max_retries})")

            # Always use GET request to follow redirects and capture content
            response = requests.get(url, allow_redirects=True, timeout=timeout)

            # Check if the response is successful
            if response.status_code == 200:
                # Check if it's a direct redirection
                if response.url != url:
                    print(f"Direct redirection resolved: {response.url}")
                    return response.url

                # If it's not a direct redirection, parse the HTML
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the external link in the page content
                link = soup.find('a', href=True)

                # Ensure we are getting an external link
                if link and "http" in link['href']:
                    print(f"Found external link in HTML: {
                          link['href']} for {url}")
                    # Return the external link from the HTML
                    return link['href']

                print(f"Warning: No external link found for {
                      url}, returning original")
                return url  # Return the original URL if no link found in HTML
            else:
                print(f"Warning: Failed to load {
                      url}, Status Code: {response.status_code}")
                retries += 1
        except requests.RequestException as e:
            print(f"Error resolving {url}: {e}")
            retries += 1
            time.sleep(2)  # Wait for 2 seconds before retrying

    # Return original URL if resolution fails after retries
    print(f"Failed to resolve URL after {max_retries} attempts: {url}")
    return url

# Function to update the CSV with resolved URLs


def update_csv_with_resolved_urls(input_file, output_file):
    """
    Read the CSV file, resolve the URLs, and save the updated file.
    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the output CSV file.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)

        # Check if 'Link' column exists
        if 'Link' not in df.columns:
            raise ValueError("The CSV file must contain a 'Link' column")

        # Initialize a progress bar with tqdm
        print("Resolving URLs, please wait...")
        resolved_urls = []

        for url in tqdm(df['Link'], desc="Processing URLs"):
            resolved_url = resolve_linkedin_redirection(url)
            resolved_urls.append(resolved_url)
            # Adding a delay of 2 seconds between each request to avoid rate-limiting
            time.sleep(2)

        df['ResolvedURL'] = resolved_urls

        # Save the updated CSV to a new file
        df.to_csv(output_file, index=False)
        print(f"\nUpdated CSV saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: The file {input_file} does not exist.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file {input_file} is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Set the input and output CSV file paths
    input_file = 'Complete_VC_and_Investor_Lists.csv'
    output_file = 'Complete_VC_and_Investor_Lists_Resolved.csv'

    # Check if the input file exists before proceeding
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
    else:
        # Call the function to update the CSV
        update_csv_with_resolved_urls(input_file, output_file)
