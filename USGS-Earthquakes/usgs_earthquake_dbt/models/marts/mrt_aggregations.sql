select 
    date(event_timestamp) as event_date,
    count(earthquake_id) as total_earthquakes,
    max(magnitude) as max_magnitude,
    avg(depth_km) as avg_depth,
    sum(case when has_tsunami_warning then 1 else 0 end) as total_tsunami_warnings
from {{ref('stg_earthquake')}}
GROUP BY 1