#!/bin/python
import requests
import json
import pprint
import sqlite3

#open db
con = sqlite3.connect('ffl.db')
cur = con.cursor()

# Opening JSON file
f = open('history_standings.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)

def pp(mydict):
	pprint.pprint(mydict)

season_years = []
teams = []
seasons = {}
owners = {}
season_standings = {}
owner_records = []
  
#loop seasons
for season in data:
	season_year = season['seasonId']
	print season_year
	print
 	#cur.execute("INSERT INTO seasons (year) VALUES ('"+str(season_year) +"')")
	
	season_years.append(season_year)
	seasons[season_year] = season
	for team in season['teams']:
		owner_id = str(team["owners"][0])
		#print owner_id
		team_name = ""
		team_name = team["location"] + " " + team["nickname"]
		owners[owner_id] = team_name
		
		# insert record //
		sql = "insert into team_season_record (team_id,year,final_rank,wins,losses,win_perc,ties) VALUES(?,?,?,?,?,?,?)"
		final_rank = team['rankCalculatedFinal']
		print final_rank
		wins = team['record']['overall']['wins']
		losses = team['record']['overall']['losses']
		ties = team['record']['overall']['ties']
		win_perc = team['record']['overall']['percentage']
		
		cur.execute(sql,(owner_id,season_year,final_rank,wins,losses,win_perc,ties))
		
	con.commit()

# Closing file
f.close()