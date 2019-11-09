
import pandas as pd
import psycopg2
import datetime

host = "localhost"
database = "jobdb"
user = "postgres"
password = "Password1"

conn = psycopg2.connect(host=host,database=database, user=user, password=password)

# Pull everything from the job database
query = """SELECT * from jobs"""

cur = conn.cursor()
dfTemp = pd.read_sql(query, con=conn)
cur.close()

# Format the date columns as datetime64 so we can calculate how long the job posting has been up for
dfTemp['first_found'] = dfTemp['first_found'].astype('datetime64[ns]')
dfTemp['last_found'] = dfTemp['last_found'].astype('datetime64[ns]')
dfTemp['timeOnBoard'] = dfTemp['last_found'] - dfTemp['first_found']

# Sort the listing so that the newest listing appear first
dfTemp.sort_values(['last_found', 'timeOnBoard', 'company_name'], ascending=[False, True, True], inplace=True)

dfTemp.to_csv('allJobs.csv')
