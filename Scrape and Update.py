import pandas as pd
import psycopg2
import datetime
import scraper


host = "localhost"
database = "jobdb"
user = "postgres"
password = "Password1"


# In[16]:


conn = psycopg2.connect(host=host,database=database, user=user, password=password)


# In[17]:


# Read in the results from the scraper

df = pd.read_csv('jobs.csv')


# In[18]:


# Remove the index column

df.drop(df.columns[0], axis=1, inplace=True)


# In[19]:


df.head()


# In[20]:


# Our database doesn't like our apostrophes, we can just delete them

df['summary'].replace(regex=True,inplace=True,to_replace='\047',value='')
df['job_title'].replace(regex=True,inplace=True,to_replace='\047',value='')
df['company_name'].replace(regex=True,inplace=True,to_replace='\047',value='')


# In[23]:


# Keep a timestamp so we know how long we've had each job listing for

now = datetime.datetime.now()


# In[24]:


# Iterate through the scraped job listings

for index, row in df.iterrows():
    query = """
    SELECT job_id from jobs
    WHERE job_title = '""" + row['job_title'] +"""' AND company_name = '""" + row['company_name'] + """' AND location = '""" + row['location'] + """' AND summary = '""" + row['summary'] + """';"""

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
        ('""" + row['job_title'] + """','""" + row['company_name'] + """','""" + row['location'] + """','""" + row['summary'] + """','""" + now.strftime("%Y-%m-%d %H:%M") +"""', '""" +now.strftime("%Y-%m-%d %H:%M")+ """');"""
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()


# In[25]:


cur.close()
