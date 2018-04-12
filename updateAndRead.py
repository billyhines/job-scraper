import pandas as pd
import psycopg2
import datetime

host = "localhost"
database = "jobdb"
user = "jobuser"
password = "punch"

conn = psycopg2.connect(host=host,database=database, user=user, password=password)

df = pd.read_csv('jobs.csv')

# Remove the column of index values
df.drop(df.columns[0], axis=1, inplace=True)

# Our database really doesn't like apostrophes, remove these
df['summary'].replace(regex=True,inplace=True,to_replace='\047',value='')
df['job_title'].replace(regex=True,inplace=True,to_replace='\047',value='')
df['company_name'].replace(regex=True,inplace=True,to_replace='\047',value='')

now = datetime.datetime.now()

for index, row in df.iterrows():
    query = """
    SELECT job_id from jobs
    WHERE job_title = '""" + row['job_title'] +"""' AND company_name = '""" + row['company_name'] + """' AND location = '""" + row['location'] + """' AND summary = '""" + row['summary'] + """';"""
    
    cur = conn.cursor()
    cur.execute(query)
    
    # Check to see if we already have this job listing, if so update the "last_found" column
    if cur.rowcount > 0:
        updateCommand = """
        UPDATE jobs
        SET last_found = '""" + now.strftime("%Y-%m-%d %H:%M") + """' where job_id = """ + str(cur.fetchone()[0]) + """;"""
        
        cur = conn.cursor()
        cur.execute(updateCommand)
        cur.close()
        conn.commit()
    
    # If it's a new job listing, insert it into the table
    else:
        command = """
        INSERT INTO jobs (job_title, company_name, location, summary, first_found, last_found)
        VALUES
        ('""" + row['job_title'] + """','""" + row['company_name'] + """','""" + row['location'] + """','""" + row['summary'] + """','""" + now.strftime("%Y-%m-%d %H:%M") +"""', '""" +now.strftime("%Y-%m-%d %H:%M")+ """');"""
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()

cur.close()

# Re-open the connection to pull the database into a .csv
conn = psycopg2.connect(host=host,database=database, user=user, password=password)

query = """SELECT * from jobs"""

cur = conn.cursor()
dfTemp = pd.read_sql(query, con=conn)
cur.close()

dfTemp['first_found'] = dfTemp['first_found'].astype('datetime64[ns]')
dfTemp['last_found'] = dfTemp['last_found'].astype('datetime64[ns]')
dfTemp['timeOnBoard'] = dfTemp['last_found'] - dfTemp['first_found']

dfTemp.sort_values(['last_found', 'timeOnBoard', 'company_name'], ascending=[False, True, True], inplace=True)

dfTemp.to_csv('allJobs.csv')