import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import telepot


token ='5330218153:AAH_ZYI7CDNvyXGtUznO1x_1ptlAHYjkKKk'
receiver_id = 799755225

HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def get_jobs_list(url, job_title, location, page_number):
    # create a dictionary of properties to attach to the end of the base url
    # publication_date (fromage) can take one of these values  {1, 3, 7, 14, last} 
    # (1) last 24 hours, (3) last three days, (7) last seven days, (last) since last visit
    query_args = {'q': job_title, 'l': location, 'fromage': 1, 'start' : page_number}
    # designate the base url
    url_cpt = url+urllib.parse.urlencode(query_args)
    page = requests.get(url_cpt, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup.find(class_="jobsearch-ResultsList")

def get_job_details(jobs_list, country, titles, companies, links, dates):
    # get all divs == jobs in the list
    assert jobs_list is not None, 'No new jobs found'

    job_divs = jobs_list.find_all('div', class_='slider_container')
    # get titles
    titles.append([div.find('h2', class_='jobTitle').text.strip() for div in job_divs])
    # get companies
    companies.append([div.find('span', class_='companyName').text.strip() for div in job_divs])
    # get links
    links.append([country+'.indeed.com' + div.find('a')['href'] for div in job_divs])
    # get dates
    dates.append([div.find('span', class_='date').text.strip()[6:] for div in job_divs])
    return titles, companies, links, dates

def scrape_jobs(website, country, job_title, location):
    titles, companies, links, dates = [], [], [], []
    if website == 'indeed':
        if country == 'ca':
            url = 'http://ca.indeed.com/jobs?'
        elif country == 'ma':
            url = 'http://ma.indeed.com/jobs?'
        for page_number in range(0, 21, 10):
            jobs_list = get_jobs_list(url, job_title, location, page_number)
            get_job_details(jobs_list, country, titles, companies, links, dates)
        titles = flatten_list(titles)
        companies = flatten_list(companies)
        links = flatten_list(links)
        dates = flatten_list(dates)
        return pd.DataFrame({'Job Title': titles, 'Company': companies, 'Link': links, 'Date': dates})


def send_telegram_message(token, df):
    bot = telepot.Bot(token)
    for index, row in df.iterrows():
        bot.sendMessage(receiver_id, row['Job Title'] + ' - ' + row['Company'] + ' - ' + row['Link'])

def main(csv_file, job_title, location, country):
    df_old = pd.read_csv(csv_file)
    found = False

    try:
        df = scrape_jobs('indeed', country, job_title, location)
        df.to_csv(csv_file, index=False)
        found = True
    except Exception:
        print('No jobs found')
    

    if found:
        df_new = pd.concat([df_old, df]).drop_duplicates(keep=False)
        if not df_new.empty:
            send_telegram_message(token, df_new)



if __name__ == '__main__':
    job_title = 'data scientist'
    location = ''
    
    main('jobs_ca.csv', job_title, location, 'ca')
    main('jobs_ma.csv', job_title, location, 'ma')