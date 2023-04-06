import requests
import json
from bs4 import BeautifulSoup
from l2m import get_ref_dict
jsondata = []

ref_dict=get_ref_dict()
url = 'https://official.nba.com/referee-assignments/'
#url='http://127.0.0.1:5500/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')


table = soup.tbody
gamesdata = table.find_all('tr')
todays_games = []

for game in gamesdata:
	tds = game.find_all('td')
	teamsdata = tds[0]
	teams=teamsdata.get_text(strip=True)
	refsdata = game.find_all('a')
	refs = []
	for ref in refsdata:
		name = (ref.get_text(strip=True)).split('(')[0].strip()
		refs.append(name)
	todays_games.append({'teams':teams, 'refs': refs})


for game in todays_games:
	for ref in game['refs']:
		try:
			print('Game :', game['teams'], 'Name: ',ref, 'Bad Beat Percentage: ', ref_dict[ref]['bad_percent'], 'Total Relevant Games: ', ref_dict[ref]['total_games'])
			row = {
                'teams': game['teams'],
                'name': ref,
                'bad_beat_percentage': ref_dict[ref]['bad_percent'],
                'total_relevant_games': ref_dict[ref]['total_games']
            }
			jsondata.append(row)
		except KeyError:
			print('Game :', game['teams'], 'Name: ',ref, 'Bad Beat Percentage: NA  Total Relevant Games: 0')
			row = {
                'teams': game['teams'],
                'name': ref,
                'bad_beat_percentage': 'NA',
                'total_relevant_games': 0
            }
			jsondata.append(row)

json_data = json.dumps(jsondata)

print(json_data)

	
