{% macro classify_earthquake(magnitude_column) %}
    CASE
        WHEN {{ magnitude_column }} >= 8 THEN 'Great'
        WHEN {{ magnitude_column }} >= 7 AND {{ magnitude_column }} < 8 THEN 'Major'
        WHEN {{ magnitude_column }} >= 6 AND {{ magnitude_column }} < 7 THEN 'Strong'
        WHEN {{ magnitude_column }} >= 5 AND {{ magnitude_column }} < 6 THEN 'Moderate'
        WHEN {{ magnitude_column }} >= 4 AND {{ magnitude_column }} < 5 THEN 'Light'
        WHEN {{ magnitude_column }} >= 3 AND {{ magnitude_column }} < 4 THEN 'Minor'
        ELSE 'Micro'
    END
{% endmacro %}

