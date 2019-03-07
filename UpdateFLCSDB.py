import numpy as np
import pandas as pd
from os import path
from sqlalchemy import *

FLCS_Path = path.abspath(path.curdir)

rawdata = pd.read_csv(FLCS_Path + r"\FLCS.csv", delimiter=',',names = ("Split","Player","Position","Team","Win/Loss","Points"),usecols=(0,1,3,4,5,6))
rawdata['Week'] = ''
rawdata['Opponent'] = rawdata['Team'].astype(str).str[-3:]
rawdata['Excess'] = rawdata['Position']
rawdata['Win/Loss'] = rawdata['Win/Loss'].astype(str).str[0]
rawdata['Team'] = rawdata['Team'].astype(str).str[:3]
rawdata = rawdata[["Split","Week","Player","Position","Team","Opponent","Win/Loss","Points","Excess"]]
rawdata['Week'] = rawdata['Player'].astype(str).str[-1:]
rawdata['Position'] = rawdata['Position'].fillna(method='ffill')
a = 1
week = []
replace = []
while (a < 10):
    week.append("Week %d" % a)
    replace.append(np.nan)
    a = a + 1
rawdata['Player'] = rawdata['Player'].replace(week,replace)
rawdata['Player'] = rawdata['Player'].fillna(method='ffill')
rawdata = rawdata[rawdata['Excess'].isna()]
rawdata = rawdata.drop(columns = ['Excess'])