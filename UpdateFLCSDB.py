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
while (i < a.shape[0]): 
    if (b[b==c.iloc[i]].shape[0] > 0):
        b = b[b!=b.iloc[d]]
        a = a[a['Week'].astype(str) + a['Team'] + a['Opponent'] != b.iloc[d]]
        i += 1
    else:
        d += 1
        i += 1


total3 = a

cur.execute("DROP TABLE IF EXISTS player")
total.to_sql(name='player',con=e,dtype={"Split": Float, "Week": Float, "Player": String(32), "Position": String(32), "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})
cur.execute("DROP TABLE IF EXISTS team")
total2.to_sql(name='team',con=e,dtype={"Split": Float, "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})
#cur.execute("DROP TABLE IF EXISTS results")
#total2.to_sql(name='results',con=e,dtype={"Split": Float, "Week": String(32), "Team": String(32), "Opponent": String(32), "Result": String(32)})

