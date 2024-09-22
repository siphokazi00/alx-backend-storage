-- Drop the index if it already exists
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create the index on the first letter of the name
CREATE INDEX idx_name_first ON names (name(1));
