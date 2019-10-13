import bs4 as BeautifulSoup
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
from os import path
from sqlalchemy import *
import time


e = create_engine('mysql://username:password@localhost:3306/flcs')
conn = e.connect()
cur = conn.connection.cursor()


team_table = pd.read_sql("SELECT Split, CEIL(ROW_NUMBER() OVER (PARTITION BY Team ORDER BY Split)/2)AS Week, Team, Opponent, CASE WHEN Result = 'L' THEN 0 WHEN Result = 'W' THEN 1 ELSE NULL END AS Result, Points FROM team ORDER BY Split,Week",con=e)
player_table = pd.read_sql("SELECT Split,(Week + (Split-1)*9) AS Week, Player, CASE WHEN Player = 'xPeke' AND Position = 'Mid, AD Carry' AND Week > 3 THEN 'AD Carry' WHEN Player = 'xPeke' AND Position = 'Mid, AD Carry' THEN 'Mid' WHEN Player = 'Piglet' AND Position = 'Mid, AD Carry' AND Week > 4 THEN 'Mid' WHEN Player = 'Piglet' AND Position = 'Mid, AD Carry' THEN 'AD Carry' WHEN Player = 'Nukeduck' AND Position = 'Mid, AD Carry' AND week > 2 THEN 'Support' WHEN Player = 'Nukeduck' AND position = 'Mid, AD Carry' THEN 'Mid' ELSE Position END AS Position, Team, Opponent, CASE WHEN Result = 'W' THEN 1 WHEN Result = 'L' THEN 0 ELSE NULL END AS Result, Points FROM player ORDER BY Split, Week ",con=e)

