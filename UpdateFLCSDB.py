import numpy as np
import pandas as pd
from os import path
from sqlalchemy import *

e = create_engine('mysql://root:password@localhost:3306/flcs')
conn = e.connect()
cur = conn.connection.cursor()


FLCS_Path = path.abspath(path.curdir)
total = pd.DataFrame(columns=["Split","Week","Player","Position","Team","Opponent","Result","Points"])
total2 = pd.DataFrame(columns=["Team","Result","Points","Excess"])


i=1
while (i<8):
    scrapedata = pd.read_csv(FLCS_Path + r"\Player" + str(i) + ".csv", delimiter=',',names = ("Player","Week","Position","Team","Points","Excess"),usecols=(0,1,2,3,4,12),encoding='latin-1')
    scrapedata['Player1'] = ''
    scrapedata['Week1'] = ''
    scrapedata['Position1'] = ''
    scrapedata['Team1'] = ''
    scrapedata['Points1'] = ''
    scrapedata['Week'] = scrapedata['Week'].str.rstrip('*')
    small = scrapedata[scrapedata['Excess'].isna()].shift(periods=6,axis='columns')
    big = scrapedata[scrapedata['Excess'].notnull()]
    complete = pd.concat([small,big]).reindex(scrapedata.index)
    complete['Position'] = complete['Position'].fillna(method='ffill')
    complete['Player'] = complete['Player'].fillna(method='ffill')
    complete = complete[complete['Points'].isna()]
    complete = complete.drop(['Week','Team','Points','Excess','Player1'],axis=1)
    complete['Split'] = i
    complete['Week2'] = complete['Week1'].astype(str).str[-1:]
    complete['Week'] = complete['Week2'].astype(int) + ((complete['Split'] - 1) * 9)
    complete['Team'] = complete['Position1'].astype(str).str[:3]
    complete['Opponent'] = complete['Position1'].astype(str).str[-3:]
    complete['Points'] = complete['Points1']
    complete['Result'] = complete['Team1'].astype(str).str[0]
    complete = complete.drop(['Week1','Team1','Points1','Position1','Week2'],axis=1)
    complete = complete[["Split","Week","Player","Position","Team","Opponent","Result","Points"]]
    complete = complete[complete['Points'] != "0.00"]
    total = total.append(complete,sort=True)
   
    scrapedata2 = pd.read_csv(FLCS_Path + r"\Team" + str(i) + ".csv", delimiter=',',names = ("Team","Result","Points","Excess"),usecols=(0,1,3,5))
    scrapedata2['Split'] = str(i)
    scrapedata2['Team'] = scrapedata2['Team'].str.rstrip('*')
    complete2 = scrapedata2[scrapedata2['Excess'] < 10]
    total2 = total2.append(complete2,sort=True)

    i+=1

total['Player'] = total['Player'].replace("Incarnati0n","Jensen")
total['Player'] = total['Player'].replace("Zion Spartan","Darshan")
total['Player'] = total['Player'].replace("Niels","Zven")
total['Position'] = total['Position'].replace("Jungler, Mid","Jungler")

total['Team'] = total['Team'].str.strip()
total['Opponent'] = total['Opponent'].str.strip()


playerroles = total[['Player','Position']].drop_duplicates()
total4 = pd.DataFrame(columns=["Week","Player","Team","Opponent","Region","Points"])
Week = pd.read_excel("Split8.xlsx",sheet_name="Week1")
WeekTeams = Week[Week["Game 1"].isna()]
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
WeekPlayers['Region'] = 'EU'
WeekPlayers = WeekPlayers.reset_index(drop=True)
WeekPlayers = WeekPlayers[['Week','Player','Team','Opponent','Region','Points']]
total4 = total4.append(WeekPlayers,sort=False)


Week = pd.read_excel("Split8.xlsx",sheet_name="Week2")
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
        WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.1'].iloc[i])
    
    i+=1
        
