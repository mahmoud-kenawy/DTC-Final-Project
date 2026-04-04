{{ config(
    materialized='table' 
) }}

WITH categories AS (
    SELECT * FROM {{ ref('mrt_earthquake_categories') }}
),
emergencies AS (
    SELECT * FROM {{ ref('mrt_emergency') }}
)

SELECT 
    c.earthquake_id,
    c.event_timestamp,
    c.magnitude,            -- رجعناها للقوة الأصلية للزلزال
    {{ classify_earthquake('c.magnitude') }} AS magnitude_category, -- التصنيف مبني على القوة الأصلية
    c.latitude || ',' || c.longitude AS location_coordinates,
    c.region_name,
    COALESCE(e.emergency_level, 'Routine') AS emergency_level, 
    e.station_has_effected
FROM categories c
LEFT JOIN emergencies e ON c.earthquake_id = e.earthquake_id