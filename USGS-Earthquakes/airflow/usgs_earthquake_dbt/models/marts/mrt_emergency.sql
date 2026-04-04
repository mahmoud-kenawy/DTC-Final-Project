select 
    earthquake_id,
    event_timestamp,
    significance_score,
    {{ classify_earthquake_by_sig('significance_score') }} AS emergency_level,
    location_description,
    review_status,
    stations_count as station_has_effected
from {{ ref('stg_earthquake') }}
where significance_score >= 400
or has_tsunami_warning = true