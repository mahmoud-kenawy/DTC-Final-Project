SELECT
    id as earthquake_id,
    properties:place as location_description,
    to_timestamp(properties:time) as event_timestamp,
    to_timestamp(properties:updated) as updated_timestamp,
    properties:type as event_type,
    properties:mag::FLOAT as magnitude,
    properties:magType as magnitude_type,
    properties:sig as significance_score,
    COALESCE(properties:alert, 'unrated') as alert_level,
    properties:tsunami>0 as has_tsunami_warning,
    geometry:coordinates[0]::FLOAT AS longitude,
    geometry:coordinates[1]::FLOAT AS latitude,
    geometry:coordinates[2]::FLOAT AS depth_km,
    properties:status AS review_status,
    properties:nst::INT AS stations_count
FROM {{ source('usgs_data', 'earthquakes') }}