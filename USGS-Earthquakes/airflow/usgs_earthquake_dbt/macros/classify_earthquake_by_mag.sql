{% macro classify_earthquake(magnitude_column) %}
    CASE
        WHEN {{ magnitude_column }} >= 8 THEN 'Great'
        WHEN {{ magnitude_column }} >= 7 THEN 'Major'
        WHEN {{ magnitude_column }} >= 6 THEN 'Strong'
        WHEN {{ magnitude_column }} >= 5 THEN 'Moderate'
        WHEN {{ magnitude_column }} >= 4 THEN 'Light'
        WHEN {{ magnitude_column }} >= 3 THEN 'Minor'
        ELSE 'Micro'
    END
{% endmacro %}

