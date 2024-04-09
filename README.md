# Dashboard Link
- Keywords set as Data Engineer
https://lookerstudio.google.com/reporting/b59e7673-bc6b-4811-b521-5ea353e9264f/page/p_13pn3bm7fd
<img width="968" alt="Screenshot 2024-04-09 at 3 45 17 PM" src="https://github.com/moscardino1/linkedinAnalytics/assets/9267948/50aa1372-6bad-4ae8-b741-248955ab10cc">

# Job Listings Scraper

This project is designed to scrape job listings from LinkedIn based on specific keywords and locations, then process and analyze the extracted data. The script performs several functions such as extracting job descriptions, skills, organizations, and products from text, as well as merging the scraped data with existing data from Google Sheets.
This project is a Python script that scrapes job listings from LinkedIn based on a given search query and location. It extracts various information about the job listings, such as job title, company, job description, location, and other relevant details. The script then stores the data in a Google Sheets worksheet.

## Features

- Scrapes job listings based on keywords and locations
- Extracts job descriptions, skills, organizations, products, city, country, salary information, seniority level, employment type, number of applicants, job function, and industries
- Merges scraped data with existing data from Google Sheets based on Job Link as the update key
## Features

- Extracts job title, company, job link, job description, location, and other details for a specified number of job listings.
- Utilizes `gspread` and `gspread_dataframe` libraries to interact with Google Sheets.
- Employs `spaCy` and `transformers` libraries for named entity recognition (NER) to extract skills, organizations, and products from the job descriptions.
- Extracts city and country information from the job location using both `spaCy` and a BERT-based NER model.
- Handles pagination and adds a delay between requests to avoid rate limiting.
- Merges the new data with the existing data in the Google Sheets worksheet, using the job link as the update key.
## Requirements

- Python 3.x
- gspread_dataframe
- google-auth
- google-auth-httplib2
- google-auth-oauthlib
- google-api-python-client
- requests
- spacy
- transformers
- BeautifulSoup
- pandas
- numpy
- datetime
- json
- re

 

Before running the script, make sure you have the following prerequisites:

1. Python 3.x installed on your system.
2. The following Python libraries installed:
   - `gspread`
   - `google-auth`
   - `gspread_dataframe`
   - `requests`
   - `beautifulsoup4`
   - `pandas`
   - `spacy`
   - `transformers`
3. A Google Cloud Platform project with the Google Sheets API and Google Drive API enabled.
4. A Google Sheets spreadsheet with a worksheet named `test_final` (or the desired worksheet name).
5. A Google Cloud Platform service account with the necessary permissions to access the Google Sheets spreadsheet.

## Setup

1. Authenticate your Google account for access to Google Sheets. Follow instructions here: https://docs.gspread.org/en/latest/oauth2.html
2. Replace the Google Sheets URL, sheet name, and other necessary parameters in the code according to your needs.
 
## Usage

1. Clone the repository or copy the provided code.
2. Replace the following variables with your desired values:
   - `num_offer`: The number of job listings to scrape.
   - `city`: The city or region to search for job listings (e.g., "London", "Asia", "America", "Africa", "Europe", "North America").
   - `Keyword`: The keyword to search for job listings (e.g., "Data Engineer").
   - `sheetname`: The name of the worksheet in the Google Sheets spreadsheet to store the data.
   - `sheetanalysis`: The name of the worksheet in the Google Sheets spreadsheet to store the analysis.
3. Authenticate your Google Cloud Platform service account by running the provided code:

   ```python
   from google.colab import auth
   auth.authenticate_user()
   
   import gspread
   from google.auth import default
   creds, _ = default()
   
   gc = gspread.authorize(creds)


   
For more details about each function used in this project, refer to their respective documentation links below:

- gspread_dataframe: https://github.com/trending/gspread-dataframe
- spacy: https://spacy.io/usage/
- Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#documentation-for-the-newest-release
- Pandas: https://pandas.pydata.org/docs/

Feel free to modify this project according to your needs!

