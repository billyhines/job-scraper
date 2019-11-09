
import pandas as pd
import psycopg2
import datetime
import scraper

# Scrape
max_results_per_title = 100
title_set = ["data+scientist", "data+analyst"]

scrape_df = scraper.indeed_scraper(title_set, max_results_per_title)

# Connect to DB and insert data
host = "localhost"
database = "jobdb"
user = "postgres"
password = "Password1"

# Make a connection to the database and then create a cursor
conn = psycopg2.connect(host=host,database=database, user=user, password=password)
cur = conn.cursor()

# Command to create the database table

command = """
CREATE TABLE jobs (
job_id SERIAL PRIMARY KEY,
job_title VARCHAR(255) NOT NULL,
company_name VARCHAR(255) NOT NULL,
location VARCHAR(255) NOT NULL,
summary VARCHAR(255) NOT NULL,
first_found VARCHAR(255),
last_found VARCHAR(255)
)
"""

cur.execute(command)

# Our database doesn't like our apostrophes, we can just delete them
scrape_df['company'].replace(regex=True,inplace=True,to_replace='\047',value='')
scrape_df['job'].replace(regex=True,inplace=True,to_replace='\047',value='')
scrape_df['summary'].replace(regex=True,inplace=True,to_replace='\047',value='')

# Keep a timestamp so we know how long we've had each job listing for
now = datetime.datetime.now()

# Iterate through the scraped job listings and insert them into the database
for index, row in scrape_df.iterrows():
    command = """
    INSERT INTO jobs (job_title, company_name, location, summary, first_found, last_found)
    VALUES
    ('""" + row['job'] + """','""" + row['company'] + """','""" + row['location'] + """','""" + row['summary'] + """','""" + now.strftime("%Y-%m-%d %H:%M") +"""', '""" +now.strftime("%Y-%m-%d %H:%M")+ """');"""

    cur = conn.cursor()
    cur.execute(command)
    cur.close()
    conn.commit()
