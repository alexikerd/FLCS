CREATE DEFINER=`root`@`localhost` PROCEDURE `resetelo`()
BEGIN

	DROP TABLE elo;


	CREATE TABLE elo
		(
		Split int
		,Week int
		,Team varchar(8)
		,Opponent varchar(8)
		,Result int
		,Points int
		,Team_ELO float
		,Opp_ELO float
		);

  
	INSERT INTO elo
		(
		Split
		,Week
		,Team
		,Opponent
		,Result
		,Points
		,Team_ELO
		,Opp_ELO
		)
	SELECT 
		Split
		,9*(Split-1) + CEIL(ROW_NUMBER() OVER (PARTITION BY Team, Split)/2)AS Week
		,Team
		,Opponent
		,CASE WHEN Result = 'L' THEN 0 WHEN Result = 'W' THEN 1 ELSE NULL END AS Result
		,Points 
		,null
		,null
	FROM team 
	ORDER BY Split, Week;
    
    UPDATE elo elo
		,(SELECT Team, MIN(Week) minweek FROM elo GROUP BY Team) early
	SET Team_ELO = 1000
	WHERE elo.Team = early.Team AND elo.Week = early.minweek;
    
    
    UPDATE elo elo
		,(SELECT Opponent, MIN(WEEK) minweek FROM elo GROUP BY Opponent) early
	SET Opp_ELO = 1000
	WHERE elo.Opponent = early.Opponent AND elo.Week = early.minweek;
    
END