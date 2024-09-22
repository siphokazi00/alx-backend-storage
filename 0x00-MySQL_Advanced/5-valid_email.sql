-- Drop the existing trigger if it exists
DROP TRIGGER IF EXISTS reset_valid_email;

-- Create the trigger that fires before an update on the users table
CREATE TRIGGER reset_valid_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email has changed
    IF OLD.email <> NEW.email THEN
        -- Reset valid_email to false (0)
        SET NEW.valid_email = 0;
    END IF;
END;
