import bs4 as BeautifulSoup
import csv
from selenium import webdriver
import numpy as np
import pandas as pd
from os import path
from sqlalchemy import *

total = pd.DataFrame(columns=["Week","Player","Team","Opponent","Region","Points"])
Week = pd.read_excel("FantasyLCSPlayerPoints.xlsx",sheet_name="Week1")
WeekTeams = Week[Week["Game 1"].isna()]
WeekPlayers = Week[(Week['Players'].str.isupper()==False)&(Week['Players'] != 100)]
print(WeekPlayers)
WeekPlayers[['Points 1','Game 1']] = WeekPlayers['Game 1'].str.split('(',expand=True)
WeekPlayers[['Points 2','Game 2']] = WeekPlayers['Game 2'].str.split('(',expand=True)
WeekPlayers['Team 1.1'] = WeekPlayers['Game 1'].astype(str).str[:3]
WeekPlayers['Team 2.1'] = WeekPlayers['Game 2'].astype(str).str[:3]
WeekPlayers['Team 1.1'] = WeekPlayers['Team 1.1'].str.rstrip('-')
WeekPlayers['Team 2.1'] = WeekPlayers['Team 2.1'].str.rstrip('-')
WeekPlayers['Team 1.2'] = WeekPlayers['Game 1'].astype(str).str[-4:]
WeekPlayers['Team 1.2'] = WeekPlayers['Team 1.2'].str.lstrip('-')
WeekPlayers['Team 1.2'] = WeekPlayers['Team 1.2'].str.rstrip(')')
WeekPlayers['Team 2.2'] = WeekPlayers['Game 2'].astype(str).str[-4:]
WeekPlayers['Team 2.2'] = WeekPlayers['Team 2.2'].str.lstrip('-')
WeekPlayers['Team 2.2'] = WeekPlayers['Team 2.2'].str.rstrip(')')
WeekPlayers = WeekPlayers.reset_index(drop=True)
i=0
while (i<WeekPlayers.shape[0]):
    if (WeekPlayers['Team 1.1'].iloc[i] == WeekPlayers['Team 2.1'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.2'].iloc[i])
    elif (WeekPlayers['Team 1.1'].iloc[i] == WeekPlayers['Team 2.2'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.1'].iloc[i])
    elif (WeekPlayers['Team 1.2'].iloc[i] == WeekPlayers['Team 2.1'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.2'].iloc[i])
    elif (WeekPlayers['Team 1.2'].iloc[i] == WeekPlayers['Team 2.2'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.2'].iloc[i])
    i+=1
        
WeekPlayers1 = WeekPlayers[['Players','Team 1','Opponent 1','Points 1']].rename(columns={'Players':'Player','Team 1': 'Team','Opponent 1':'Opponent','Points 1':'Points'})
WeekPlayers2 = WeekPlayers[['Players','Team 2','Opponent 2','Points 2']].rename(columns={'Players':'Player','Team 2': 'Team','Opponent 2':'Opponent','Points 2':'Points'})       
WeekPlayers = WeekPlayers1.append(WeekPlayers2,sort='True')        
WeekPlayers['Week'] = 64
WeekPlayers['Region'] = 'EU'
WeekPlayers = WeekPlayers.reset_index(drop=True)
WeekPlayers = WeekPlayers[['Week','Player','Team','Opponent','Region','Points']]
total = total.append(WeekPlayers,sort=False)


Week = pd.read_excel("FantasyLCSPlayerPoints.xlsx",sheet_name="Week2")
Week = Week.iloc[(Week[Week['Players'].isna()].index[0]+ 1):]
Week = Week[Week['Players'].notna()]
WeekPlayers = Week[(Week['Players'].str.isupper()==False)&(Week['Players'] != 100)]
WeekPlayers[['Points 1','Game 1']] = WeekPlayers['Game 1'].str.split('(',expand=True)
WeekPlayers[['Points 2','Game 2']] = WeekPlayers['Game 2'].str.split('(',expand=True)
WeekPlayers['Team 1.1'] = WeekPlayers['Game 1'].astype(str).str[:3]
WeekPlayers['Team 2.1'] = WeekPlayers['Game 2'].astype(str).str[:3]
WeekPlayers['Team 1.1'] = WeekPlayers['Team 1.1'].str.rstrip('-')
WeekPlayers['Team 2.1'] = WeekPlayers['Team 2.1'].str.rstrip('-')
WeekPlayers['Team 1.2'] = WeekPlayers['Game 1'].astype(str).str[-4:]
WeekPlayers['Team 1.2'] = WeekPlayers['Team 1.2'].str.lstrip('-')
WeekPlayers['Team 1.2'] = WeekPlayers['Team 1.2'].str.rstrip(')')
WeekPlayers['Team 2.2'] = WeekPlayers['Game 2'].astype(str).str[-4:]
WeekPlayers['Team 2.2'] = WeekPlayers['Team 2.2'].str.lstrip('-')
WeekPlayers['Team 2.2'] = WeekPlayers['Team 2.2'].str.rstrip(')')
WeekPlayers = WeekPlayers.reset_index(drop=True)
i=0
while (i<WeekPlayers.shape[0]):
    if (WeekPlayers['Team 1.1'].iloc[i] == WeekPlayers['Team 2.1'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.2'].iloc[i])
    elif (WeekPlayers['Team 1.1'].iloc[i] == WeekPlayers['Team 2.2'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.1'].iloc[i])
    elif (WeekPlayers['Team 1.2'].iloc[i] == WeekPlayers['Team 2.1'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.2'].iloc[i])
    elif (WeekPlayers['Team 1.2'].iloc[i] == WeekPlayers['Team 2.2'].iloc[i]):
        WeekPlayers.set_value(i,'Team 1',WeekPlayers['Team 1.2'].iloc[i])
        WeekPlayers.set_value(i,'Team 2',WeekPlayers['Team 2.2'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 1',WeekPlayers['Team 1.1'].iloc[i])
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.2'].iloc[i])
    
    i+=1
        
WeekPlayers1 = WeekPlayers[['Players','Team 1','Opponent 1','Points 1']].rename(columns={'Players':'Player','Team 1': 'Team','Opponent 1':'Opponent','Points 1':'Points'})
WeekPlayers2 = WeekPlayers[['Players','Team 2','Opponent 2','Points 2']].rename(columns={'Players':'Player','Team 2': 'Team','Opponent 2':'Opponent','Points 2':'Points'})       
WeekPlayers = WeekPlayers1.append(WeekPlayers2,sort='True')        
WeekPlayers['Week'] = 64
WeekPlayers['Region'] = 'NA'
WeekPlayers = WeekPlayers[['Week','Player','Team','Opponent','Region','Points']]
WeekPlayers = WeekPlayers[WeekPlayers['Points'] != '']
WeekPlayers = WeekPlayers.reset_index(drop=True)
total = total.append(WeekPlayers,sort=False)
toal = total.reset_index(drop=True)


