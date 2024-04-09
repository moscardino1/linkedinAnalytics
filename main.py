

import gspread_dataframe as gd
from google.colab import auth
auth.authenticate_user()

import gspread
from google.auth import default
creds, _ = default()

gc = gspread.authorize(creds)

num_offer = 50
city = "London" #Asia #America #Africa #Europe #North America
# city = ["New York", "Toronto" ]

Keyword = "Data Engineer"
sheetname = 'test_final'
sheetanalysis = 'test_final'

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from datetime import datetime
import json
import re

import pandas as pd
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time

# Function to read data from a Google Sheets worksheet into a DataFrame
def read_sheet_into_dataframe(gc, spreadsheet_url, sheet_name):
    worksheet = gc.open_by_url(spreadsheet_url).worksheet(sheet_name)
    data = worksheet.get_all_values()
    if len(data) > 0:
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        df = pd.DataFrame(columns=data[0])  # Changed to use data[0] as columns
    return df

# Function to extract skills, organizations, and products from text
def extract_skills_and_tech(text):
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']
    organizations = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
    products = [ent.text for ent in doc.ents if ent.label_ == 'PRODUCT']
    return skills, organizations, products

# Function to extract city and country using spaCy NER
def extract_city_country_spacy(text):
    doc = nlp_spacy(text)
    city = ""
    country = ""
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE: Geopolitical Entity
            if not city:
                city = ent.text
            elif city and ent.text != city:  # Avoid assigning the same entity to both city and country
                country = ent.text
    return city, country

# Function to extract job description
def extract_job_description(job_link):
    response = requests.get(job_link)
    soup = BeautifulSoup(response.content, 'html.parser')
    match = soup.find("section", class_="show-more-less-html")
    if match:
        description_text = match.get_text(separator=' ', strip=True)  # Use separator=' ' to preserve spaces
        return re.sub(r'<[^>]+>', ' ', description_text)
    else:
        return "Job description not found."

# Function to extract datetime
def extract_datetime(job_listing):
    datetime_element = job_listing.find("time", class_="job-search-card__listdate")
    if datetime_element:
        return datetime_element.get("datetime")
    else:
        return "N/A"

