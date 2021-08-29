#!/bin/python
import requests
import json
import pprint
import sqlite3

# Create db
print "Creating db...."
con = sqlite3.connect('ffl.db')

cur = con.cursor()
cur.execute('''
CREATE TABLE teams (
	team_id text,
	team_name text
);
''')

cur.execute('''
CREATE TABLE team_season_record (
	team_id text,
	year integer,
	final_rank integer,
	wins integer,
	losses integer,
	win_perc DECIMAL(10,3)
);
''')