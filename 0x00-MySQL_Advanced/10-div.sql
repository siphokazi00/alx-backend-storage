-- Drop the function if it already exists
DROP FUNCTION IF EXISTS SafeDiv;

-- Create the SafeDiv function
DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT) 
RETURNS FLOAT
DETERMINISTIC
BEGIN
    RETURN CASE 
        WHEN b = 0 THEN 0 
        ELSE a / b 
    END;
END;
//

DELIMITER ;
