CREATE DEFINER=`root`@`localhost` PROCEDURE `curdemo`()
BEGIN

	DECLARE done INT DEFAULT False;
	DECLARE wk INT;
	DECLARE cur CURSOR FOR SELECT DISTINCT Week FROM elo WHERE Week <> 1;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

	OPEN cur;


	read_loop: LOOP
		FETCH cur INTO wk;
        IF done THEN
			LEAVE read_loop;
		END IF;
            
		UPDATE elo elo
		LEFT JOIN (SELECT elo.Team, SUM(Team_ELO/2 + 32*((CASE WHEN Result IS NULL THEN 0.5 ELSE Result END) - (POWER(10,Team_ELO/400)/(POWER(10,Team_ELO/400) + POWER(10,Opp_ELO/400))))) newlo FROM elo JOIN (SELECT Team, MAX(Week) lstwk FROM elo WHERE Week < Wk GROUP BY Team) tmp ON tmp.Team = elo.Team AND tmp.lstwk = elo.Week GROUP BY Team) telo ON elo.Team = telo.Team
		SET elo.Team_ELO = CASE WHEN COALESCE(telo.newlo,1000) < 750 THEN 2 * COALESCE(telo.newlo,1000) ELSE COALESCE(telo.newlo,1000) END
        WHERE Week = wk;

		UPDATE elo elo
        INNER JOIN (SELECT DISTINCT Week, Team, Team_ELO FROM elo WHERE Week = Wk) telo ON telo.Team = elo.Opponent AND telo.Week = elo.Week
        SET elo.Opp_ELO = telo.Team_ELO
        WHERE elo.Week = wk;

    END LOOP;
      
	CLOSE cur;

END