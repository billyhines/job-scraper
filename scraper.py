import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_info_from_result(soup, jobs = [], companies = [], summaries = [], locations=[]):
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])

        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())

        for b in div.find_all(name="div", attrs={"class":"summary"}):
            summaries.append(b.text.strip())

        for c in div.find_all(name="div", attrs={"class":"recJobLoc"}):
            locations.append(c["data-rc-loc"])


    df = pd.DataFrame({'job':jobs,
                       'company':companies,
                       'location':locations,
                       'summary':summaries})

    return df

def indeed_scraper(title_set, max_results_per_title):
    job_df = []
    for title in title_set:
        for start in range(0, max_results_per_title, 10):
            page = requests.get("http://www.indeed.com/jobs?q=" + str(title) + "&l=boston+%2C+ma" + "&start=" + str(start))
            time.sleep(1)  #ensuring at least 1 second between page grabs
            soup = BeautifulSoup(page.text, "html.parser")

            job_df.append(extract_info_from_result(soup))
            print("scraping and appending")


    job_df = pd.concat(job_df)
    job_df.drop_duplicates(inplace = True)
    job_df.sort_values(['company', 'job'], ascending=[True, True], inplace=True)

    return job_df
