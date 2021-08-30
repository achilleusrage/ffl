#!/bin/python
import requests
import json
import pprint
import sqlite3

#only run this once

# Create db
print "Creating db...."
con = sqlite3.connect('ffl.db')

cur = con.cursor()

cur.execute('''
CREATE TABLE scores (
	year INTEGER,
	sched_num INTEGER,
	home_id TEXT,
	home_points DECIMAL(10,2),
	away_id TEXT,
	away_points DECIMAL(10,2)
)
''')
con.commit()
quit()

cur.execute('''
CREATE TABLE teams (
	team_id text,
	team_name text
);
''')


cur.execute('''
CREATE TABLE team_season_record (
	team_id text,
	team_num integer,
	year integer,
	final_rank integer,
	wins integer,
	losses integer,
	win_perc DECIMAL(10,3),
	pf DECIMAL(10,3)
);
''')