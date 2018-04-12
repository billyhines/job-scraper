# Libraries for scraping

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

max_results_per_title = 100

title_set = ["data+scientist", "data+analyst"]

columns = ["job_title", "company_name", "location", "summary"]
jobs_df = pd.DataFrame(columns = columns)

def extract_job_title_from_result(soup, jobs = []):
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return jobs

def extract_company_from_result(soup, companies = []): 
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return companies

def extract_location_from_result(soup, locations = []):
    spans = soup.findAll("span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return locations
    
def extract_summary_from_result(soup, summaries = []):
    spans = soup.findAll("span", attrs={"class": "summary"})
    for span in spans:
        summaries.append(span.text.strip())
    return summaries
    
    
#scraping code:
for title in title_set:
    for start in range(0, max_results_per_title, 10):
        page = requests.get("http://www.indeed.com/jobs?q=" + str(title) + "&l=boston+%2C+ma" + "&start=" + str(start))
        time.sleep(1)  #ensuring at least 1 second between page grabs
        soup = BeautifulSoup(page.text, "html.parser")
        
        tmpDf = pd.DataFrame(columns = columns)
        
        tmpDf.job_title = extract_job_title_from_result(soup)
        tmpDf.company_name = extract_company_from_result(soup)
        tmpDf.location = extract_location_from_result(soup)
        tmpDf.summary = extract_summary_from_result(soup)
        
        jobs_df = jobs_df.append(tmpDf, ignore_index=True)
        print("scraping and appending")
        
jobs_df = jobs_df.drop_duplicates()
jobs_df.sort_values(['company_name', 'company_name'], ascending=[True, True], inplace=True)
jobs_df.to_csv('jobs.csv',encoding='utf-8')