WeekPlayers1 = WeekPlayers[['Players','Team 1','Opponent 1','Points 1']].rename(columns={'Players':'Player','Team 1': 'Team','Opponent 1':'Opponent','Points 1':'Points'})
WeekPlayers2 = WeekPlayers[['Players','Team 2','Opponent 2','Points 2']].rename(columns={'Players':'Player','Team 2': 'Team','Opponent 2':'Opponent','Points 2':'Points'})       
WeekPlayers = WeekPlayers1.append(WeekPlayers2,sort='True')        
WeekPlayers['Week'] = 64
WeekPlayers['Region'] = 'NA'
WeekPlayers = WeekPlayers[['Week','Player','Team','Opponent','Region','Points']]
WeekPlayers = WeekPlayers[WeekPlayers['Points'] != '']
WeekPlayers = WeekPlayers.reset_index(drop=True)
total4 = total4.append(WeekPlayers,sort=False)
total4 = total4.reset_index(drop=True)

j = 2
while(j<10):
    Week = pd.read_excel("Split8.xlsx",sheet_name="Week" + str(j))
    Week = Week.iloc[:(Week[Week['Players'].isna()].index[0])]
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
            WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.1'].iloc[i])

        i+=1

    WeekPlayers1 = WeekPlayers[['Players','Team 1','Opponent 1','Points 1']].rename(columns={'Players':'Player','Team 1': 'Team','Opponent 1':'Opponent','Points 1':'Points'})
    WeekPlayers2 = WeekPlayers[['Players','Team 2','Opponent 2','Points 2']].rename(columns={'Players':'Player','Team 2': 'Team','Opponent 2':'Opponent','Points 2':'Points'})       
    WeekPlayers = WeekPlayers1.append(WeekPlayers2,sort='True')        
    WeekPlayers['Week'] = 63 + j
    WeekPlayers['Region'] = 'EU'
    WeekPlayers = WeekPlayers[['Week','Player','Team','Opponent','Region','Points']]
    WeekPlayers = WeekPlayers[WeekPlayers['Points'] != '']
    WeekPlayers = WeekPlayers.reset_index(drop=True)
    total4 = total4.append(WeekPlayers,sort=False)
    total4 = total4.reset_index(drop=True)
    
    Week = pd.read_excel("Split8.xlsx",sheet_name="Week" + str(j+1))
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
            WeekPlayers.set_value(i,'Opponent 2',WeekPlayers['Team 2.1'].iloc[i])

        i+=1

    WeekPlayers1 = WeekPlayers[['Players','Team 1','Opponent 1','Points 1']].rename(columns={'Players':'Player','Team 1': 'Team','Opponent 1':'Opponent','Points 1':'Points'})
    WeekPlayers2 = WeekPlayers[['Players','Team 2','Opponent 2','Points 2']].rename(columns={'Players':'Player','Team 2': 'Team','Opponent 2':'Opponent','Points 2':'Points'})       
    WeekPlayers = WeekPlayers1.append(WeekPlayers2,sort='True')        
    WeekPlayers['Week'] = 63 + j
    WeekPlayers['Region'] = 'NA'
    WeekPlayers = WeekPlayers[['Week','Player','Team','Opponent','Region','Points']]
    WeekPlayers = WeekPlayers[WeekPlayers['Points'] != '']
    WeekPlayers = WeekPlayers.reset_index(drop=True)
    total4 = total4.append(WeekPlayers,sort=False)
    total4 = total4.reset_index(drop=True)
    j += 1

total4 = total4.merge(playerroles, on='Player',how='left')
total4['Result'] = ''
total4['Split'] = 8
total4 = total4[["Split","Week","Player","Position","Team","Opponent","Result","Points"]]



total = total.append(total4,sort=false)

total = total[["Split","Week","Player","Position","Team","Opponent","Result","Points"]]

