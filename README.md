# FLCS
An attempt to create a model to predict fantasy lcs scores and analyze drafting strategies

I'm currently waiting on the new season so that I can set up the scrape code as they are revamping the new format.

My plan is to create an ELO rating system in order to describe each team's strength as well as the probability that one team will beat the other.

Afterwards,  I will use cubic regression splines to find the relationship between the number of points a player gets and the 
  Position
  Result
  Points the team got
  ELO of team
  ELO of opponent
  Position strength
  
I will then use a General Additive Model and Elastic Net to generate a player by player model to estimate the amount of points each player will get per week as well as rate player by their capabilities as a player by removing the factors of being on a good team and position


10/13/2019

Update scripts:
  FLCSDB.py
  FLCS.py

I've gone back and updated the scripts as it looks as though we didn't get a fantasy lcs this year as we were expecting.
Most of the updates focus on cleaning up the dataframe manipulations as well as improve the scraping itself
I'll look into visualization as well as basic data analysis although the limited number of input values will be interesting to work around.  I'll also look into using the ELO system as a possibility.

1/23/2020

Looks like the website I scraped from is down.  Regardless, the current plan is to do what I can to create visualizations as well as try to optimize rosters.  I might still try the ELO system

Final Update

I ended up creating a script that calculated the ELO.  I also manually entered game time for one of the splits.  I've created a report that goes over all of my findings
