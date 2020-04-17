from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import time

pages = [10, 20, 30, 40, 50]

# Enter URL from Indeed website (should end with '=')
URL = input('Enter URL: ')

job_titles = []
company_name = []
locations = []
job_summary = []
sal = []

for page in pages:

    source = requests.get(f'''
    {URL}{page}
    ''').text

    soup = BeautifulSoup(source, 'html.parser')

    for jobs in soup.find_all(class_='result'):

        try:
            job_title = jobs.h2.text.strip()
        except:
            job_title = None
        job_titles.append(job_title)
        # print('-------------------')

        try:
            company = jobs.span.text.strip()
        except:
            company = None
        company_name.append(company)
        # print('-------------------')

        try:
            location = jobs.find(class_='location').text.strip()
        except:
            location = None
        locations.append(location)
        # print('-------------------')

        try:
            summary = jobs.find(class_='summary').text.strip()
        except:
            summary = None
        job_summary.append(summary)
        # print('-------------------')

        try:
            salary = jobs.find('span', class_='no-wrap').text.strip()
        except:
            salary = None
        sal.append(salary)
        # print('-------------------')

    # Save yourself from getting IP blocked
    time.sleep(2)

df = pd.DataFrame({'job_title': job_titles, 'company_name': company_name, 'location': locations,
                   'summary': job_summary, 'salary': sal})
# print(df.head())

# Name your CSV
df.to_csv(f'indeed_{input("Name CSV (without .csv): ")}.csv')