# Function to extract other details
def extract_other_details(soup):
    try:
        seniority_level = soup.find("span", class_="description__job-criteria-text--criteria").text.strip()
    except AttributeError:
        seniority_level = "N/A"

    try:
        employment_type = soup.find_all("span", class_="description__job-criteria-text--criteria")[1].text.strip()
    except (AttributeError, IndexError):
        employment_type = "N/A"

    try:
        num_applicants = soup.find("figcaption", class_="num-applicants__caption").text.strip()
    except AttributeError:
        num_applicants = "N/A"

    try:
        job_function = soup.find_all("span", class_="description__job-criteria-text--criteria")[2].text.strip()
    except (AttributeError, IndexError):
        job_function = "N/A"

    try:
        industries = soup.find_all("span", class_="description__job-criteria-text--criteria")[3].text.strip()
    except (AttributeError, IndexError):
        industries = "N/A"

    try:
        script_tag = soup.find("script", type="application/ld+json")
        json_ld = script_tag.string
        job_posting = json.loads(json_ld)
        date_posted_str = job_posting.get("datePosted")
        date_posted_dt = datetime.strptime(date_posted_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        date_posted_dt = "N/A"

    return seniority_level, employment_type, num_applicants, job_function, industries, date_posted_dt

# Define search query parameters
search_query = {
    'keywords': Keyword,
    'location': city
}

# Make request to LinkedIn search page
url = f'https://www.linkedin.com/jobs/search?keywords={search_query["keywords"]}&location={search_query["location"]}&f_TPR=r86400'
print(url)
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all job listings
job_listings = soup.find_all("div", class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card")

# Create an empty DataFrame to store job data
job_data = []

# Counter for tracking iterations
counter = 0

# Iterate through each job listing
for job_listing in job_listings:
    # Check if we have already processed the desired number of records
    if counter == num_offer:
        break

    # Add a delay between requests
    time.sleep(2)

    # Extract job title
    job_title = job_listing.find("h3", class_="base-search-card__title").text.strip()

    # Extract company name
    company_name = job_listing.find("h4", class_="base-search-card__subtitle").text.strip()

    # Extract card location
    card_location = job_listing.find("span", class_="job-search-card__location").text.strip()

    # Extract link to job description
    job_link = job_listing.a["href"]
    time.sleep(1)

    job_description = extract_job_description(job_link)

    # Extract other details
    seniority_level, employment_type, num_applicants, job_function, industries, date_posted_dt = extract_other_details(BeautifulSoup(requests.get(job_link).content, 'html.parser'))

    # Append data to list
    job_data.append({
        'Job Title': job_title,
        'Company': company_name,
        'Job Link': job_link,
        'Job Description': job_description,
        'Card Location': card_location,
        'Datetime': date_posted_dt,
        'Seniority Level': seniority_level,
        'Employment Type': employment_type,
        'Num Applicants': num_applicants,
        'Job Function': job_function,
        'Industries': industries
    })

    # Increment counter
    counter += 1
    print(counter)
    time.sleep(1)

# Create DataFrame
df = pd.DataFrame(job_data)

# Read data from Google Sheets into DataFrame
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ND9JczGggyAuV-4RClz7nD70UqUNGfLImywXpFCns-M/edit#gid=0'
output_sheet_name = 'Countries'
countries_decode = read_sheet_into_dataframe(gc, spreadsheet_url, output_sheet_name)

# Merge main DataFrame with countries_decode on 'Card Location'
df = pd.merge(df, countries_decode, on='Card Location', how='left')
nlp = spacy.load("en_core_web_sm")

# Apply extraction functions to 'Job Description' column
df[['skills', 'organizations', 'products']] = df['Job Description'].apply(extract_skills_and_tech).apply(pd.Series)

# Regular expression pattern to extract salary-related information
salary_pattern = r'(?:\$|€|£|USD|EUR|usd|eur|GBP|gbp|cad|CAD)\s?\d[\d\.,]*\d'
# Function to extract salary-related information from description column
def extract_salary(description):
    matches = re.findall(salary_pattern, description)
    return ', '.join(matches)

# Apply the function to the 'description' column
df['salary_info'] = df['Job Description'].apply(extract_salary)
import pandas as pd
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load spaCy model for named entity recognition
nlp_spacy = spacy.load('en_core_web_sm')

# Load the BERT-based NER model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("ml6team/bert-base-uncased-city-country-ner")
model = AutoModelForTokenClassification.from_pretrained("ml6team/bert-base-uncased-city-country-ner")
nlp_bert = pipeline('ner', model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Function to extract city and country using spaCy NER
def extract_city_country_spacy(text):
    doc = nlp_spacy(text)
    city = ""
    country = ""
    for ent in doc.ents:
        if ent.label_ == 'GPE':  # GPE: Geopolitical Entity
            if not city:
                city = ent.text
            elif city and ent.text != city:  # Avoid assigning the same entity to both city and country
                country = ent.text
    return pd.Series([city, country])

# Define a function to apply extract_city_country_spacy only to null rows
def update_city_country(row):
    if pd.isnull(row['City']) or pd.isnull(row['Country']):
        return extract_city_country_spacy(row['Card Location'])
    else:
        return (row['City'], row['Country'])

# Apply the function to the City and Country columns
df[['City', 'Country']] = df.apply(update_city_country, axis=1, result_type='expand')

import pandas as pd
from datetime import datetime

# Function to read data from a Google Sheets worksheet into a DataFrame
def read_sheet_into_dataframe(gc, spreadsheet_url, sheet_name):
    worksheet = gc.open_by_url(spreadsheet_url).worksheet(sheet_name)
    data = worksheet.get_all_values()
    if len(data) > 0:
        df = pd.DataFrame(data[1:], columns=data[0])
    else:
        df = pd.DataFrame(columns=df.columns)
    return df

# Define the spreadsheet URL and sheet names
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ND9JczGggyAuV-4RClz7nD70UqUNGfLImywXpFCns-M/edit#gid=0'
output_sheet_name = sheetname

# Read existing data from the Google Sheets worksheet
worksheet = gc.open_by_url(spreadsheet_url).worksheet(output_sheet_name)
data = worksheet.get_all_values()
if len(data) > 0:
    existing_data = pd.DataFrame(data[1:], columns=data[0])
else:
    existing_data = pd.DataFrame(columns=df.columns)

df['Insert Timestamp'] = datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')

# Merge the existing data with the new data, using the Job Link as the update key
merged_df = pd.concat([existing_data, df]).drop_duplicates(subset='Job Link', keep='last')
merged_df
# Update the worksheet with the merged data
gd.set_with_dataframe(gc.open_by_url(spreadsheet_url).worksheet(output_sheet_name), merged_df)
