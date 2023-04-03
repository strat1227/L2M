import requests
from bs4 import BeautifulSoup
from l2m import get_ref_dict

ref_dict=get_ref_dict()
#url = 'https://official.nba.com/referee-assignments/'
url='http://127.0.0.1:5500/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.tbody
gamesdata = table.find_all('tr')
todays_games = []

print(ref_dict)

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
		except KeyError:
			print('Game :', game['teams'], 'Name: ',ref, 'Bad Beat Percentage: NA  Total Relevant Games: 0')


	
