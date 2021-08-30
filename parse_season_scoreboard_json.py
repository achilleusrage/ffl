#!/bin/python
import requests
import json
import pprint
import sqlite3
import os

# parses scoreboard json
# > 2018 url is: https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/200597?view=modular&view=mNav&view=mMatchupScore&view=mScoreboard&view=mSettings&view=mTopPerformers&view=mTeam
# < 2018 url is: https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/200597?view=mLiveScoring&view=mMatchupScore&view=mRoster&view=mSettings&view=mStandings&view=mStatus&view=mTeam&view=modular&view=mNav&seasonId=2017
def pp(mydict):
	pprint.pprint(mydict)
	
#open db
con = sqlite3.connect('ffl.db')
cur = con.cursor()

# scan the dir for json files to parse
json_files = []
json_dir = 'json_data/scoreboards'
for entry in os.listdir(json_dir):
    if os.path.isfile(os.path.join(json_dir, entry)):
        json_files.append(entry)

# loop thru files, open and parse
for json_f in json_files:
	json_f_full_path = json_dir + '/' + json_f
	f = open(json_f_full_path,)
	json_data = json.load(f)
	
	print "PARSING..." + json_f_full_path
	print
	
	# for older seasons, json starts with index 0
	if json_data[0]:
		season_data = json_data[0]
	else:
		season_data = json_data
	# first, get the season "team number (0-9 or 11)" and save it to the db

	for x in season_data['teams']:
		owner_id = x['primaryOwner']
		team_num = x['id']
		#print owner_id
		#print team_num
		points_for = x['points']
		year = season_data['seasonId']
		#print year
		# update db to assign in season team_num to owner for year
		sql = """
				UPDATE team_season_record
				SET team_num = ?,
				pf = ?
				WHERE team_id = ?
				AND year = ?
				"""
		cur.execute(sql,(team_num,points_for,owner_id,year))
	
	# now process scores #
	year = season_data['seasonId']
	sql_delete = "DELETE FROM scores WHERE year = ?"
	
	cur.execute(sql_delete,(year,))
	
	for week in season_data['schedule']:
		home_id = week['home']['teamId']
		home_points = 0
		away_id = week['away']['teamId']
		away_points = 0
		sched_num = week['matchupPeriodId']
		
		for p in week['home']['pointsByScoringPeriod']:
			# only take the last score (playoffs have more than one period)
			home_points = week['home']['pointsByScoringPeriod'][p]
			
		for p in week['away']['pointsByScoringPeriod']:
			# only take the last score (playoffs have more than one period)
			away_points = week['away']['pointsByScoringPeriod'][p]
		
		sql_insert = """
			INSERT INTO scores (year,home_id,home_points,away_id,away_points,sched_num)
			VALUES(?,?,?,?,?,?)
		"""
		cur.execute(sql_insert,(year,home_id,home_points,away_id,away_points,sched_num))

con.commit()

