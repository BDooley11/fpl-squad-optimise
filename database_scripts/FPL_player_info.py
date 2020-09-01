import requests , json, csv

url = "https://fantasy.premierleague.com/api/bootstrap-static/"

response = requests.get(url)
data = response.text
parsed = json.loads(data)
length = len(parsed['elements'])

playerData = []

def position(x):

	position =  {
		1: "GK",
		2: "DEF",
		3: "MID",
		4: "FWD"
	}

	return position[x]

def team(x):

	team =  {
		1: "Arsenal",
		2: "Aston Villa",
		3: "Brighton",
		4: "Burnley",
		5: "Chelsea",
		6: "Crystal Palace",
		7: "Everton",
		8: "Fulham",
		9: "Leicester",
		10: "Leeds",
		11: "Liverpool",
		12: "Man City",
		13: "Man Utd",
		14: "Newcastle",
		15: "Sheffield Utd",
		16: "Southampton",
		17: "Spurs",
		18: "West Brom",
		19: "West Ham",
		20: "Wolves"
	}

	return team[x]	

#get csv of player information
for x in range(length):
	data = [
		parsed['elements'][x]['id'],
		parsed['elements'][x]['web_name'],
		position(parsed['elements'][x]['element_type']),
		team(parsed['elements'][x]['team']),
		int(parsed['elements'][x]['now_cost'])/10
	]
	playerData.append(data)

with open("players.csv", "w", encoding="utf-8", newline="") as csvfile:
	headers = ["ID", "Player Name", "Position", "Team Name", "Value"]
	writer = csv.writer(csvfile)
	writer.writerow(headers)
	writer.writerows(playerData)