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
