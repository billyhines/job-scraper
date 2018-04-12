# job-scraper
Scrapes Indeed.com for job listings then inserts the listings to a PostgreSQL database

## Motivations
I initially worked on the job-scraper so that I could search for and compile job listing for companies that were hiring both for data analysts and data scientists. As an aspiring data person, I am looking for an established data team to join and quickly learn from. After looking over the results from the scraper, I felt that I was looking at the same listings over and over. At that point I decided that I should keep the results in a database so I could track how long job listings had been online for, and also be able to get a point where I could see hiring trends of different companies in my area.

## Instructions
scraper.py is the script used to hit Indeed.com for job listings. It can search through multiple search terms, and it checks to make sure there are no duplicates at the end. The results are then stored in a csv file.  

I used the following tutorial to initialize my PostgreSQL database. Once I had a user and a database created, the first two Jupyter Notebooks will initialize and then make the first inserst into the database. The next notebook will read in scraper results and then will update job listings that have already been found and read in new entries to the database. The final notebook will just read the results from the database and print them to a csv. I found myself running these two notebooks so many times that I created updateAndRead.py to execute this all from the command line.