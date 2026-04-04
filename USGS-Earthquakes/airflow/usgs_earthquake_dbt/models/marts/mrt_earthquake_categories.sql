Select 
    earthquake_id,
    event_timestamp,
    magnitude,
    {{ classify_earthquake('magnitude') }} AS magnitude_category,
    location_description,
    TRIM(SPLIT_PART(location_description, ',', 2)) AS region_name,
    longitude,
    latitude,
    review_status
from {{ ref('stg_earthquake') }}