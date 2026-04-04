{%macro classify_earthquake_by_sig(sig_column) %}
    CASE
        WHEN {{ sig_column }} >= 800 THEN 'Critical'
        WHEN {{ sig_column }} >= 600 AND {{ sig_column }} < 800 THEN 'Emergency'
        WHEN {{ sig_column }} >= 400 AND {{ sig_column }} < 600 THEN 'Warning'
        WHEN {{ sig_column }} >= 200 AND {{ sig_column }} < 400 THEN 'Noticeable'
        ELSE 'Routine'
    END
{%endmacro%}
