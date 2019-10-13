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






player_table_temp = []
team_table_temp = []
urls = ['https://fantasy.na.lolesports.com/en-US/league/803748/stats'
    ,'https://fantasy.na.lolesports.com/en-US/league/899089/stats'
    ,'https://fantasy.na.lolesports.com/en-US/league/1078350/stats'
    ,'https://fantasy.na.lolesports.com/en-US/league/1152480/stats'
    ,'https://fantasy.na.lolesports.com/en-US/league/1190618/stats'
    ,'https://fantasy.na.lolesports.com/en-US/league/1224700/stats'
    ,'https://fantasy.na.lolesports.com/en-US/league/1249782/stats']

for split,url in enumerate(urls):
    browser = webdriver.Firefox()
    browser.get(url)
    
    time.sleep(5)
        
    for i,element in enumerate(browser.find_elements_by_class_name("toggle-expansion")):
        element.click()
        number_of_buttons = i + 1
    
    
    
    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup.BeautifulSoup(innerHTML,'html.parser')
    table = soup.find_all('table',{"class":"stats-table stats-table-player"})[0]
    rows = table.find_all('tr')[1:]
    
    
    
    for row in rows:
        temp_table = [cell.get_text() for cell in row.find_all(['tr','td'])]
        temp_table.append(split + 1)
        player_table_temp.append(temp_table)
        
    
 
    
    browser.find_elements_by_class_name("stats-nav-left")[1].click()
        
    
   
        
    for element in browser.find_elements_by_class_name("toggle-expansion")[number_of_buttons:]:
        element.click()

            
    

    
    innerHTML = browser.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup.BeautifulSoup(innerHTML,'html.parser')
    table = soup.find_all('table',{"class":"stats-table stats-table-team"})[0]
    rows = table.find_all('tr')[1:]
       
    for row in rows:
        temp_table = [cell.get_text() for cell in row.find_all(['tr','td'])]
        temp_table.append(split + 1)
        team_table_temp.append(temp_table)
        
        
    browser.close()

    
player_table = pd.DataFrame(player_table_temp,columns=["Week","Matchup","Result","Points","Points2","Games Played","Kills","Deaths","Assists","CS","10+ K/A","3K/4K/5K","Split","Filler"])   
team_table = pd.DataFrame(team_table_temp,columns=["Matchup","Result","Points","Points2","Games Played","Wins","Losses","First Bloods","Dragon Kills","Baron Kills","Towers Destroyed","<30 Min Win","Split","Team"])







player_table["Player"] = ''
player_table["Owner"] = ''
player_table["Position"] = ''
player_table = pd.concat([player_table[player_table["Filler"].notnull()].shift(periods=13,axis='columns'),player_table[player_table["Filler"].isna()]]).reindex(player_table.index)
player_table.replace('',np.nan,inplace=True)
player_table.fillna(method='ffill',inplace=True)
player_table = player_table[player_table["Split"].notnull()]
player_table["Week"] = player_table["Week"].astype(str).str[-1:]
player_table["Team"] = player_table["Matchup"].astype(str).str[:3]
player_table["Opponent"] = player_table["Matchup"].astype(str).str[-3:]
player_table["Result"] = player_table["Result"].astype(str).str[0]
player_table = player_table[["Split","Week","Player","Position","Team","Opponent","Result","Points"]]
player_table.loc[:,"Player"].replace(['Incarnati0n','Zion Spartan','Niels'],['Jensen','Darshan','Zven'],inplace=True)
player_table.loc[:,"Position"].replace(['Jungler, Mid','Mid, Support'],['Jungler','Support'],inplace=True)



team_table["Team"] = team_table["Matchup"].astype(str).str[:3]
team_table["Opponent"] = team_table["Matchup"].astype(str).str[-3:]
team_table["Result"] = team_table["Result"].astype(str).str[0]
team_table = team_table[["Split","Team","Opponent","Result","Points"]]
team_table = team_table[team_table["Split"].notnull()]






cur.execute("DROP TABLE IF EXISTS player")
cur.execute("DROP TABLE IF EXISTS team")

player_table.to_sql(name='player',con=e,dtype={"Split": Float, "Week": Float, "Player": String(32), "Position": String(32), "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})
team_table.to_sql(name='team',con=e,dtype={"Split": Float, "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})                                          