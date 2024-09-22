-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

-- Create the ComputeAverageWeightedScoreForUser procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE average_weighted_score FLOAT DEFAULT 0;

    -- Calculate total score and total weight
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
END;
