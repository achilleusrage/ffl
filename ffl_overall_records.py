#!/bin/python
import requests
import json
import pprint
import sqlite3
from prettytable import from_db_cursor


con = sqlite3.connect('ffl.db')
cur = con.cursor()

sql = """select team_name,SUM(wins) as w,SUM(losses) as l,SUM(ties) as t,
	     printf("%.3f",(
	     	CAST(
	     		SUM(wins) AS FLOAT
	     		) 
	     / 
	        (
	        	CAST(SUM(wins) + SUM(losses) as float)
	        )
	     )
	     )
	     as "WIN%",
	     printf("%.2f",AVG(final_rank)) as "AVG FINISH",
	     SUM(final_rank = 1) as "CHAMPS",
	     SUM(final_rank = 2) as "RUNNER UPS",
	     SUM(final_rank = 3) as "3RDs",
	     SUM(final_rank = 4) as "4THs",
	     SUM(final_rank = 10 OR final_rank = 12) as "LAST"
	     from team_season_record
		 JOIN teams on team_season_record.team_id = teams.team_id
		 JOIN seasons on team_season_record.year = seasons.year
		 GROUP BY team_name
		 ORDER BY "WIN%" DESC
		 """;
cur.execute(sql)
mytable = from_db_cursor(cur)
	
print mytable