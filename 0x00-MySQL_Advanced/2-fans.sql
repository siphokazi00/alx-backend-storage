-- Create a table to store the ranking of band origins
CREATE TABLE IF NOT EXISTS band_origins (
    origin VARCHAR(255) NOT NULL,
    nb_fans INT NOT NULL
);

-- Populate the band_origins table with aggregated fan counts
INSERT INTO band_origins (origin, nb_fans)
SELECT origin, COUNT(*) AS nb_fans
FROM metal_bands
GROUP BY origin;

-- Select and order the results by the number of fans in descending order
SELECT origin, nb_fans
FROM band_origins
ORDER BY nb_fans DESC;
