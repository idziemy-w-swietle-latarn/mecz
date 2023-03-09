import requests
from bs4 import BeautifulSoup
from transfermarkt import main_leagues, second_leagues, main_cups, second_cups, eurocups
from meczbot import subreddit
from transfermarkt_parsing import DomesticCup, DomesticLeague, EuroCup, is_theDay, body_text, title_text, NoDate
from datetime import date

def main():

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    }

    for name, link in main_leagues.items():
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')    
        a = DomesticLeague()
        matches = []
        for gameday in a.oneSeason_gamedays(soup):
            for game in a.oneDay_games(gameday):
                try:
                    today = a.single_game(game)
                    if is_theDay(today['date'], date.today()):
                        matches.append(today)                    
                except NoDate:
                    pass
        if matches:
            subreddit.submit(title_text(name), selftext = body_text(matches), discussion_type='CHAT')

    for name, link in main_cups.items():
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')    
        b = DomesticCup()
        matches = []
        rounds = b.two_top_rounds(soup=soup)
        for round in rounds:
            round = b.games_from_round(round)
            for game in round:
                try:
                    today = b.single_game(game)
                    today['date'] = b.parse_date(today['date'])
                    if is_theDay(today['date'], date.today()):
                        matches.append(today)
                except NoDate:
                    pass
        if matches:
            subreddit.submit(title_text(name), selftext = body_text(matches), discussion_type='CHAT')
            
    for name, link in eurocups.items():
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')    
        b = EuroCup()
        matches = []
        rounds = b.two_top_rounds(soup=soup)
        for round in rounds:
            round = b.games_from_round(round)
            for game in round:
                try:
                    today = b.single_game(game)
                    today['date'] = b.parse_date(today['date'])
                    if is_theDay(today['date'], date.today()):
                        matches.append(today)
                except NoDate:
                    pass
        if matches:
            subreddit.submit(title_text(name), selftext = body_text(matches), discussion_type='CHAT')        

    matches = []
    for name, link in second_leagues.items():
        submatches = []
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')    
        a = DomesticLeague()
        assert not submatches
        for gameday in a.oneSeason_gamedays(soup):
            for game in a.oneDay_games(gameday):
                try:
                    today = a.single_game(game)
                    if is_theDay(today['date'], date.today()):
                        submatches.append(today)
                except NoDate:
                    pass
        if submatches:
            matches.append(15*'*' + '   ' + name + '  ' + 15*'*')
            matches.extend(submatches)
    if matches:
        subreddit.submit(title_text('Inne ligi'), selftext = body_text(matches), discussion_type='CHAT')
    
    
    matches = []
    for name, link in second_cups.items():
        submatches = []
        r = requests.get(link, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')    
        b = DomesticCup()
        rounds = b.two_top_rounds(soup=soup)
        assert not submatches
        for round in rounds:
            round = b.games_from_round(round)
            for game in round:
                try:
                    today = b.single_game(game)
                    today['date'] = b.parse_date(today['date'])
                    if is_theDay(today['date'], date.today()):
                        submatches.append(today)
                except NoDate:
                    pass
        if submatches:
            matches.append(15*'*' + '   ' + name + '  ' + 15*'*')
            matches.extend(submatches)
    
    if matches:
        subreddit.submit(title_text('Inne puchary krajowe'), selftext = body_text(matches), discussion_type='CHAT')
    
        

if __name__ == '__main__':
    main()  