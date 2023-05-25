import requests
from bs4 import BeautifulSoup
from meczbot import subreddit
from transfermarkt_parsing import body_text, title_text, game_dict_parser
from transfermarkt_parsing import Fixtures
from datetime import date
from collections import defaultdict
from sub_dict import leagues
import json

headers = {
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}

order_queue = ['Europa Wschodnia', 'Europa Zachodnia', 'Europa Południowa', 'Wielka Brytania', 
               'Rozgrywki Polskiego Związku Piłki Nożnej', 'Ekstraklasa', 'Liga Konferencji Europy', 'Liga Europy', 'Liga Mistrzów']

def main():
    f = Fixtures()
    checked_date = date.today()
    checked_link = f.fixtures_link(checked_date)
    r = requests.get(checked_link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    day_dict = defaultdict(list)

    fixtures = f.matches_by_competitions(soup)
    for key, value in fixtures.items():
        submatches = []
        title = value[0]
        link = "https://www.transfermarkt.com" + key
        key = key.split('/')[4]
        submatches.append(15*'*' + '   ' + title + '  ' + 15*'*' + " [{}]({}) ".format(key, link) + 15*'*')
        key = leagues.get(key)
        
        for game in value[1]:
            submatches.append(game_dict_parser(f.single_match(game)))

        if key:
            day_dict[key].extend(submatches)
        

    threads = {}   

    for league_submition in order_queue:
        value = day_dict.get(league_submition)
        key = league_submition
        if value:
            thread = subreddit.submit(title_text(key), selftext = body_text(value), discussion_type='CHAT')
            threads[key] = thread.id

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(threads, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()