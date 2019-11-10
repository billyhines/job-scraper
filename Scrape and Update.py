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

conn = psycopg2.connect(host=host,database=database, user=user, password=password)


# Our database doesn't like our apostrophes, we can just delete them
scrape_df['summary'].replace(regex=True,inplace=True,to_replace='\047',value='')
scrape_df['job'].replace(regex=True,inplace=True,to_replace='\047',value='')
scrape_df['company'].replace(regex=True,inplace=True,to_replace='\047',value='')

# Keep a timestamp so we know how long we've had each job listing for
now = datetime.datetime.now()

# Iterate through the scraped job listings
for index, row in scrape_df.iterrows():
    query = """
    SELECT job_id from jobs
    WHERE job_title = '""" + row['job'] +"""' AND company_name = '""" + row['company'] + """' AND location = '""" + row['location'] + """' AND summary = '""" + row['summary'] + """';"""

    cur = conn.cursor()
    cur.execute(query)

    # If this job listing already exists in the database we'll update the "last_found" column
    if cur.rowcount > 0:
        updateCommand = """
        UPDATE jobs
        SET last_found = '""" + now.strftime("%Y-%m-%d %H:%M") + """' where job_id = """ + str(cur.fetchone()[0]) + """;"""

        cur = conn.cursor()
        cur.execute(updateCommand)
        cur.close()
        conn.commit()

    # If this job listing has not been found yet, we'll insert a new row
    else:
        command = """
        INSERT INTO jobs (job_title, company_name, location, summary, first_found, last_found)
        VALUES
        ('""" + row['job'] + """','""" + row['company'] + """','""" + row['location'] + """','""" + row['summary'] + """','""" + now.strftime("%Y-%m-%d %H:%M") +"""', '""" +now.strftime("%Y-%m-%d %H:%M")+ """');"""
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()


cur.close()
