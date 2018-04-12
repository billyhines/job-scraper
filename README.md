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
scraper.py is the script used to scrape Indeed.com job listings. It can
search through multiple search terms, and it checks to make sure there
are no duplicates at the end. The results are then stored in a csv file.

I used the following tutorial to initialize my PostgreSQL database:
[link](https://www.codementor.io/engineerapart/getting-started-
with-postgresql-on-mac-osx-are8jcopb). Once I had a user and a database
on my machine, I created the first two Jupyter Notebooks to initialize
and then insert the first set of rows into the database. I created the
third notebook to read in scraper results, update job listings that had
already been found, and read in new entries to the database. The final
notebook will just read the results from the database and print them to
a csv. I found myself running these final two notebooks so many times
that I created updateAndRead.py to execute this all from the command
line.
