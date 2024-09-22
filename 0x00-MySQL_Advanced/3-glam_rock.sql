-- Create a query to calculate the lifespan of Glam rock bands
SELECT 
    band_name,
    (2022 - formed) AS lifespan
FROM 
    metal_bands
WHERE 
    style = 'Glam rock'
ORDER BY 
    lifespan DESC;
