import numpy as np
import pandas as pd
from os import path
from sqlalchemy import *

e = create_engine('mysql://root:password@localhost:3306/flcs')
conn = e.connect()
cur = conn.connection.cursor()


FLCS_Path = path.abspath(path.curdir)
total = pd.DataFrame(columns=["Split","Week","Player","Position","Team","Opponent","Result","Points"])
i=1
while (i<8):
    scrapedata = pd.read_csv(FLCS_Path + r"\Split" + str(i) + ".csv", delimiter=',',names = ("Player","Week","Position","Team","Points","Excess"),usecols=(0,1,2,3,4,12),encoding='latin-1')
    scrapedata['Player1'] = ''
    scrapedata['Week1'] = ''
    scrapedata['Position1'] = ''
    scrapedata['Team1'] = ''
    scrapedata['Points1'] = ''
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
    total = total.append(complete)
    i+=1


cur.execute("DROP TABLE IF EXISTS player")
total.to_sql(name='player',con=e,dtype={"Split": Float, "Week": Float, "Player": String(32), "Position": String(32), "Team": String(32), "Opponent": String(32), "Result": String(32), "Points": Float})

