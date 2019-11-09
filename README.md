# job-scraper
Scrapes Indeed.com for job listings then inserts the listings to a
PostgreSQL database

## Motivations
I initially worked on the job-scraper so that I could search for and
compile job listing for companies that were hiring both for data
analysts and data scientists. As an aspiring data person, I am looking
for an established data team to join and quickly learn from and I
figured anyone hiring for both positions would have a relatively large
team. After looking over the results from the scraper, I felt that I was
looking at the same listings over and over. At that point, I decided
that I should keep the results in a database so I could track how long
job listings had been online for. In the future, I might also be able to
use this data to look at hiring trends over time.

## Instructions
scraper.py holds the function used to scrape Indeed.com job listings. It can
search through multiple search terms, and it checks to make sure there
are no duplicates at the end. It returns a pandas DataFrame.

I used the following tutorial to initialize my PostgreSQL database:
[link](http://www.postgresqltutorial.com/install-postgresql/). Once I had a user and a database
on my machine, I run the "Initial Scape and Insert" to initialize
and then insert the first set of rows into the database. I created "Scrape and Update"
to read in scraper results, update job listings that had
already been found, and read in new entries to the database. The "Read All Results"
script will just read the results from the database and print them to
a csv. 