total[total['Player']== 'Soligo'] = total[total['Player']== 'Soligo'].assign(Position = 'Mid')
total[total['Player']== 'Bang'] = total[total['Player']== 'Bang'].assign(Position = 'AD Carry')
total[total['Player']== 'Fragas'] = total[total['Player']== 'Fragas'].assign(Position = 'Jungler')
total[total['Player']== 'Soligo'] = total[total['Player']== 'Soligo'].assign(Position = 'Mid')
total[total['Player']== 'FakeGod'] = total[total['Player']== 'FakeGod'].assign(Position = 'Top')
total[total['Player']== 'Crown'] = total[total['Player']== 'Crown'].assign(Position = 'Mid')
total[total['Player']== 'Broken Blade'] = total[total['Player']== 'Broken Blade'].assign(Position = 'Top')
total[(total['Player']== 'Piglet') & (total['Week']== 72)] = total[(total['Player']== 'Piglet') & (total['Week']== 72)].assign(Position = 'Mid')
total[total['Player']== 'Diamond'] = total[total['Player']== 'Diamond'].assign(Position = 'Support')
total[total['Player']== 'V1per'] = total[total['Player']== 'V1per'].assign(Position = 'Top')
total[total['Player']== 'GorillA'] = total[total['Player']== 'GorillA'].assign(Position = 'Support')
total[total['Player']== 'Humanoid'] = total[total['Player']== 'Humanoid'].assign(Position = 'Mid')
total[total['Player']== 'Exile'] = total[total['Player']== 'Exile'].assign(Position = 'Mid')
total[total['Player']== 'Mowgli'] = total[total['Player']== 'Mowgli'].assign(Position = 'Jungler')
total[total['Player']== 'Jeskla'] = total[total['Player']== 'Jeskla'].assign(Position = 'AD Carry')
total[total['Player']== 'Nemesis'] = total[total['Player']== 'Nemesis'].assign(Position = 'Mid')
total[total['Player']== 'Patrik'] = total[total['Player']== 'Patrik'].assign(Position = 'AD Carry')
total[total['Player']== 'Crownshot'] = total[total['Player']== 'Crownshot'].assign(Position = 'AD Carry')
total[total['Player']== 'Abbedagge'] = total[total['Player']== 'Abbedagge'].assign(Position = 'Mid')
total[total['Player']== 'Selfmade'] = total[total['Player']== 'Selfmade'].assign(Position = 'Jungler')
total[total['Player']== 'Asta'] = total[total['Player']== 'Asta'].assign(Position = 'AD Carry')
total[total['Player']== 'FallenBandit'] = total[total['Player']== 'FallenBandit'].assign(Position = 'Top')
total[total['Player']== 'Special'] = total[total['Player']== 'Special'].assign(Position = 'Mid')
total[total['Player']== 'Finn'] = total[total['Player']== 'Finn'].assign(Position = 'Top')
total[total['Player']== 'Kasing'] = total[total['Player']== 'FallenBandit'].assign(Position = 'Support')
total[total['Player']== 'Orome'] = total[total['Player']== 'Orome'].assign(Position = 'Top')
total[total['Player']== 'Panda'] = total[total['Player']== 'Panda'].assign(Position = 'Jungler')
total[total['Player']== 'Saken'] = total[total['Player']== 'Saken'].assign(Position = 'Mid')
total[total['Player']== 'Auto'] = total[total['Player']== 'Auto'].assign(Position = 'AD Carry')
total[total['Player']== 'Mystiques'] = total[total['Player']== 'Mystiques'].assign(Position = 'Support')
total[total['Player']== 'Promisq'] = total[total['Player']== 'Promisq'].assign(Position = 'Support')
total[total['Player']== 'Kumo'] = total[total['Player']== 'Kumo'].assign(Position = 'Top')















































total2 = total2.drop(['Excess'],axis=1)
total2['Opponent'] = complete2['Team'].astype(str).str[-3:]
total2['Team'] = total2['Team'].astype(str).str[:3]
total2['Result'] = total2['Result'].astype(str).str[0]
total2 = total2[["Split","Team", "Opponent","Result","Points"]]
total2['Team'] = total2['Team'].str.strip()
total2['Opponent'] = total2['Opponent'].str.strip()

a = total[['Split','Week','Team','Opponent','Result']]
a = a.drop_duplicates()
b = a['Week'].astype(str) + a['Team'] + a['Opponent']
c = a['Week'].astype(str) + a['Opponent'] + a['Team']
d = 0
i = 0
while (i < len(c)): 
    if (b[b==c.iloc[i]].shape[0] > 0):
        a = a[a['Week'].astype(str) + a['Team'] + a['Opponent'] != b.iloc[d]]
        b = b[b!=b.iloc[d]]
        i += 1
    else:
        d += 1
        i += 1



total3 = a

cur.execute("DROP TABLE IF EXISTS player")
total.to_sql(name='player',con=e,dtype={"Split": Float, "Week": Float, "Player": String(32), "Position": String(32), "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})
cur.execute("DROP TABLE IF EXISTS team")
total2.to_sql(name='team',con=e,dtype={"Split": Float, "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})
cur.execute("DROP TABLE IF EXISTS results")
total3.to_sql(name='results',con=e,dtype={"Split": Float, "Week": String(32), "Team": String(32), "Opponent": String(32), "Result": String(32)},index=False)

