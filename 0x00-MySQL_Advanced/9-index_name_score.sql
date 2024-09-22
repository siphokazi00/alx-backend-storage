-- Drop the index if it already exists
DROP INDEX IF EXISTS idx_name_first_score ON names;

-- Create the index on the first letter of the name and score
CREATE INDEX idx_name_first_score ON names (name(1), score);
