-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Create the ComputeAverageWeightedScoreForUsers procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE done INT DEFAULT FALSE;

    -- Declare a cursor for iterating through users
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN user_cursor;

    -- Loop through all users
    read_loop: LOOP
        FETCH user_cursor INTO user_id;

        IF done THEN
            LEAVE read_loop;
        END IF;

        DECLARE total_score FLOAT DEFAULT 0;
        DECLARE total_weight INT DEFAULT 0;
        DECLARE average_weighted_score FLOAT DEFAULT 0;

        -- Calculate total score and total weight for the current user
        SELECT SUM(c.score * p.weight) INTO total_score
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        SELECT SUM(p.weight) INTO total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;

        -- Calculate the average weighted score
        IF total_weight > 0 THEN
            SET average_weighted_score = total_score / total_weight;
        ELSE
            SET average_weighted_score = 0;
        END IF;

        -- Update the average_score in the users table
        UPDATE users SET average_score = average_weighted_score WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE user_cursor;
END;
