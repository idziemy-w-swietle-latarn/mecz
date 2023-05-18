from meczbot import reddit
import requests
from bs4 import BeautifulSoup
from time import sleep
from sub_dict import leagues
import json
import logging


def get_competitiors(input_string):
    splitted = input_string.split('-')
    home = ' '.join(splitted[0].split()[:-1])
    away = ' '.join(splitted[1].split()[1:])
    return home, away

def check_competition_offline(input_string: str, resource: dict):
    return resource.get(input_string)

def check_competition_online(input_string):
    link = 'https://www.transfermarkt.pl/schnellsuche/ergebnis/schnellsuche?query={}'
    input_string = '+'.join(input_string.split())
    link = link.format(input_string)
    r = requests.get(link, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    soup = soup.find('div', {'id':'main'})
    soup = soup.main.find_all('div', recursive=False)
    for div in soup:
        div = div.table.tbody.find_all('tr', recursive=False)
        div = div[0].find('td', {'class':'hauptlink'}).a['href']
        if 'verein' not in div:
            print(div)
            continue
        div = str(div).replace('startseite', 'spielplan')
        link = "https://www.transfermarkt.pl" + div
        html = requests.get(link, headers=headers).text
        div = BeautifulSoup(html, 'html.parser')
        div = div.find_all('div', {'class': 'table-header'})
        return [competition.h2.a['href'] for competition in div]
    return None


while True:
    try:
        logging.basicConfig(filename='golgif.log', encoding='utf-8', level=logging.INFO)
        subreddit = reddit.subreddit('soccer')
        result = subreddit.stream.submissions(skip_existing=True)


        template = "[{}]({})"
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
        }

        with open('data.json', encoding='utf-8') as f:
            threads = json.load(f)

        for submission in result:
            if submission.link_flair_text == 'Media':
                if '-' in submission.title:
                    competitors = get_competitiors(submission.title)
                    logging.info(submission.title)
                    try:
                        competitions_links = check_competition_online(competitors[0])
                    except AttributeError as e:
                        try:
                            competitions_links = check_competition_online(competitors[1])
                        except AttributeError:
                            competitions_links = None
                    if competitions_links:
                        for link in competitions_links:
                            thread_title = leagues.get(link.split('/')[4])
                            if thread_title:
                                thread_id = threads.get(thread_title)
                                if thread_id:
                                    thread = reddit.submission(thread_id)
                                    thread.reply(template.format(submission.title, submission.url))
                                    logging.info('Submitted: {}'.format(submission.title))
                                    break
    except Exception as e:
        logging.exception(e)
        continue