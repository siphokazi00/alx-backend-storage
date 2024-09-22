-- Check if the table exists before creating it
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,  -- Auto incrementing primary key
    email VARCHAR(255) NOT NULL UNIQUE,    -- Email field, unique and not null
    name VARCHAR(255),                     -- Name field, optional
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'  -- Country field with default value
);
